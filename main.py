from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import math
import time


options = Options()
options.add_argument("--headless")  # Executa sem abrir janela
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.kabum.com.br/computadores/monitores")

# Espera carregar
time.sleep(2)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

qtd_itens_div = soup.find('div', id='listingCount')
qtd_itens = int(qtd_itens_div.find('b').get_text().strip())
print("Total de produtos:", qtd_itens)

qtd_paginas = math.ceil(qtd_itens / 20)
qtd_paginas = 2
print("Total de páginas:", qtd_paginas)

dic_produtos = {
    "descricao": [],
    "preco": [],
    "link": []
}

for i in range(1, qtd_paginas + 1):
    url_pag = f"https://www.kabum.com.br/computadores/monitores?page_number={i}&page_size=20&facet_filters=&sort=most_searched"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url_pag)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    produtos = soup.find_all('div', class_=re.compile('hover:shadow-lg'))
    for produto in produtos:
        descricao = produto.find('span', class_=re.compile('nameCard')).get_text()
        preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()
        link_produto = produto.find('a', class_=re.compile('productLink')).get('href').strip()
        link = f'www.kabum.com.br{link_produto}'
        #print(descricao, preco, link)
        dic_produtos['descricao'].append(descricao)
        dic_produtos['preco'].append(preco)
        dic_produtos['link'].append(link)

df = pd.DataFrame(dic_produtos)
df.to_csv('kabum_monitores.csv', encoding='utf-8-sig', sep=';')