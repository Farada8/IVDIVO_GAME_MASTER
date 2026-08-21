param(
  [Parameter(Mandatory=$true)][string]$MasterWav,
  [string]$OutDir = ".\\P003A2_OUTPUT",
  [string]$CueMap = ""
)
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$argsList = @(
  ".\\p003a2_interval_analyzer.py",
  $MasterWav,
  "--segment-start", "0",
  "--segment-end", "444.980",
  "--window-ms", "100",
  "--thresholds", "-85", "-50", "-45",
  "--expected-sha256", "231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8",
  "--output-json", (Join-Path $OutDir "ROOM917_E01_P003A2_INTERVALS_v1.json"),
  "--output-csv", (Join-Path $OutDir "ROOM917_E01_P003A2_INTERVALS_v1.csv")
)
if ($CueMap -ne "") { $argsList += @("--cue-map", $CueMap) }
python @argsList
if ($LASTEXITCODE -ne 0) { throw "P003A2 analyzer failed with exit code $LASTEXITCODE" }
Write-Host "P003A2 measurement complete. Patch authorization still requires cue-lineage join + human/listener evidence."
