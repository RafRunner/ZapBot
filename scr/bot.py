from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import time


class NumeroNaoEncontrado(Exception):
    pass


class ZapBot:

    __instance = None
    __create_key = object()

    def __init__(self, create_key):
        assert (create_key == ZapBot.__create_key), "ZapBot é um singleton! Para obter a instância chame instance()"

        self._base_url = 'https://web.whatsapp.com/send?phone='
        self._driver = webdriver.Chrome()

    def close(self):
        self._driver.quit()

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls(cls.__create_key)
        return cls.__instance

    def _abrir_conersa_numero(self, numero):
        self._driver.get(self._base_url + numero)
        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'O número de telefone compartilhado através de url é inválido.')]")))
            raise NumeroNaoEncontrado()
        except TimeoutException:
            pass

    # requer que a conversa esteja aberta no número
    def _enviar_mensagem_conversa_aberta(self, mensagem):
        text_box_mensagem = WebDriverWait(self._driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))
        text_box_mensagem.send_keys(mensagem + Keys.ENTER)

    # É necessário esperar um tempo (3s~) após o envio de uma mensagem para enviar para outro número sem problemas
    # TODO arrumar isso e fazer clicar o alert? Acho que de toda forma tem que esperar um pouco
    def enviar_mensagem(self, numero, mensagem):
        if mensagem == '':
            return

        self._abrir_conersa_numero(numero)
        self._enviar_mensagem_conversa_aberta(mensagem)

    def enviar_mensagens(self, numero, mensagens):
        self._abrir_conersa_numero(numero)

        for mensagem in mensagens:
            if mensagem == '':
                continue
            self._enviar_mensagem_conversa_aberta(mensagem)
            time.sleep(1)

