import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

import requests
import os

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

logging.info('---- CARREGANDO CREDENCIAIS ----')
credentials = {}
with open('.secrets', 'r') as f:
    for line in f:
        (key, val) = line.split()
        credentials[key] = val

logging.info('---- INICIANDO DRIVER ----')
# set options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# initiate driver
driver = webdriver.Chrome('chromedriver', options=chrome_options)

logging.info('---- REALIZANDO LOGIN NA PÁGINA ----')
# login step
url = 'https://identity.mrv.com.br/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3D22107012-a736-4777-8675-2eb07aef625e%26redirect_uri%3Dhttps%253A%252F%252Fmeuape.mrv.com.br%252Frelacionamento%252Fentrar%26response_type%3Dcode%26scope%3Dcmd.relacionamento.prd%2520cmd.financeiro.prd%2520idp.bfflogin.prd%2520openid%2520profile%2520offline_access%2520cmd.resolver.agendamento.prd%2520cmd.resolver.chamado.prd%2520cmd.resolver.diagnostico.prd%2520cmd.resolver.direcionamento.prd%2520cmd.resolver.unidades.prd%2520cmd.vendadearmario.prd%2520cmd.atendimento.prd%2520cmd.conviver.prd%26state%3D3a1187a1d88247f3bdba12fa8658180e%26code_challenge%3D4f4fzSZXcJWT6DJOb5rMulxAapCoo5O7-uUWEO-ofiw%26code_challenge_method%3DS256%26response_mode%3Dquery'
driver.get(url)
time.sleep(2)
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')
username.send_keys(credentials['username'])
password.send_keys(credentials['password'])
driver.find_element(By.NAME, "button").click()
time.sleep(2)

logging.info('---- INDO PARA A HOMEPAGE ----')
# get to the home page
driver.get('https://meuape.mrv.com.br')
time.sleep(3)

# click 'Acompanhe sua obra' button
relationship_button = driver.find_element(By.ID, 'menu-button-relationship')
driver.execute_script("arguments[0].click();", relationship_button)
time.sleep(5)

# get the ids of the cards
cardResults = driver.find_elements(By.XPATH, '//button[contains(@id, "list-cards-")]')
cards = []
for card in cardResults:
    cards.append(card.get_attribute('id'))

# get the name of the fases
textResults = driver.find_elements(By.XPATH, '//div[@class="styles__CardText-sc-1rwamvk-3 caYGMC"]')
fases = []
for text in textResults:
    fases.append(text.get_attribute('innerHTML').strip())

imgURLS = {}

stop_phrases = [
    'Você visualizou todos os seus momentos dessa fase.',
    'Em breve, novidades do que estamos construindo!',
    'Você ainda não tem nenhuma novidade.'
]

for i, card in enumerate(cards):
    logging.info(f'---- RASPANDO PÁGINA: {fases[i]} ----')
    # navegate 'Fases da obra'
    if i == 0:
        driver.find_element(By.ID, card).click()
    else:
        driver.execute_script("window.scrollTo(0, 0);")
        driver.find_elements(By.XPATH, '//button[contains(@class, "styles__Button-sc-1j31hgz-0")]')[i].click()
    time.sleep(2)
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        stop_phrase = []
        stop_phrase = driver.find_element(By.XPATH, '//div[contains(@class, "react-swipeable-view-container")]').get_attribute('innerHTML')
        if new_height == last_height:
            if stop_phrases[0] in stop_phrase or stop_phrases[1] in stop_phrase or stop_phrases[2] in stop_phrase:
                break
            else:
                driver.find_elements(By.XPATH, '//button[contains(@class, "styles__Button-sc-1qlvqus-0 PvBJt styles__Base-c2rton-0 idcxql")]')[i].click()
        last_height = new_height

    logging.info(f'---- PEGANDO URL DAS IMAGENS: {fases[i]} ----')
    time.sleep(2)
    imgURLS[fases[i]] = []
    imgResults = driver.find_elements(By.XPATH, '//img[contains(@src,"RESIDENCIAL_CASONI")]')
    for img in imgResults:
        imgURLS[fases[i]].append(img.get_attribute('src'))
    time.sleep(2)

    logging.info(f'---- BAIXANDO IMAGENS: {fases[i]} ----')
    for url in imgURLS[fases[i]]:
        filename = url.split("/")[-1]
        file_path = f'./pictures/{fases[i]}/{filename}'

        if os.path.exists(file_path):
            logging.info(f'IMAGEM "{filename}" JÁ EXISTE!')
        else:
            logging.info(f'BAIXANDO "{filename}"...')
            response = requests.get(url, stream=True)
            with open(f'{file_path}', 'wb') as handle:
                handle.write(response.content)

logging.info('---- FINALIZADO! ----')
