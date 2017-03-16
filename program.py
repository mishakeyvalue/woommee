import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import platform
import logging
import pymorphy2
logging.basicConfig(filename='main.log', level = logging.INFO,
   format = '%(asctime)s : %(levelname)s : %(message)s')

import mi_weather as we

with open('config.json') as json_data_file:
    config = dict(json.load(json_data_file))    
_login = config['login']
_password = config['pass']
_my_id = '80314023'
morph = pymorphy2.MorphAnalyzer()
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
                            w = we.get_weather(morph.normal_forms(word)[0])
                            answer =str("Погода в {3} на {4}\nТемпература от {0} до {1}. {2}\nВосход: {5}\nЗакат:{6}".format(w['min_t'], w['max_t'], w['descr'],morph.parse(w["city"])[0].inflect({"loc2"})[0].title(),w["date"],w["sunrise"],w["sunset"]))
                        except ValueError as err:
                            logging.info('Word isnt a city: ')
                    vk.messages.send(message = answer, user_id = event.user_id)
                if event.from_group:
                        vk.messages.send(message =str(platform.platform()) + "\n" + str(event.text) + str(we.get_weather('Харьков')),user_id = '80314023')
        



if __name__ == "__main__":
    main()