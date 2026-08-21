$ErrorActionPreference = "Stop"
$gate = ".\renders\BODYGUARD_E01_AUDITIONS\S0\BODYGUARD_E01_S0_TECHNICAL_GATE_v1.json"
if (-not (Test-Path $gate)) { throw "S0 gate missing." }
$obj = Get-Content $gate -Raw | ConvertFrom-Json
if ($obj.verdict -ne "PASS_TO_S1") { throw "S0 gate is not PASS_TO_S1." }
python .\bodyguard_e01_voice_audition_runner.py `
  --stage S1 `
  --requests .\BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_REQUESTS_v1.json `
  --cascade .\BODYGUARD_E01_S0_S4_VOICE_AUDITION_CASCADE_v1.json `
  --bindings .\BODYGUARD_E01_CANDIDATE_VOICE_BINDINGS_v1.json `
  --output-dir .\renders\BODYGUARD_E01_AUDITIONS `
  --execute
