$ErrorActionPreference = "Stop"
Write-Host "BODYGUARD E01 local setup check"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw "Python not found in PATH." }
python -c "import httpx; print('httpx OK')"
$required = @(
  "BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_REQUESTS_v1.json",
  "BODYGUARD_E01_S0_S4_VOICE_AUDITION_CASCADE_v1.json",
  "BODYGUARD_E01_CANDIDATE_VOICE_BINDINGS_v1.json",
  "bodyguard_e01_voice_audition_runner.py"
)
foreach ($f in $required) { if (-not (Test-Path $f)) { throw "Missing file: $f" } }
Write-Host "LOCAL_SETUP_PASS"
Write-Host "API key present in current session:" ([bool]$env:ELEVENLABS_API_KEY)
