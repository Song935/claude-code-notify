"""카카오톡 '나에게 보내기'로 알림을 보낸다.

사용법:
    python kakao_notify.py setup <REST_API_KEY> <CLIENT_SECRET>   # 키 저장 (PC마다 한 번)
    python kakao_notify.py auth                                   # 카카오 로그인 동의 (브라우저가 열림)
    python kakao_notify.py send "보낼 메시지"                      # 알림 보내기
    python kakao_notify.py hook                                   # Claude Code Notification 훅 (stdin JSON)

키와 토큰은 ~/.claude/kakao/ 에만 저장하고 저장소에는 올리지 않는다.
"""
import http.server
import json
import sys
import time
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

DIR = Path.home() / ".claude" / "kakao"
CONFIG = DIR / "config.json"
TOKENS = DIR / "tokens.json"
REDIRECT_URI = "http://localhost:8765/callback"


def load(path):
    if not path.exists():
        sys.exit(f"{path} 가 없습니다. 먼저 setup/auth 를 실행하세요.")
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, data):
    DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def post(url, data, token=None):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())
    req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"카카오 API 오류 {e.code}: {e.read().decode(errors='replace')}")


def store_tokens(resp, old=None):
    now = int(time.time())
    tokens = dict(old or {})
    tokens["access_token"] = resp["access_token"]
    tokens["access_expires_at"] = now + int(resp["expires_in"])
    if "refresh_token" in resp:  # 만료가 가까울 때만 새 refresh token이 온다
        tokens["refresh_token"] = resp["refresh_token"]
        tokens["refresh_expires_at"] = now + int(resp["refresh_token_expires_in"])
    save(TOKENS, tokens)
    return tokens


def cmd_setup(rest_key, client_secret):
    save(CONFIG, {"rest_api_key": rest_key, "client_secret": client_secret})
    print(f"키 저장 완료: {CONFIG}")


def cmd_auth():
    cfg = load(CONFIG)
    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            result.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            msg = "인증 완료. 이 창은 닫아도 됩니다." if "code" in result else "인증 실패. 터미널을 확인하세요."
            self.wfile.write(f"<h2>{msg}</h2>".encode())

        def log_message(self, *a):
            pass

    url = "https://kauth.kakao.com/oauth/authorize?" + urllib.parse.urlencode({
        "client_id": cfg["rest_api_key"], "redirect_uri": REDIRECT_URI,
        "response_type": "code", "scope": "talk_message",
    })
    server = http.server.HTTPServer(("127.0.0.1", 8765), Handler)
    server.timeout = 300
    print("브라우저에서 카카오 로그인 후 동의해 주세요...")
    webbrowser.open(url)
    while "code" not in result and "error" not in result:
        server.handle_request()
    server.server_close()
    if "error" in result:
        sys.exit(f"인증 실패: {result}")

    resp = post("https://kauth.kakao.com/oauth/token", {
        "grant_type": "authorization_code", "client_id": cfg["rest_api_key"],
        "client_secret": cfg["client_secret"], "redirect_uri": REDIRECT_URI, "code": result["code"],
    })
    store_tokens(resp)
    print(f"토큰 저장 완료: {TOKENS}")


def access_token():
    cfg, tokens = load(CONFIG), load(TOKENS)
    if time.time() < tokens["access_expires_at"] - 60:
        return tokens["access_token"]
    resp = post("https://kauth.kakao.com/oauth/token", {
        "grant_type": "refresh_token", "client_id": cfg["rest_api_key"],
        "client_secret": cfg["client_secret"], "refresh_token": tokens["refresh_token"],
    })
    return store_tokens(resp, tokens)["access_token"]


def cmd_send(text):
    template = {"object_type": "text", "text": text[:200], "link": {}}
    resp = post("https://kapi.kakao.com/v2/api/talk/memo/default/send",
                {"template_object": json.dumps(template, ensure_ascii=False)}, access_token())
    if resp.get("result_code") != 0:
        sys.exit(f"전송 실패: {resp}")
    print("카카오톡 전송 완료")


def cmd_hook():
    # Claude Code가 확인을 기다릴 때 호출된다. 알림 실패가 Claude 작업을 막지 않도록 오류는 무시한다.
    try:
        raw = sys.stdin.buffer.read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("cp949", errors="replace")  # 한국어 Windows 기본 인코딩
        data = json.loads(text or "{}")
        folder = Path(data.get("cwd", "")).name or "?"
        cmd_send(f"🔔 Claude가 확인을 기다려요 [{folder}]\n{data.get('message', '')}")
    except BaseException:
        pass


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if args[:1] == ["setup"] and len(args) == 3:
        cmd_setup(args[1], args[2])
    elif args == ["auth"]:
        cmd_auth()
    elif args[:1] == ["send"] and len(args) == 2:
        cmd_send(args[1])
    elif args == ["hook"]:
        cmd_hook()
    else:
        sys.exit(__doc__)
