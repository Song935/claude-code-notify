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

## 동작 방식

- `Stop` 훅: Claude Code가 훅 정보(JSON)를 표준입력으로 넘기면, 작업 폴더 이름을 읽어 `[폴더이름] 답변이 끝났어요` 팝업을 띄웁니다.
- 한글 폴더명이 깨지지 않도록 입력을 UTF-8 바이트로 받아 해석합니다.

## 라이선스

MIT