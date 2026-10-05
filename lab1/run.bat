@echo off
rem Запуск без Maven под Windows: компиляция через javac и старт через java.
cd /d "%~dp0"
if exist out rmdir /s /q out
mkdir out
dir /s /b src\main\java\*.java > out\sources.txt
javac -encoding UTF-8 -d out @out\sources.txt
if errorlevel 1 (
    echo Ошибка компиляции.
    pause
    exit /b 1
)
java -Dfile.encoding=UTF-8 -cp out com.example.happiness.Main
pause
