from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

#OBS: PARA VISUALIZAÇÃO DE INFORMACOES MAIS DETALHADAS, O SIGAA POSSUI UMA BASE DE URL PRA CADA CURSO QUE CONSISTE EM:
# https://sigaa.ufpb.br/sigaa/public/curso/<O QUE ESTÁ NO HREF DA TAG A DE CADA LINHA DA COLUNA>

options = webdriver.ChromeOptions()
#options.add_argument("--headless") # Habilitar pra deixar a automação rodando em segundo plano

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://sigaa.ufpb.br/sigaa/public/curso/lista.jsf?nivel=G&aba=p-graduacao")  # Substitua pela URL real

    sleep(1)

    tabela = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "listagem"))
    )

    linhas = tabela.find_elements(By.XPATH, ".//tr[contains(@class, 'linhaPar') or contains(@class, 'linhaImpar')]")

    colunas = ["Nome", "Sede", "Modalidade", "Coordenador"]
    df = pd.DataFrame(columns=colunas)

    def extrair_dados(linhas):
        dados = []
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) > len(df.columns): 
                dados.append([coluna.text for coluna in colunas[:len(df.columns)]])  
        return dados

    dados_extraidos = extrair_dados(linhas)

    df_dados = pd.DataFrame(dados_extraidos, columns=df.columns)

    df = pd.concat([df, df_dados], ignore_index=True)

    print(df)

except Exception as e:
    print(f"Erro: {e}")

finally:
    driver.quit()