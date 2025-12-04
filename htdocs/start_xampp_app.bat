@echo off
cd /D C:/xampp
start /MIN "" xampp-control.exe
timeout /t 2 /nobreak >nul
start /MIN python C:/xampp/htdocs/GUI.pyw