# claude-code-notify

Claude Code가 **확인을 기다리거나 답변을 마쳤을 때** 알려 주는 알림 설정입니다. (Windows 기준)

| 상황 | 훅 | 알림 방식 | 파일 |
|---|---|---|---|
| Claude가 허락·확인을 기다릴 때 | `Notification` | 카카오톡 "나에게 보내기" | `kakao_notify.py` |
| Claude가 답변을 마쳤을 때 | `Stop` | Windows 팝업(토스트) | `toast.ps1` |

VS Code에서 Claude Code를 쓰다가 다른 창을 보고 있어도, 확인이 필요한 순간을 놓치지 않게 해 줍니다.

## 준비물

- Windows 10/11, Python 3, Claude Code
- 카카오 계정 (카카오톡 알림용). 팝업 알림만 쓸 거라면 카카오 설정은 건너뛰어도 됩니다.

## 설치

1. 파일을 아래 위치에 복사합니다.
   - `kakao_notify.py` → `C:\Users\<사용자이름>\.claude\kakao\kakao_notify.py`
   - `toast.ps1` → `C:\Users\<사용자이름>\.claude\notify\toast.ps1`
2. `C:\Users\<사용자이름>\.claude\settings.json`에 `settings.example.json`의 `hooks` 부분을 합칩니다. `<사용자이름>`은 본인 것으로 바꿉니다.
3. Claude Code를 다시 시작합니다.

## 카카오톡 알림 설정 (한 번만)

1. [카카오 디벨로퍼스](https://developers.kakao.com)에서 앱을 만들고 **REST API 키**를 확인합니다.
2. 카카오 로그인을 활성화하고, Redirect URI에 `http://localhost:8765/callback`을 등록합니다.
3. 동의 항목에서 **카카오톡 메시지 전송(`talk_message`)**을 설정하고, 보안 탭에서 **Client Secret**을 발급·활성화합니다.
4. 터미널에서 순서대로 실행합니다.

```
python kakao_notify.py setup <REST_API_KEY> <CLIENT_SECRET>
python kakao_notify.py auth
python kakao_notify.py send "테스트 메시지"
```

`auth`를 실행하면 브라우저가 열립니다. 카카오 로그인 후 동의하면 토큰이 `~/.claude/kakao/`에 저장됩니다.

## 동작 방식

- `Notification` 훅: Claude Code가 훅 정보(JSON)를 표준입력으로 넘기면, 작업 폴더 이름과 메시지를 카카오톡으로 보냅니다. 알림이 실패해도 Claude의 작업은 멈추지 않도록 오류를 무시합니다.
- `Stop` 훅: 답변이 끝나면 `[폴더이름] 답변이 끝났어요` 팝업을 띄웁니다.
- 토큰은 만료되면 자동으로 갱신합니다.

## 주의

- `config.json`(API 키·Client Secret)과 `tokens.json`(토큰)은 `~/.claude/kakao/`에만 저장되며, 이 저장소의 `.gitignore`가 올라가지 않게 막습니다. **절대 공개하지 마세요.**
- 알림은 본인에게만 갑니다. 카카오 API 정책은 바뀔 수 있으니, 안 되면 카카오 디벨로퍼스 문서를 확인하세요.

## 라이선스

MIT