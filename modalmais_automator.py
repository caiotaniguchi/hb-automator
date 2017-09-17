import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from home_broker_automator import HomeBrokerAutomator


class ModalmaisAutomator(HomeBrokerAutomator):
    def __init__(self):
        super().__init__('modalmais')

    def _select_stock(self, tab, stock):
        if tab == 'order':
            self.driver.find_element_by_id('menuItemOrdemNormal-or1').click()
        elif tab == 'stop':
            self.driver.find_element_by_id('menuItemStop-or1').click()
        self._input_text_in_element_by_id('txtBoxPapel-or1', stock)\
            .send_keys(Keys.TAB)
        sleep(2)
        if not self.driver.find_element_by_id('lblNomeEmpPapel-or1').text:
            raise ValueError("O papel selecionado não existe")

    def _input_formatted_price(self, elem_id, price):
        self._input_text_in_element_by_id(elem_id, '{:.2f}'.format(price))
        sleep(1)

    def _assert_price_in_alert_box(self, alert_box_text, field_name, price):
        assert re.search(field_name + r': (\d+\.\d+)', alert_box_text)\
                 .group(1) == "{0:.2f}".format(price)

    def _confirm_stop_order(
        self, stock, good_until, quantity,
        stop_loss_trigger, stop_loss_price,
        stop_gain_trigger, stop_gain_price
    ):
        alert_box_text = self.driver.find_element_by_id('MB_p').text
        alert_box_text = alert_box_text.replace('.', '').replace(',', '.')
        assert 'Enviar ordem de [VENDA]?' in alert_box_text
        assert stock in alert_box_text
        assert good_until.strftime('%d/%m/%Y') in alert_box_text
        assert re.search(r'Quantidade: (\d+)', alert_box_text)\
                 .group(1) == str(quantity)
        self._assert_price_in_alert_box(
            alert_box_text, 'Disparo Loss', stop_loss_trigger)
        self._assert_price_in_alert_box(
            alert_box_text, 'Limite Loss', stop_loss_price)
        self._assert_price_in_alert_box(
            alert_box_text, 'Disparo Gain', stop_gain_trigger)
        self._assert_price_in_alert_box(
            alert_box_text, 'Limite Gain', stop_gain_price)
        self.driver.find_element_by_id('mb-button-yes').click()

    def _confirm_buy_order(self, stock, max_price, max_price_total, quantity):
        alert_box_text = self.driver.find_element_by_id('MB_p').text
        alert_box_text = alert_box_text.replace('.', '').replace(',', '.')
        assert 'Enviar ordem de [COMPRA]?' in alert_box_text
        assert stock in alert_box_text
        assert re.search(r'Quantidade: (\d+)', alert_box_text)\
                 .group(1) == str(quantity)
        assert float(
            re.search(r'Preço: (\d+\.\d+)', alert_box_text).group(1)
            ) <= max_price
        assert float(
            re.search(r'Valor: (\d+\.\d+)', alert_box_text).group(1)
            ) <= max_price_total
        self.driver.find_element_by_id('mb-button-yes').click()

    def enter_broker(self):
        print("Carregando página de login...")
        self.driver.get(self.url)
        self._input_text_in_element_by_id('txt-login', self.username)
        self._input_text_in_element_by_id('txt-senha', self.password)
        self.driver.find_element_by_id('btn-login').click()
        sleep(2)
        print("Usuário logado")
        print("Carregando home broker...")
        self.driver.find_element_by_xpath('//button[@href="/Bolsa/Home"]')\
            .click()
        self.driver.find_element_by_link_text('Acessar').click()
        sleep(2)
        self.driver.get(self.properties['broker_url'])
        print("Home broker carregado")

    def send_buy_order(self, stock, max_price, max_price_total):
        print("Iniciando ordem de compra...")
        self._select_stock('order', stock)
        cur_price = float(
            self.driver.find_element_by_id('spanUltNeg-or1').text
                .replace(',', '.')
        )
        if cur_price > max_price:
            raise ValueError(
                "O valor de negociação é maior do que o máximo estipulado")
        if cur_price * 100 > max_price_total:
            raise ValueError(
                "O lote mínimo é mais caro do que o limite estipulado")

        order_price = cur_price + 0.01
        quantity = int((max_price_total // (order_price * 100)) * 100)

        self._input_text_in_element_by_id('txtBoxQtde-or1', str(quantity))
        self._input_formatted_price('txtBoxPreco-or1', order_price)
        self._input_text_in_element_by_id(
            'txtBoxAssDigital-or1', self.signature)
        self.driver.find_element_by_id('btnCompra-or1').click()
        sleep(1)
        self._confirm_buy_order(stock, max_price, max_price_total, quantity)
        print("Ordem concluída")

    def send_stop_order(
        self, stock, good_until, quantity,
        stop_loss_trigger, stop_loss_price,
        stop_gain_trigger, stop_gain_price
    ):
        print("Iniciando ordem de stop...")
        self._select_stock('stop', stock)
        self._input_text_in_element_by_id(
            'txtBoxValidade-or1', good_until.strftime('%d%m%Y'))
        self._input_text_in_element_by_id('txtBoxQtde-or1', str(quantity))
        prices_to_fill = [
            ('txtBoxPrecoDispLoss-or1', stop_loss_trigger),
            ('txtBoxPrecoLimLoss-or1', stop_loss_price),
            ('txtBoxPrecoDispGain-or1', stop_gain_trigger),
            ('txtBoxPrecoLimGain-or1', stop_gain_price)
        ]
        for element in prices_to_fill:
            self._input_formatted_price(element[0], element[1])
        self._input_text_in_element_by_id(
            'txtBoxAssDigital-or1', self.signature)
        self.driver.find_element_by_id('btnVenda-or1').click()
        sleep(1)
        self._confirm_stop_order(
            stock, good_until, quantity,
            stop_loss_trigger, stop_loss_price,
            stop_gain_trigger, stop_gain_price
        )
        print("Ordem concluída")

    def send_stop_order(
        self, stock, good_until, quantity,
        stop_loss_trigger, stop_loss_price,
        stop_gain_trigger, stop_gain_price
    ):
        print("Iniciando ordem de stop...")
        self._select_stock('stop', stock)
        self._input_text_in_element_by_id(
            'txtBoxValidade-or1', good_until.strftime('%d%m%Y'))
        self._input_text_in_element_by_id('txtBoxQtde-or1', str(quantity))
        prices_to_fill = [
            ('txtBoxPrecoDispLoss-or1', stop_loss_trigger),
            ('txtBoxPrecoLimLoss-or1', stop_loss_price),
            ('txtBoxPrecoDispGain-or1', stop_gain_trigger),
            ('txtBoxPrecoLimGain-or1', stop_gain_price)
        ]
        for element in prices_to_fill:
            self._input_formatted_price(element[0], element[1])
        self._input_text_in_element_by_id(
            'txtBoxAssDigital-or1', self.signature)
        self.driver.find_element_by_id('btnVenda-or1').click()
        sleep(1)
        self._confirm_stop_order(
            stock, good_until, quantity,
            stop_loss_trigger, stop_loss_price,
            stop_gain_trigger, stop_gain_price
        )
        print("Ordem concluída")
