param(
  [Parameter(Mandatory=$true)][string]$SourceFile,
  [Parameter(Mandatory=$true)][string]$EscrowDir,
  [Parameter(Mandatory=$true)][string]$AssetId,
  [string]$ExpectedSha256 = ""
)
$ErrorActionPreference = "Stop"
$argsList = @(".\\master_escrow.py", $SourceFile, "--dest-dir", $EscrowDir, "--asset-id", $AssetId)
if ($ExpectedSha256 -ne "") { $argsList += @("--expected-sha256", $ExpectedSha256) }
python @argsList
if ($LASTEXITCODE -ne 0) { throw "Escrow verification failed with exit code $LASTEXITCODE" }
Write-Host "Local byte escrow PASS. Cloud/Drive persistence is NOT claimed until upload + readback is verified."
