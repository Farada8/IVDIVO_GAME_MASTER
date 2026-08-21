param([Parameter(Mandatory=$true)][string]$Master,[Parameter(Mandatory=$true)][string]$PatchPlan,[Parameter(Mandatory=$true)][string]$AssetBindings,[string]$PatchedMaster = ".\ROOM917_E01_P004A_PATCHED.wav",[string]$RenderReport = ".\ROOM917_E01_P004A_RENDER_REPORT.json",[string]$RegressionReport = ".\ROOM917_E01_P004A_REGRESSION.json")
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $Here "room_bed_patch_renderer.py") --master $Master --patch-plan $PatchPlan --asset-bindings $AssetBindings --out $PatchedMaster --report $RenderReport
python (Join-Path $Here "regression_gate.py") --before $Master --after $PatchedMaster --patch-plan $PatchPlan --scene3-start 444.980 --out $RegressionReport
