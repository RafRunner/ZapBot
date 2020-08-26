from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import pyautogui
import os
import imghdr
import time


class NumeroNaoEncontrado(Exception):
    pass


class ZapBot:

    __instance = None
    __create_key = object()

    def __init__(self, create_key):
        assert (create_key == ZapBot.__create_key), 'ZapBot é um singleton! Para obter a instância chame instance()'

        self._base_url = 'https://web.whatsapp.com/send?phone='
        self._driver = webdriver.Chrome()

    def close(self):
        self._driver.quit()

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls(cls.__create_key)
        return cls.__instance

    def _get_element_by_xpath(self, xpath, wait_time=10):
        return WebDriverWait(self._driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def _abrir_conersa_numero(self, numero):
        self._driver.get(self._base_url + numero)
        try:
            self._get_element_by_xpath(
                "//*[contains(text(), 'O número de telefone compartilhado através de url é inválido.')]")
            raise NumeroNaoEncontrado()
        except TimeoutException:
            pass

    # requer que a conversa esteja aberta no número
    def _enviar_mensagem_conversa_aberta(self, text_box_mensagem, mensagem):
        if mensagem == '':
            return

        # É um arquivo
        if os.path.exists(mensagem):
            self._get_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div').click()
            time.sleep(1)

            xpath_botao_correto = '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button'

            # É uma imagem
            if imghdr.what(mensagem):
                xpath_botao_correto = '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button'

            self._get_element_by_xpath(xpath_botao_correto).click()
            time.sleep(1)

            pyautogui.write(mensagem)
            pyautogui.press('enter', 1, 1)

            self._get_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div').click()

        else:
            text_box_mensagem.send_keys(mensagem + Keys.ENTER)

        time.sleep(2)

    # É necessário esperar um tempo (2s~) após o envio de uma mensagem para enviar para outro número sem problemas
    # TODO arrumar isso e fazer clicar o alert? Acho que de toda forma tem que esperar um pouco
    def enviar_mensagens(self, numero, mensagens):
        self._abrir_conersa_numero(numero)

        text_box_mensagem = self._get_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

        for mensagem in mensagens:
            self._enviar_mensagem_conversa_aberta(text_box_mensagem, mensagem)
