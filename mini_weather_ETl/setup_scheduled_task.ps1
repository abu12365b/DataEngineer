# PowerShell Script to Create a Scheduled Task for Daily ETL
# Run this script as Administrator

$TaskName = "DailyWeatherETL"
$ScriptPath = "c:\Users\abuba\OneDrive\Desktop\Github\DataEngineer\mini_weather_ETl\run_etl_daily.bat"
$Description = "Runs weather data ETL pipeline daily at 9:00 AM"
$Time = "9:00AM"

Write-Host "Creating scheduled task: $TaskName" -ForegroundColor Green
Write-Host "Script to run: $ScriptPath" -ForegroundColor Cyan
Write-Host "Schedule: Daily at $Time" -ForegroundColor Cyan

# Create the scheduled task action
$Action = New-ScheduledTaskAction -Execute $ScriptPath

# Create the trigger (daily at 6 AM)
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time

# Create task settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -WakeToRun `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Get current user
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Highest

# Register the scheduled task
try {
    # Check if task already exists
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    
    if ($ExistingTask) {
        Write-Host "Task already exists. Updating..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }
    
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Principal $Principal `
        -Description $Description
    
    Write-Host "`n✅ SUCCESS! Scheduled task created successfully!" -ForegroundColor Green
    Write-Host "`nTask Details:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName"
    Write-Host "  Time: Daily at $Time"
    Write-Host "  Script: $ScriptPath"
    Write-Host "`nTo manage this task:" -ForegroundColor Yellow
    Write-Host "  1. Open Task Scheduler (taskschd.msc)"
    Write-Host "  2. Find '$TaskName' in Task Scheduler Library"
    Write-Host "  3. Right-click to Run, Edit, or Delete"
    Write-Host "`nTo test now, run:" -ForegroundColor Yellow
    Write-Host "  Start-ScheduledTask -TaskName '$TaskName'"
    
} catch {
    Write-Host "`n❌ ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "`nTry running this script as Administrator" -ForegroundColor Yellow
}
