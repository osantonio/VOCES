param(
  [switch]$DryRun,
  [string[]]$Keep = @()
)

$Root = (Resolve-Path "$PSScriptRoot\..").Path
$Timestamp = (Get-Date -Format "yyyyMMdd-HHmmss")
$BackupDir = Join-Path $Root "backups"
$null = New-Item -ItemType Directory -Path $BackupDir -ErrorAction SilentlyContinue
$BackupZip = Join-Path $BackupDir "voces-$Timestamp.zip"
$LogFile = Join-Path $BackupDir "deprecation-removal-$Timestamp.log"

function Write-Log($msg) {
  $line = "$(Get-Date -Format o) | $msg"
  $line | Tee-Object -FilePath $LogFile -Append
}

function Backup-Repo {
  if (Test-Path $BackupZip) { Remove-Item $BackupZip -Force }
  $items = Get-ChildItem -Path $Root -Force | Where-Object { $_.Name -ne 'backups' }
  Compress-Archive -Path ($items.FullName) -DestinationPath $BackupZip -Force
  Write-Log "Backup created: $BackupZip"
}

function Remove-DeprecatedMixin {
  $path = Join-Path $Root 'app\models\base.py'
  if (-not (Test-Path $path)) { return }
  $text = Get-Content -Path $path -Raw
  $pattern = "class\s+RedesSocialesMixin[\s\S]*?(?=\nclass\s+|\Z)"
  if ($text -match $pattern) {
    $new = [regex]::Replace($text, $pattern, "")
    if ($DryRun) {
      Write-Log "[DRY] Would remove class RedesSocialesMixin from $path"
    } else {
      Set-Content -Path $path -Value $new -NoNewline
      Write-Log "Removed class RedesSocialesMixin from $path"
    }
  }
  $initPath = Join-Path $Root 'app\models\__init__.py'
  if (Test-Path $initPath) {
    $initText = Get-Content -Path $initPath -Raw
    $initText = $initText -replace 'from app.models.base import ([^\n]*)RedesSocialesMixin,?\s*', 'from app.models.base import $1'
    $initText = $initText -replace '"RedesSocialesMixin",\s*', ''
    if ($DryRun) {
      Write-Log "[DRY] Would update imports and __all__ in $initPath"
    } else {
      Set-Content -Path $initPath -Value $initText -NoNewline
      Write-Log "Updated imports and __all__ in $initPath"
    }
  }
}

function Update-Requirements($packages) {
  $reqPath = Join-Path $Root 'requirements.txt'
  if (-not (Test-Path $reqPath)) { return }
  $lines = Get-Content -Path $reqPath
  $orig = $lines.Clone()
  foreach ($pkg in $packages) {
    if ($Keep -contains $pkg) { Write-Log "Skipped package: $pkg"; continue }
    $lines = $lines | Where-Object { $_ -notmatch "^$pkg==" }
  }
  if ($DryRun) {
    Write-Log "[DRY] Would remove: $($packages -join ', ') from requirements.txt"
  } else {
    Copy-Item -Path $reqPath -Destination (Join-Path $BackupDir "requirements-$Timestamp.bak") -Force
    Set-Content -Path $reqPath -Value ($lines -join "`n")
    Write-Log "Updated requirements.txt and saved backup"
  }
}

function Move-Examples {
  $exPath = Join-Path $Root 'example'
  if (-not (Test-Path $exPath)) { return }
  $dest = Join-Path $BackupDir "example-archived-$Timestamp"
  if ($DryRun) {
    Write-Log "[DRY] Would move $exPath to $dest"
  } else {
    Move-Item -Path $exPath -Destination $dest
    Write-Log "Moved $exPath to $dest"
  }
}

$items = @(
  @{ Name = 'RedesSocialesMixin'; Action = { Remove-DeprecatedMixin } },
  @{ Name = 'requirements:passlib'; Action = { Update-Requirements @('passlib') } },
  @{ Name = 'requirements:itsdangerous'; Action = { Update-Requirements @('itsdangerous') } },
  @{ Name = 'requirements:annotated-doc'; Action = { Update-Requirements @('annotated-doc') } },
  @{ Name = 'requirements:click'; Action = { Update-Requirements @('click') } },
  @{ Name = 'requirements:colorama'; Action = { Update-Requirements @('colorama') } },
  @{ Name = 'example-folder'; Action = { Move-Examples } }
)

Write-Log "Starting deprecation cleanup"
if (-not $DryRun) { Backup-Repo }
foreach ($it in $items) {
  if ($Keep -contains $it.Name) { Write-Log "Kept: $($it.Name)"; continue }
  & $it.Action
}
Write-Log "Completed deprecation cleanup"

Write-Output "Backup: $BackupZip"
Write-Output "Log: $LogFile"
