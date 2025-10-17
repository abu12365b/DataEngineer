@echo off
REM Daily Weather ETL Job
REM This script runs the ETL pipeline using conda

echo ========================================
echo Running Daily Weather ETL Pipeline
echo Started at: %date% %time%
echo ========================================

cd /d "c:\Users\abuba\OneDrive\Desktop\Github\DataEngineer\mini_weather_ETl\ETL"

REM Run the ETL pipeline using conda
conda run -p C:\Users\abuba\anaconda3 --no-capture-output python runETL.py

echo ========================================
echo ETL Pipeline Completed
echo Finished at: %date% %time%
echo ========================================

REM Optional: Keep window open to see results (remove for production)
REM pause
