param(
  [Parameter(Mandatory=$true)][string]$Master,
  [Parameter(Mandatory=$true)][string]$PatchPlan,
  [Parameter(Mandatory=$true)][string]$AssetCandidates,
  [string]$AssetContract = "",
  [string]$ReleaseProfile = "",
  [string]$BuildId = "",
  [string]$OutDir = ".\P004A_IDENTITY_GATED_OUTPUT"
)
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Room917Root = Split-Path -Parent (Split-Path -Parent $Here)
if ($AssetContract -eq "") { $AssetContract = Join-Path $Room917Root "SOUND_DESIGN\ROOM917_E01_CURRENT_BRANCH_SOUND_ASSET_CONTRACT_v1.json" }
if ($ReleaseProfile -eq "") { $ReleaseProfile = Join-Path $Room917Root "SOUND_DESIGN\ROOM917_E01_RELEASE_TRANSLATION_QC_PROFILE_v1.json" }
if ($BuildId -eq "") { $BuildId = "ROOM917_E01_P004A_" + (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ") }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$Bindings = Join-Path $OutDir "01_IDENTITY_GATED_ASSET_BINDINGS.json"
$BindingReport = Join-Path $OutDir "01_ASSET_BINDING_GATE_REPORT.json"
$PatchedMaster = Join-Path $OutDir "02_ROOM917_E01_P004A_PATCHED.wav"
$RenderReport = Join-Path $OutDir "02_P004A_RENDER_REPORT.json"
$RegressionReport = Join-Path $OutDir "03_P004A_REGRESSION.json"
$Provenance = Join-Path $OutDir "04_DERIVED_MASTER_PROVENANCE.json"
$QcDir = Join-Path $OutDir "05_RELEASE_TRANSLATION_QC"

python (Join-Path $Here "sound_asset_binding_gate.py") --contract $AssetContract --candidates $AssetCandidates --out-bindings $Bindings --report $BindingReport
if ($LASTEXITCODE -ne 0) { throw "Sound asset identity/binding gate HOLD. Patch render forbidden." }
python (Join-Path $Here "room_bed_patch_renderer.py") --master $Master --patch-plan $PatchPlan --asset-bindings $Bindings --out $PatchedMaster --report $RenderReport
if ($LASTEXITCODE -ne 0) { throw "P004A render failed or produced no authorized patch." }
python (Join-Path $Here "regression_gate.py") --before $Master --after $PatchedMaster --patch-plan $PatchPlan --scene3-start 444.980 --out $RegressionReport
if ($LASTEXITCODE -ne 0) { throw "P004A regression gate failed." }
python (Join-Path $Here "build_derived_master_provenance.py") --source $Master --candidate $PatchedMaster --patch-plan $PatchPlan --render-report $RenderReport --regression-report $RegressionReport --build-id $BuildId --out $Provenance
if ($LASTEXITCODE -ne 0) { throw "Derived-master provenance gate failed." }
python (Join-Path $Here "release_translation_qc.py") --master $PatchedMaster --profile $ReleaseProfile --derived-provenance $Provenance --outdir $QcDir
if ($LASTEXITCODE -ne 0) { throw "Derived candidate release/translation machine QC failed or held." }
Write-Host "P004A selective repair + regression + evidence-backed provenance + machine translation QC complete. P003B human listening remains mandatory before release."
