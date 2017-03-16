#!/usr/bin/env python3
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import platform
import logging
logging.basicConfig(filename='/main.log', level = logging.INFO,
   format = '%(asctime)s : %(levelname)s : %(message)s')

import mi_weather as we
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "config.json"
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path) as json_data_file:
    config = dict(json.load(json_data_file))    
_login = config['login']
_password = config['pass']
_my_id = '80314023'

def main():
    

    vk_session = vk_api.VkApi(login=_login, password = _password)

    vk_session.authorization()
    vk= vk_session.get_api()


    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():

            if event.to_me:
                if event.from_user:
                    logging.info(event)
                    #user = vk.users.get(user_ids = event.user_id)
                    try:
                        w = we.get_weather(event.text.lower())
                        msg =str("Погода в {3} на {4}\nТемпература от {0} до {1}. {2}\nВосход: {5}\nЗакат:{6}".format(w['min_t'], w['max_t'], w['descr'],w["city"],w["date"],w["sunrise"],w["sunset"]))
                    except ValueError as err:
                        #w = we.get_weather()
                        #msg =str(str("Погода в {3} на {4}\nТемпература от {0} до {1}. {2}\nВосход: {5}\nЗакат:{6}".format(w['min_t'], w['max_t'], w['descr'],w["city"],w["date"],w["sunrise"],w["sunset"]))                       
                        msg = 'Нет такого города =( Скажи мне название, а я скажу тебе погоду.'

                    vk.messages.send(message = msg, user_id = event.user_id)
                if event.from_group:
                        vk.messages.send(message =str(platform.platform()) + "\n" + str(event.text) + str(we.get_weather('Харьков')),user_id = '80314023')
        



if __name__ == "__main__":
    main()
