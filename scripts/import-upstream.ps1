$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$dest = Join-Path $root 'upstream'
if (Test-Path -LiteralPath $dest) { throw 'upstream already exists; refusing to overwrite' }
$zip = Join-Path ([IO.Path]::GetTempPath()) ([Guid]::NewGuid().ToString() + '.zip')
try {
    Invoke-WebRequest -UseBasicParsing -Uri 'https://github.com/OMEGAALPHA10/OmegaSolver/releases/download/v5.0.0/OmegaSolver-5.0.0-source.zip' -OutFile $zip
    $expected = 'bd7af05de8b0b731998c00751f2f1c72857af4aafaf89c5d83883aa417f4e287'
    if ((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash -ne $expected) { throw 'Upstream SHA-256 mismatch' }
    Expand-Archive -LiteralPath $zip -DestinationPath $dest
    Write-Host "Verified upstream source extracted to $dest"
} finally {
    Remove-Item -LiteralPath $zip -Force -ErrorAction SilentlyContinue
}
