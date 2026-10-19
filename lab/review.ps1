$ErrorActionPreference = 'Stop'
$out = 'C:\ProgramData\MohamedLab\Phishing'
New-Item -ItemType Directory -Path $out -Force | Out-Null
[pscustomobject]@{
    utc = (Get-Date).ToUniversalTime().ToString('o')
    computer = $env:COMPUTERNAME
    user = [Security.Principal.WindowsIdentity]::GetCurrent().Name
    pid = $PID
    result = 'Attachment execution marker'
} | ConvertTo-Json | Set-Content "$out\review-result.json" -Encoding UTF8
Invoke-WebRequest 'http://10.0.2.2:8766/phishing/ack?case=benefits-review' -UseBasicParsing | Out-Null
