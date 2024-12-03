import json

def generate_price_chart(prices: list) -> str:
    """
    Gera o código HTML e JavaScript para exibir um gráfico de preços usando Chart.js.
    
    Args:
    - prices: Lista de dicionários com os dados de preço e data.
    
    Returns:
    - Código HTML + JS do gráfico para ser incorporado ao body_html.
    """
    # Extraindo datas e preços dos dados
    dates = [entry['date'] for entry in prices]
    prices_data = [entry['price'] for entry in prices]
    
    # Definir a escala mínima e máxima com base nos valores de preço
    min_price = int(min(prices_data) - 1)
    max_price = int(max(prices_data) + 1)

    # Geração do código HTML e JS para o gráfico
    chart_html = f'''
    <br>
    <br>
    <div class="chart-container" style="position: relative; height:300px; width:100%;">
        <canvas id="priceChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        var ctx = document.getElementById('priceChart').getContext('2d');
        var priceChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(dates)},  // Datas do gráfico
                datasets: [{{
                    label: 'Preço (R$)',
                    data: {json.dumps(prices_data)},  // Preços do gráfico
                    fill: false,
                    borderColor: '#F34B4B',
                    backgroundColor: 'rgba(243, 75, 75, 0.2)',
                    pointBackgroundColor: '#F34B4B',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    y: {{
                        beginAtZero: false,
                        min: {min_price},  // Escala mínima do eixo Y
                        max: {max_price},  // Escala máxima do eixo Y
                        grid: {{
                            display: true
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false  // Desativar as linhas de fundo na vertical
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top',
                    }}
                }}
            }}
        }});
    </script>
    '''
    
    return chart_html