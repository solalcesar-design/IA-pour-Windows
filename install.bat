@echo off
title Installation WinAssistant
color 0B
echo.
echo  ==========================================
echo   Installation de WinAssistant
echo  ==========================================
echo.

:: Vérifie si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installé !
    echo Téléchargez Python sur https://www.python.org/downloads/
    echo Cochez "Add Python to PATH" lors de l'installation.
    pause
    exit /b 1
)

echo [OK] Python détecté
echo.
echo Installation des dépendances...
echo.

pip install speechrecognition pyttsx3 wikipedia requests pyaudio pystray pillow --quiet

if %errorlevel% neq 0 (
    echo.
    echo [!] Tentative d'installation de PyAudio via pipwin...
    pip install pipwin --quiet
    pipwin install pyaudio --quiet
)

echo.
echo [OK] Toutes les dépendances sont installées !
echo.
echo Lancement de WinAssistant...
echo.
echo L'assistant démarrera automatiquement à chaque démarrage de Windows.
echo Pour le retrouver dans la barre des tâches, regardez les icônes système.
echo.

python "%~dp0assistant.py"

pause
