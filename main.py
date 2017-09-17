from datetime import date

from modalmais_automator import ModalmaisAutomator

from timeit import default_timer as timer
from time import sleep

# ...
start = timer()
automator = ModalmaisAutomator()
automator.enter_broker()
# automator.send_buy_order('SGPS3', 11.00, 1100)
# sleep(2)
# automator.send_buy_order('VLID3', 17.00, 3340)
# sleep(2)
# automator.send_buy_order('EMBR3', 16.00, 1600)
# sleep(2)

# automator.send_stop_order(
#     'SGPS3', date(2017, 9, 2), 300,
#     8.04, 8.04 - 0.10,
#     155.9, 155.9
#     )
# sleep(2)
# automator.send_stop_order(
#     'EMBR3', date(2017, 9, 2), 300,
#     13.88, 13.88 - 0.10,
#     155.9, 155.9
#     )
# sleep(2)
# automator.send_stop_order(
#     'LAME4', date(2017, 9, 2), 200,
#     13.09, 13.09 - 0.10,
#     155.9, 155.9
#     )
# sleep(2)
automator.send_stop_order(
    'SAPR4', date(2017, 9, 8), 300,
    9.29, 9.29 - 0.10,
    155.9, 155.9
    )
sleep(2)

automator.quit()
# automator.quit()
end = timer()
print(end - start)
