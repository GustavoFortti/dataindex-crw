#!/bin/bash

test_chrome() {
    local display=$1
    export DISPLAY=$display
    echo "Iniciando o Chrome no display $DISPLAY..."

    echo "Executando o Chrome com interface gráfica..."
    /usr/bin/google-chrome --no-sandbox --disable-gpu about:blank &  # Executa com interface gráfica

    chrome_pid=$!

    # Espera um pouco para dar tempo do Chrome iniciar
    sleep 3

    # Verifica se o processo ainda está em execução
    if ps -p $chrome_pid > /dev/null; then
        echo "Chrome iniciou com sucesso no display $DISPLAY"
        
        # Fecha o Chrome
        kill $chrome_pid
        return 0
    else
        echo "Falha ao iniciar o Chrome no display $DISPLAY"
        return 1
    fi
}

# Função para testar displays do :0 até :3
find_working_display() {
    active_displays=("0" "1" "1024" "1025")
    for display_num in "${active_displays[@]}"; do
        display=":$display_num"
        echo "Testando o display $display..."
        if test_chrome $display; then
            echo "Usando o display $display"
            return 0
        fi
    done

    echo "Nenhum display funcional encontrado."
    exit 1
}

# Executa a configuração e usa o primeiro display funcional
find_working_display

echo "DISPLAY configurado para: $DISPLAY"