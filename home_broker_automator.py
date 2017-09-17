import yaml
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from abc import ABC, abstractmethod
from selenium.webdriver.chrome.options import Options


class HomeBrokerAutomator(ABC):
    def __init__(self, broker_name):
        # Load broker configuration
        broker_list = yaml.safe_load(open('config.yaml'))['broker']
        broker = [b for b in broker_list if b.get('name') == broker_name]
        if len(broker) == 0:
            raise ValueError("O broker selecionado não existe")
        # Load broker credentials
        broker_list = yaml.safe_load(open('credentials.yaml'))['broker']
        broker_credentials = [
            b for b in broker_list if b.get('name') == broker_name]
        if len(broker_credentials) == 0:
            raise ValueError(
                "Não existem credenciais para o broker selecionado")

        # Initialize Chrome browser
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=1200x600")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.name = broker_name
        self.url = broker[0]['url']
        self.properties = broker[0]['properties']
        self.username = broker_credentials[0]['username']
        self.password = broker_credentials[0]['password']
        self.signature = broker_credentials[0]['signature']

    def _input_text_in_element_by_id(self, id, text):
        elem = self.driver.find_element_by_id(id)
        elem.clear()
        elem.send_keys(text)
        sleep(1)
        return elem

    @abstractmethod
    def enter_broker(self):
        pass

    @abstractmethod
    def send_buy_order(self, stock, max_price, max_price_total):
        pass

    @abstractmethod
    def send_stop_order(
        self, stock, good_until, quantity,
        stop_loss_trigger, stop_loss_price,
        stop_gain_trigger, stop_gain_price
    ):
        pass

    def quit(self):
        self.driver.quit()
