$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

python -m capsule_builder build `
  --source founder-source/stanai `
  --output dist/stanai.cap `
  @args
