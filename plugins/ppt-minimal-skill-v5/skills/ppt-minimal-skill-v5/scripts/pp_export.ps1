$src = Join-Path $PSScriptRoot "Deck.pptx"
$out = Join-Path (Split-Path $PSScriptRoot -Parent) "extract\Deck_powerpoint.pdf"
# Attach to PowerPoint, open ONLY our deck without a window, export, close ONLY our deck.
# Never Quit PowerPoint and never touch other presentations the user has open.
# PowerPoint may be busy (RPC_E_CALL_REJECTED) while the user works in it, so each call retries.
function Retry([scriptblock]$f) {
  for ($k = 0; $k -lt 30; $k++) {
    try { return & $f } catch { if ($_.Exception.HResult -ne -2147418111) { throw }; Start-Sleep -Milliseconds 1000 }
  }
  throw "PowerPoint stayed busy"
}
$pp = New-Object -ComObject PowerPoint.Application
$p = Retry { $pp.Presentations.Open($src, $true, $false, $false) }
Retry { $p.SaveAs($out, 32) } | Out-Null
Retry { $p.Close() } | Out-Null
"exported $out"
