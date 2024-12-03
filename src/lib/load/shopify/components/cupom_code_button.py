def cupom_code_button(cupom_code, discount_percent_cupom):
    return f'''
        <br>
        <div style="margin: 15px 0 1rem 0;">
            <a href="#" id="cupom-link">
                <button id="copy-cupom-btn" role="button">
                    Copiar -&nbsp;<span id="cupom-text"> {cupom_code}</span> 
                </button>
            </a>
        </div>
        
        <div style="text-align: left; margin: 15px 0 1rem 0;">
            <p>Clique no botão acima para copiar o cupom!</p>
            <h3><strong>{discount_percent_cupom} de desconto</strong> nas compras usando o cupom: <strong>{cupom_code}</strong></h3>
        </div>

        <!-- CSS para estilizar o botão -->
        <style>
            #copy-cupom-btn {{
                align-items: center;
                background-color: #000000; /* Fundo preto */
                border: 1px solid rgba(255, 255, 255, 0.1); /* Borda branca translúcida */
                border-radius: 0.25rem;
                box-shadow: rgba(255, 255, 255, 0.02) 0 1px 3px 0;
                box-sizing: border-box;
                color: rgba(255, 255, 255, 0.85); /* Texto branco */
                cursor: pointer;
                display: inline-flex;
                font-family: system-ui, -apple-system, system-ui, "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 16px;
                font-weight: 400;
                justify-content: center;
                line-height: 1.25;
                margin: 0;
                min-height: 3rem;
                padding: calc(0.875rem - 1px) calc(1.5rem - 1px);
                position: relative;
                text-decoration: none;
                transition: all 250ms;
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                vertical-align: baseline;
                width: 100%;
            }}

            #copy-cupom-btn:hover,
            #copy-cupom-btn:focus {{
                border-color: rgba(255, 255, 255, 0.15); /* Borda branca mais visível no hover */
                box-shadow: rgba(255, 255, 255, 0.1) 0 4px 12px;
                color: rgba(255, 255, 255, 0.85); /* Mantém o texto branco */
            }}

            #copy-cupom-btn:hover {{
                transform: translateY(-1px);
            }}

            #copy-cupom-btn:active {{
                background-color: #333333; /* Fundo preto mais claro ao clicar */
                border-color: rgba(255, 255, 255, 0.15);
                box-shadow: rgba(255, 255, 255, 0.06) 0 2px 4px;
                color: rgba(255, 255, 255, 0.85); /* Texto branco */
                transform: translateY(0);
            }}

            #cupom-text {{
                font-weight: bold; /* Deixa o texto do cupom em negrito */
                margin-right: 5px; /* Espaço entre o cupom e o texto "Copiar" */
            }}
        </style>

        <!-- Script para copiar o cupom -->
        <script>
            document.getElementById('copy-cupom-btn').addEventListener('click', function(event) {{
                event.preventDefault(); // Previne o comportamento padrão do link

                // Cria um elemento temporário para armazenar o cupom e copiá-lo
                var tempInput = document.createElement('input');
                tempInput.value = '{cupom_code}';
                document.body.appendChild(tempInput);
                tempInput.select();
                tempInput.setSelectionRange(0, 99999); // Para dispositivos móveis
                document.execCommand('copy');
                document.body.removeChild(tempInput);

                // Exibe uma mensagem indicando que o cupom foi copiado
                alert('Cupom copiado: {cupom_code}');
            }});
        </script>
    '''
