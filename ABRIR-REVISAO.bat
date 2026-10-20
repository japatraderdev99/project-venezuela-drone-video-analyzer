@echo off
rem Duplo clique (Windows): abre a revisao no navegador. Deixe esta janela aberta enquanto revisa.
cd /d "%~dp0"
where py >nul 2>nul && (py -3 servidor.py) || (python servidor.py)
pause
