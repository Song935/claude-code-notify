# Claude Code Stop 훅: Claude가 답변을 마치면 Windows 알림 팝업을 띄운다.
# stdin으로 훅 JSON(cwd 등)을 받는다. Windows PowerShell 5.1(powershell.exe)로 실행해야 WinRT 알림 API를 쓸 수 있다.
$folder = '?'
try {
    # 훅 JSON은 UTF-8. [Console]::In은 콘솔 코드페이지(cp949)로 읽어 한글 폴더명이 깨지므로 바이트로 받아 UTF-8로 해석한다.
    $ms = New-Object IO.MemoryStream
    [Console]::OpenStandardInput().CopyTo($ms)
    $raw = [Text.Encoding]::UTF8.GetString($ms.ToArray())
    if ($raw) {
        $data = $raw | ConvertFrom-Json
        if ($data.cwd) { $folder = Split-Path $data.cwd -Leaf }
    }
} catch {}

[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

$title = [Security.SecurityElement]::Escape('Claude 작업 완료')
$body = [Security.SecurityElement]::Escape("[$folder] 답변이 끝났어요")
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml("<toast><visual><binding template='ToastGeneric'><text>$title</text><text>$body</text></binding></visual><audio src='ms-winsoundevent:Notification.IM'/></toast>")

$appId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show(
    [Windows.UI.Notifications.ToastNotification]::new($xml))
