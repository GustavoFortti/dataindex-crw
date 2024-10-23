
def redirecionamento_button(product_url):
    return f'''
        <a href="{product_url}" target="_blank" id="product_url-link">
            <button id="product_url" role="button">
                <span id="product-button-text">Ir para loja do suplemento</span> 
            </button>
        </a>

        <style>
            #product_url {{
                align-items: center;
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 0.25rem;
                box-shadow: rgba(0, 0, 0, 0.02) 0 1px 3px 0;
                box-sizing: border-box;
                color: rgba(0, 0, 0, 0.85);
                cursor: pointer;
                display: inline-flex;
                font-family: system-ui, -apple-system, system-ui, "Helvetica Neue", Helvetica,
                    Arial, sans-serif;
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
            #product_url:hover,
            #product_url:focus {{
                border-color: rgba(0, 0, 0, 0.15);
                box-shadow: rgba(0, 0, 0, 0.1) 0 4px 12px;
                color: rgba(0, 0, 0, 0.65);
            }}
            #product_url:hover {{
                transform: translateY(-1px);
            }}
            #product_url:active {{
                background-color: #f0f0f1;
                border-color: rgba(0, 0, 0, 0.15);
                box-shadow: rgba(0, 0, 0, 0.06) 0 2px 4px;
                color: rgba(0, 0, 0, 0.65);
                transform: translateY(0);
            }}
            
            #product-button-text {{
                font-weight: bold; /* Deixa o texto do cupom em negrito */
                margin-right: 5px; /* Espaço entre o cupom e o texto "Copiar" */
            }}
        </style>
    '''