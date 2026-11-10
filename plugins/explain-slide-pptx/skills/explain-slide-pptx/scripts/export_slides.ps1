# Export every slide of a PPTX to PNG (2560 x 1440) for visual QA.
# Opens its own read-only copy and closes only that presentation. Never calls Quit, so the
# user's other open PowerPoint files stay untouched.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File export_slides.ps1 <deck.pptx> <out_folder>
param([string]$pptx, [string]$outdir)
New-Item -ItemType Directory -Force -Path $outdir | Out-Null
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($pptx, $true, $false, $false)
for ($i = 1; $i -le $pres.Slides.Count; $i++) {
    $png = Join-Path $outdir ("slide_{0:D2}.png" -f $i)
    $pres.Slides($i).Export($png, "PNG", 2560, 1440)
    Write-Output "exported $png"
}
$pres.Close()
