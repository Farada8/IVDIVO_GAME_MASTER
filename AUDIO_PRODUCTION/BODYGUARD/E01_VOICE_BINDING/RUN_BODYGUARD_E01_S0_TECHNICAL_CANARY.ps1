$ErrorActionPreference = "Stop"
python .\bodyguard_e01_voice_audition_runner.py `
  --stage S0 `
  --requests .\BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_REQUESTS_v1.json `
  --cascade .\BODYGUARD_E01_S0_S4_VOICE_AUDITION_CASCADE_v1.json `
  --bindings .\BODYGUARD_E01_CANDIDATE_VOICE_BINDINGS_v1.json `
  --output-dir .\renders\BODYGUARD_E01_AUDITIONS `
  --execute
