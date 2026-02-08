@echo off
setlocal enabledelayedexpansion
FOR /F "delims=" %%A IN ('cd') DO SET "CURRDIR=%%A"
cd /d %~dp0
npm start
