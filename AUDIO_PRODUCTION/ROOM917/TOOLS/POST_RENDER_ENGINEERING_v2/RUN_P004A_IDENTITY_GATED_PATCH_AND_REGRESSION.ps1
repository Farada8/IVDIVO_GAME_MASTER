param(
  [Parameter(Mandatory=$true)][string]$Master,
  [Parameter(Mandatory=$true)][string]$PatchPlan,
  [Parameter(Mandatory=$true)][string]$AssetCandidates,
  [string]$AssetContract = "",
  [string]$OutDir = ".\P004A_IDENTITY_GATED_OUTPUT"
)
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($AssetContract -eq "") {
  $AssetContract = Join-Path (Split-Path -Parent (Split-Path -Parent $Here)) "SOUND_DESIGN\ROOM917_E01_CURRENT_BRANCH_SOUND_ASSET_CONTRACT_v1.json"
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$Bindings = Join-Path $OutDir "01_IDENTITY_GATED_ASSET_BINDINGS.json"
$BindingReport = Join-Path $OutDir "01_ASSET_BINDING_GATE_REPORT.json"
$PatchedMaster = Join-Path $OutDir "02_ROOM917_E01_P004A_PATCHED.wav"
$RenderReport = Join-Path $OutDir "02_P004A_RENDER_REPORT.json"
$RegressionReport = Join-Path $OutDir "03_P004A_REGRESSION.json"

python (Join-Path $Here "sound_asset_binding_gate.py") --contract $AssetContract --candidates $AssetCandidates --out-bindings $Bindings --report $BindingReport
if ($LASTEXITCODE -ne 0) { throw "Sound asset identity/binding gate HOLD. Patch render forbidden." }

python (Join-Path $Here "room_bed_patch_renderer.py") --master $Master --patch-plan $PatchPlan --asset-bindings $Bindings --out $PatchedMaster --report $RenderReport
if ($LASTEXITCODE -ne 0) { throw "P004A render failed or produced no authorized patch." }

python (Join-Path $Here "regression_gate.py") --before $Master --after $PatchedMaster --patch-plan $PatchPlan --scene3-start 444.980 --out $RegressionReport
if ($LASTEXITCODE -ne 0) { throw "P004A regression gate failed." }

Write-Host "P004A identity-gated selective repair complete. Human P003B remains required before release."
