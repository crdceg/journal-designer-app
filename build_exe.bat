@echo off

pyinstaller ^
--noconfirm ^
--onefile ^
--windowed ^
--icon=assets/icons/app.ico ^
--collect-all docxcompose ^
--add-data "assets;assets" ^
--add-data "config;config" ^
--add-data "templates;templates" ^
--add-data "covers;covers" ^
main.py

pause