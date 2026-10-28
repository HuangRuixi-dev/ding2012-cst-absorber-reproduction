param([Parameter(Mandatory=$true)][string]$CaseName,[switch]$BuildOnly)
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$caseRoot=Join-Path $taskRoot ('runs\'+$CaseName)
$projectFile=Join-Path $caseRoot 'absorber.cst'
if(Test-Path $projectFile){throw 'Refusing to overwrite an existing model'}
$cstApp=New-Object -ComObject CSTStudio.Application.2023
try {
 $mws=$cstApp.NewMWS()
 $code=((Get-ChildItem (Join-Path $caseRoot 'stages') -Filter '*.vba' | Sort-Object Name | ForEach-Object {[System.IO.File]::ReadAllText($_.FullName)}) -join "`n")
 $built=$mws.AddToHistory('Parametric absorber design',$code)
 if(-not $built){throw 'CST rejected model history'}
 Write-Output 'BUILT complete model'
 $mws.SaveAs($projectFile,$true)
 $mws.Save()
} finally {$cstApp.Quit()}
if(-not $BuildOnly) {
 $started=Get-Date
 $job=Start-Process -FilePath 'D:\Program Files (x86)\CST Studio Suite 2023\CST DESIGN ENVIRONMENT.exe' -ArgumentList @('-m','-f',('"'+$projectFile+'"')) -WindowStyle Hidden -Wait -PassThru
 @{started=$started.ToString('o');finished=(Get-Date).ToString('o');exit_code=$job.ExitCode;project=$projectFile} | ConvertTo-Json | Set-Content (Join-Path $caseRoot 'execution.json')
 if($job.ExitCode -ne 0){throw "CST exited with $($job.ExitCode)"}
 Write-Output "SOLVED $CaseName"
}
