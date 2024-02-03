# HOW TO INSTALL CHROME
```
    unzip chrome-linux64.zip -d ~/chrome-linux64

    sudo mv ~/caminho/para/chrome-linux64 /opt/

    sudo ln -s /opt/chrome-linux64/chrome /usr/local/bin/chrome

    sudo nano /usr/share/applications/chrome-custom.desktop

    [Desktop Entry]
    Version=1.0
    Name=Google Chrome (Custom)
    Exec=/opt/chrome-linux64/chrome
    Icon=/opt/chrome-linux64/product_logo_48.png
    Terminal=false
    Type=Application
    Categories=Internet;WebBrowser;
```