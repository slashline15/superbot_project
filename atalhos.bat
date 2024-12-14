@echo off
REM Ativar o ambiente virtual
call .venv\Scripts\activate.ps1

REM Exemplo: Commit no Git
git commit -m "%1"
