import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json

with open('config.json') as json_data_file:
    config = dict(json.load(json_data_file))    
_login = config['login']
_password = config['pass']
_my_id = '80314023'

def main():
    
    play()
    vk_session = vk_api.VkApi(login=_login, password = _password)

    vk_session.authorization()
    vk= vk_session.get_api()


    longpoll = VkLongPoll(vk_session)


def play():
    import mi_weather as we

    while True:

        c = input("Weather to show: ")
        if c is "":
            print(we.get_weather())
            continue
        print(we.get_weather(c))
    



if __name__ == "__main__":
    main()