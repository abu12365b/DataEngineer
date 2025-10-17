# Scheduling Your ETL Pipeline

This guide will help you set up your Weather ETL pipeline to run automatically every day at 6:00 AM.

## Quick Setup (Recommended)

### Method 1: Using PowerShell Script (Easiest)

1. **Right-click** on `setup_scheduled_task.ps1`
2. Select **"Run with PowerShell"**
3. If prompted, allow the script to run
4. Done! Your task is scheduled.

**Or run manually:**
```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File "setup_scheduled_task.ps1"
```

### Method 2: Manual Setup with Task Scheduler

1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click **"Create Basic Task"** in the right panel
3. Fill in the wizard:
   - **Name:** DailyWeatherETL
   - **Description:** Runs weather data ETL pipeline daily at 6:00 AM
   - **Trigger:** Daily
   - **Start time:** 6:00 AM
   - **Action:** Start a program
   - **Program/script:** Browse to `run_etl_daily.bat`
4. Check "Open Properties dialog" and click Finish
5. In Properties:
   - **General tab:** Check "Run whether user is logged on or not"
   - **Conditions tab:** Uncheck "Start only if on AC power"
   - **Settings tab:** Check "Run task as soon as possible after scheduled start is missed"
6. Click OK

## Testing Your Scheduled Task

### Test the batch script first:
```cmd
cd "c:\Users\abuba\OneDrive\Desktop\Github\DataEngineer\mini_weather_ETl"
run_etl_daily.bat
```

### Test the scheduled task:
```powershell
Start-ScheduledTask -TaskName "DailyWeatherETL"
```

### Check task history:
1. Open Task Scheduler
2. Find "DailyWeatherETL" in Task Scheduler Library
3. Click on "History" tab (enable it if needed)

## Monitoring & Logs

### Add Logging (Optional)

To save logs of each run, modify `run_etl_daily.bat`:

```batch
@echo off
set LOGFILE=c:\Users\abuba\OneDrive\Desktop\Github\DataEngineer\mini_weather_ETl\logs\etl_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

echo ======================================== >> %LOGFILE%
echo ETL Started at: %date% %time% >> %LOGFILE%
echo ======================================== >> %LOGFILE%

cd /d "c:\Users\abuba\OneDrive\Desktop\Github\DataEngineer\mini_weather_ETl\ETL"
conda run -p C:\Users\abuba\anaconda3 --no-capture-output python runETL.py >> %LOGFILE% 2>&1

echo ======================================== >> %LOGFILE%
echo ETL Completed at: %date% %time% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
```

Then create the logs directory:
```powershell
mkdir "c:\Users\abuba\OneDrive\Desktop\Github\DataEngineer\mini_weather_ETl\logs"
```

## Troubleshooting

### Task doesn't run:
1. Check Task Scheduler history for errors
2. Verify the batch script works manually
3. Ensure the conda path is correct
4. Check that your computer is on at 6 AM

### Permission issues:
- Run the PowerShell setup script as Administrator
- Or manually set the task to run with highest privileges

### Network issues:
- In Task Scheduler Properties → Conditions
- Check "Start only if the following network connection is available"

## Managing the Scheduled Task

### View task:
```powershell
Get-ScheduledTask -TaskName "DailyWeatherETL"
```

### Run task now:
```powershell
Start-ScheduledTask -TaskName "DailyWeatherETL"
```

### Disable task:
```powershell
Disable-ScheduledTask -TaskName "DailyWeatherETL"
```

### Enable task:
```powershell
Enable-ScheduledTask -TaskName "DailyWeatherETL"
```

### Delete task:
```powershell
Unregister-ScheduledTask -TaskName "DailyWeatherETL" -Confirm:$false
```

## Alternative: Apache Airflow

For more advanced scheduling and monitoring, consider using Apache Airflow:

```python
# dags/weather_etl_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 16),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_etl_daily',
    default_args=default_args,
    description='Daily Weather ETL Pipeline',
    schedule_interval='0 6 * * *',  # 6 AM daily
    catchup=False
)

def run_etl():
    import sys
    sys.path.append('c:\\Users\\abuba\\OneDrive\\Desktop\\Github\\DataEngineer\\mini_weather_ETl\\ETL')
    from runETL import run_etl
    run_etl()

etl_task = PythonOperator(
    task_id='run_weather_etl',
    python_callable=run_etl,
    dag=dag,
)
```

## Next Steps

1. ✅ Set up the scheduled task
2. ✅ Test it runs successfully
3. ✅ Monitor for a few days
4. ✅ Add email notifications (optional)
5. ✅ Set up log rotation (optional)
6. ✅ Create a dashboard to visualize your data (optional)
