import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newagent-lxugdd"

from gnewsclient import gnewsclient
client = gnewsclient.NewsClient(max_results=3)

import pyowm
owm = pyowm.OWM(os.environ.get('OWM_KEY'))

from pymongo import MongoClient

from apiclient.discovery import build

def get_news(parameters):
    client.topic = parameters.get('news_type')
    client.language = parameters.get('language')
    client.location = parameters.get('geo-country')
    return client.get_news()

def get_weather(param,s_id):
    client = MongoClient("mongodb+srv://test:test@cluster0-rjeed.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('weather_db') 
    records = db.weather_loc

    if not param['geo-city']:
        wstr = param['geo-country']
    elif not param['geo-country']:
        wstr = param['geo-city']
    else:
        wstr = param['geo-city'] + "," + param['geo-country'] 

    observation = owm.weather_at_place(wstr)
    w = observation.get_weather()

    new_loc = {'session_id':s_id, 'location' : wstr }
    records.insert_one(new_loc)
    return w

def custom_search(srch):
    api_key = os.environ.get('CSE_KEY')
    resource = build("customsearch", 'v1', developerKey=api_key).cse()
    result = resource.list(q=srch, cx='006393511391755239890:69obfjl8kuy').execute()
    return result['items'][:min(3,len(result['items']))]

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg,session_id):
    response = detect_intent_from_text(msg,session_id)
    
    if response.intent.display_name == 'get_news':
        news = get_news(dict(response.parameters))
        news_str = "Here is your news:\n"
        news_lst = []
        news_lst.append(news_str)
        for row in news:
            news_lst.append("{}\n\n{}\n\n".format(row['title'],row['link']))
        return news_lst
        
    elif response.intent.display_name == 'get_history':
        client = MongoClient("mongodb+srv://test:test@cluster0-rjeed.mongodb.net/test?retryWrites=true&w=majority")
        db = client.get_database('weather_db') 
        records = db.weather_loc
        ret_str = "Your search history is:\n"
        for rec in list(records.find({'session_id': session_id})):
            ret_str += "\n" + rec['location']
        return ret_str

    elif response.intent.display_name == 'get_temp' :
        try:
            w = get_weather(dict(response.parameters),session_id)
            weather_str = "Here is your weather report:\n It will be {} today.\n\n Current Temp: {}°C, Max Temp: {}°C, Min Temp: {}°C\n\n Wind Degree: {}, Wind Speed: {}m/s\n\n Humidity: {}% ".format(w.get_status(),w.get_temperature('celsius')['temp'],w.get_temperature('celsius')['temp_max'],w.get_temperature('celsius')['temp_min'],w.get_wind()['deg'],w.get_wind()['speed'],w.get_humidity())
            return (weather_str,w.get_weather_icon_url())
        except:
            return "Please enter correct city name."

    elif response.intent.display_name == 'custom_search':
        search_results = custom_search(msg)
        cse_str = "Here are the top {} results:\n".format(len(search_results))
        cse_lst = []
        cse_lst.append(cse_str)
        for row in search_results:
            cse_lst.append("{}\n\n{}\n\n".format(row['title'],row['link']))
        return cse_lst

    else:
        return response.fulfillment_text