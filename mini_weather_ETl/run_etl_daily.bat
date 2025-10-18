@echo off
REM Daily Weather ETL Job
REM This script runs the ETL pipeline using conda

REM Toggle: Put computer to sleep after successful ETL (1 = yes, 0 = no)
set "SLEEP_AFTER_ETL=1"

echo ========================================
echo Running Daily Weather ETL Pipeline
echo Started at: %date% %time%
echo ========================================

cd /d "c:\Users\abuba\OneDrive\Desktop\Github\DataEngineer\mini_weather_ETl\ETL"

REM Run the ETL pipeline using conda
conda run -p C:\Users\abuba\anaconda3 --no-capture-output python runETL.py

REM Capture exit code from ETL
set "ETL_EXIT=%ERRORLEVEL%"

echo ========================================
echo ETL Pipeline Completed
echo Finished at: %date% %time%
echo ========================================

REM Optional: Keep window open to see results (remove for production)
REM pause

REM If enabled and ETL succeeded, put the machine to sleep after a short delay
if "%SLEEP_AFTER_ETL%"=="1" (
	if "%ETL_EXIT%"=="0" (
		echo ETL succeeded. Sleeping in 30 seconds...
		timeout /t 30 /nobreak >nul
		REM Attempt to put the system to sleep. Note: On some systems with Hibernate/Hybrid Sleep,
		REM this may hibernate instead of sleep depending on power settings.
		rundll32.exe powrprof.dll,SetSuspendState Sleep
	) else (
		echo ETL failed with exit code %ETL_EXIT%. Skipping sleep.
	)
)
