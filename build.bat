@echo off
echo Criando ambiente virtual...
python -m venv venv
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo Criando executavel...
pyinstaller build_config.spec --clean

echo Copiando arquivos necessarios...
xcopy /E /I /Y "dist\SSD Settings Clean" "release"
rmdir /S /Q build
rmdir /S /Q "dist"

echo Build concluido! O executavel esta na pasta 'release'
pause 