from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

import datetime
from datetime import date, timedelta
from dateutil.parser import parse
import sys
import os
import requests
import warnings

warnings.filterwarnings("ignore")

class ActionWeather(Action):
	
	def name(self):
		return 'action_weather'

	def validate_date(self,date_text,fuzzy=False):
		try: 
			parse(date_text, fuzzy=fuzzy)
			return True
		except ValueError:
			return False
		
	def run(self, dispatcher, tracker, domain):
		from apixu.client import ApixuClient
		
		today = date.today()
		api_key = 'c15bb4ce62c89adc52a2832a5fb72fd2' #your apixu key
		loc = tracker.get_slot('location') #obtain location slot
		userDate = tracker.get_slot('date') #obtain date slot
		userDate = userDate.split("'")
		userDate = userDate[0]
		
		checkDateFormat = self.validate_date(userDate)
		
		if(checkDateFormat):
			reqDate = datetime.datetime.strptime(userDate, "%d-%m-%Y").strftime("%Y-%m-%d")
		else:
			strToDate = today
			preposition = 'is'
			if userDate == "yesterday" :
				strToDate = strToDate - timedelta(days=1)
				preposition = 'was'
			elif userDate == "tomorrow":
				strToDate = strToDate + timedelta(days=1)
				preposition = 'would be'
			elif userDate == "day after tomorrow":
				strToDate = strToDate + timedelta(days=2)
				preposition = 'would be'
			elif userDate == "day before yesterday":
				strToDate = strToDate - timedelta(days=2)
				preposition = 'was'
			
			reqDate = strToDate.strftime("%Y-%m-%d")
		
		
		#client = ApixuClient(api_key)
		#current = client.current(q=loc)
		
		if reqDate != today.strftime("%Y-%m-%d"):
			api_address='http://api.weatherstack.com/historical?access_key={}&query={}&historical_date={}'.format(api_key,loc,reqDate) #for json data		
		else:
			api_address='http://api.weatherstack.com/current?access_key={}&query={}&historical_date={}'.format(api_key,loc,reqDate) #for json data		
		
		current = requests.get(api_address).json()
		
		if "success" in current and current['success'] == False:
			response = current['error']['info']
		else:
			country = current['location']['country']
			city = current['location']['name']
			condition = current['current']['weather_descriptions'][0]
			temperature_c = current['current']['temperature']
			humidity = current['current']['humidity']
			wind_mph = current['current']['wind_speed']
			
			response = """The weather {} {} on {} in {} . The temperature is {} degrees,
						 the humidity is {}% and wind speeed is {} mph. """.format(preposition,condition, reqDate, city, temperature_c, humidity, wind_mph)
		
		dispatcher.utter_message(response)
		return [SlotSet('location',''), SlotSet('date','')] 

