# claude-code-notify

Claude Code가 **답변을 마쳤을 때** Windows 팝업(토스트)으로 알려 주는 설정입니다. (Windows 기준)

VS Code에서 Claude Code에게 작업을 맡기고 다른 창을 보고 있어도, 끝난 순간을 놓치지 않게 해 줍니다. 팝업에는 작업 폴더 이름이 함께 표시되어, 여러 프로젝트를 동시에 돌려도 어느 작업인지 구분됩니다.

| 상황 | 훅 | 알림 방식 | 파일 |
|---|---|---|---|
| Claude가 답변을 마쳤을 때 | `Stop` | Windows 팝업(토스트) | `toast.ps1` |

## 준비물

- Windows 10/11, Windows PowerShell 5.1(기본 포함), Claude Code

## 설치

1. `toast.ps1`을 `C:\Users\<사용자이름>\.claude\notify\toast.ps1`에 복사합니다.
2. `C:\Users\<사용자이름>\.claude\settings.json`에 `settings.example.json`의 `hooks` 부분을 합칩니다. `<사용자이름>`은 본인 것으로 바꿉니다.
3. Claude Code를 다시 시작합니다.

## Claude Code에게 설치 맡기기

Claude Code에 아래 문장을 붙여 넣으면 에이전트가 설치합니다. `내이름`은 본인 윈도우 사용자 이름으로 바꿉니다.

```
https://github.com/Song935/claude-code-notify 레포를 보고 윈도우 알림 훅을 설치해줘.

1. 레포의 README.md와 toast.ps1을 먼저 읽고, 무슨 일을 하는 코드인지 나에게 쉬운 말로 설명해줘.
2. toast.ps1을 C:\Users\내이름\.claude\notify\ 폴더에 복사해줘. 폴더가 없으면 만들어줘.
3. C:\Users\내이름\.claude\settings.json에 Stop 훅을 추가해줘. 이미 있는 설정은 지우지 말고 합쳐줘. 수정 전에 어떻게 바뀌는지 먼저 보여줘.
4. 설치가 끝나면 팝업이 뜨는지 확인하는 방법을 알려줘.
```

설치가 끝나면 Claude Code를 다시 시작해야 훅이 적용됩니다.
## 동작 방식

- `Stop` 훅: Claude Code가 훅 정보(JSON)를 표준입력으로 넘기면, 작업 폴더 이름을 읽어 `[폴더이름] 답변이 끝났어요` 팝업을 띄웁니다.
- 한글 폴더명이 깨지지 않도록 입력을 UTF-8 바이트로 받아 해석합니다.

## 라이선스

MIT