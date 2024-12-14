# Base leve com Python
FROM python:3.10-slim

# Instalar dependências do sistema e utilitários
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    libxi6 \
    libxcursor1 \
    libxdamage1 \
    libxtst6 \
    libatk1.0-0 \
    libgtk-3-0 \
    libxshmfence1 \
    fonts-liberation \
    && apt-get clean

# Baixar e instalar a versão específica do Google Chrome
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_131.0.6778.108-1_amd64.deb && \
    apt-get install -y ./google-chrome-stable_131.0.6778.108-1_amd64.deb && \
    rm google-chrome-stable_131.0.6778.108-1_amd64.deb

# Baixar e instalar a versão específica do ChromeDriver
RUN wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/131.0.6778.85/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf chromedriver-linux64 chromedriver-linux64.zip

# Configurações do Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Torna o script executável
RUN chmod +x ./dev-launcher.sh

# Configurar o ambiente
ENV DISPLAY=:0

# Comando padrão
CMD ["bash", "./dev-launcher.sh"]
