from bs4 import BeautifulSoup as bs
import requests
import datetime
import logging
logging.basicConfig(filename='main.log', level = logging.INFO,
   format = '%(asctime)s : %(levelname)s : %(message)s')

_uri = 'https://sinoptik.ua/'

def get_weather(city = 'Киев', date = datetime.date.today()):
    _uri = 'https://sinoptik.ua/погода-{0}/{1}'.format(city.lower(), date)    
    req = requests.get(_uri)
    #+++++++++++++++++++++++++++++++++++
    if req.status_code == 404:
        raise ValueError("No such city")
    #+++++++++++++++++++++++++++++++++++
    soup = bs(requests.get(_uri).text, "html.parser")
    weather = {'city':city, 'date' : date }
    try:   
        w_today = soup.find('div',{'class' : 'main loaded'}) 
        weather['max_t'] = w_today.find('div',{'class': 'max'}).find('span').text 
        weather['min_t'] = w_today.find('div',{'class': 'min'}).find('span').text

        weather['descr'] = soup.findAll('div', {'class': 'description'})[0].text
        weather['sunrise'] = soup.find('div', {'class' : 'infoDaylight'}).findAll('span')[0].text
        weather['sunset'] = soup.find('div', {'class' : 'infoDaylight'}).findAll('span')[1].text

    except Exception as e:
        print(e)
    return weather