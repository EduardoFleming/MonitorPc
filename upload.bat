@echo off
echo ==========================================
echo 🚀 Preparando para subir o Monitor PC...
echo ==========================================

:: Adiciona todos os arquivos novos ou modificados (ignorando o que ta no .gitignore)
git add .

:: Cria uma mensagem de salvamento automatica com a data e hora
git commit -m "Atualizacao automatica - %date% %time%"

:: Envia tudo para o seu repositorio no GitHub
git push -u origin main

echo.
echo ✅ Sucesso! Codigo enviado para o GitHub.
pause