$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
foreach($name in @('report','slides')) {
 $imagesDir=Join-Path (Join-Path $taskRoot $name) 'images'
 New-Item -ItemType Directory -Path $imagesDir -Force | Out-Null
 Get-ChildItem -LiteralPath (Join-Path $taskRoot 'figures') -Filter '*.pdf' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination $imagesDir -Force}
}
foreach($name in @('report','slides','study_notes')) {
 Push-Location (Join-Path $taskRoot $name)
 try {
  1..2 | ForEach-Object {
   & xelatex -interaction=nonstopmode -halt-on-error main.tex | Out-File -LiteralPath ('build_'+$_+'.txt') -Encoding utf8
   if($LASTEXITCODE -ne 0){throw "LaTeX failed in $name; see build logs"}
  }
 } finally {Pop-Location}
}
Write-Output 'Compiled report, Beamer slides, and learning notes.'
