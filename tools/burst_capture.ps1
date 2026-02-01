# Burst Capture Tool (Slow Mode)
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$saveDir = "c:\repos\HD2Dmaker\debug_screenshots"
if (!(Test-Path $saveDir)) { New-Item -ItemType Directory -Path $saveDir | Out-Null }

Get-ChildItem $saveDir | Remove-Item

Write-Host "===" -ForegroundColor Cyan
Write-Host " 3 seconds to start SLOW capturing..." -ForegroundColor Yellow
Write-Host "===" -ForegroundColor Cyan
Start-Sleep -Seconds 3

$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bmp)

# 0.5秒間隔で20枚撮影（合計10秒間）
for ($i = 0; $i -lt 20; $i++) {
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $filename = "$saveDir\capture_$($i.ToString('00')).png"
    $bmp.Save($filename, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Host "Captured: $filename"
    Start-Sleep -Milliseconds 500
}

$graphics.Dispose()
$bmp.Dispose()

Write-Host "Done! Opening folder..." -ForegroundColor Green
Invoke-Item $saveDir
