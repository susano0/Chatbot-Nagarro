# Chatbot-Nagarro

This chatbot was made as an assignment during Nagarro Bootcamp Program(2019).

The chatbot was built mainly with the help of Flask, DialogFlow and Twilio.

It has 4 Dialogflow Intents, namely `get_news`,`get_temp`,`get_history` and `custom_search`.

The `get_news` intent with the help of `gnewsclient` is used to get news from various categories and locations. Example: type: 'Sports news from the UK', the chatbot will display the top 3 news results in separate messages with there heading and URL. 

The `get_temp` intent and a python wrapper `pyowm` for  OpenWeatherMap (OWM) are used to get the weather forecast for any location at the city level. The search history of a user is saved in a NoSQL database using MongoDB. Example: type 'Climate in London' or 'temp in New Delhi', the chatbot will show a summarised weather report.

The `get_history` intent and MongoDB are used to get the search weather history of a user. Example: type
'Show me my weather history' chatbot will retrieve the data from the database for that particular user.

The `custom_search` intent and Google Custom Search API are used to fetch results from Quora and GeeksForGeeks and display the top 3 hits. Example: 'Search breaking bad on Quora' or 'shortest path algorithm of gfg', the chatbot will display the title and the URL in 3 separate messages.

## Hosted on Heroku: http://utk-chatbot.herokuapp.com/

## To initiate a conversation with the bot: 

Send a WhatsApp message to `+1(415)523-8886` with code `join hot-among`.



