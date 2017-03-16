#!/usr/bin/env python3
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import platform
import logging
import pymorphy2

logging.basicConfig(filename='main.log', level = logging.INFO,

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
morph = pymorphy2.MorphAnalyzer()


CHARS_ALLOWED = 'йцукенгшщзхъэждлорпавыфюбьтимсчя'
def clean_word(word):
    for ch in word:
        if ch not in CHARS_ALLOWED:
            word = word.replace(ch, '')
    return word

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
                    msg_text = event.text.lower()
                    answer = 'Если назовешь мне город, то я скажу тебе, какая там погода ^_^'
                    
                    for word in msg_text.split():
                        try:
                            w = we.get_weather(morph.normal_forms(clean_word(word))[0])
                            answer =str("Погода в {3} на {4}\nТемпература от {0} до {1}. {2}\nВосход: {5}\nЗакат:{6}".format(w['min_t'], w['max_t'], w['descr'],morph.parse(w["city"])[0].inflect({"loc2"})[0].title(),w["date"],w["sunrise"],w["sunset"]))
                        except ValueError as err:
                            logging.info('Word isnt a city: ')
                        except Exception as e:
                            logging.info(str(e))
                    vk.messages.send(message = answer, user_id = event.user_id)
                if event.from_group:
                        vk.messages.send(message =str(platform.platform()) + "\n" + str(event.text) + str(we.get_weather('Харьков')),user_id = '80314023')
        



if __name__ == "__main__":
    main()
