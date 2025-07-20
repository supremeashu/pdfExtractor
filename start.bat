@echo off
echo PDF Heading Extractor
echo.
echo Drag and drop your PDF file onto this window and press Enter
echo Or type the filename manually
echo.
set /p filename="PDF File: "

if "%filename%"=="" (
    echo No file specified
    pause
    exit
)

echo.
echo Installing requirements...
pip install -r requirements.txt >nul 2>&1

echo Processing PDF...
python extract.py "%filename%"

echo.
pause
