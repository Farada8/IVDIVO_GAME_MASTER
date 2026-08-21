param([Parameter(Mandatory=$true)][string]$Master,[Parameter(Mandatory=$true)][string]$TimingMap,[Parameter(Mandatory=$true)][string]$Analyzer,[string]$OutDir = ".\P003A2_OUTPUT")
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Semantic = Join-Path $Here "examples\ROOM917_E01_S01_S02_SEMANTIC_CUE_LINEAGE_v1.json"
$Sha = "231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8"
python (Join-Path $Here "post_render_pipeline.py") --master $Master --expected-sha256 $Sha --semantic-lineage $Semantic --timing-map $TimingMap --analyzer $Analyzer --outdir $OutDir
