#cowin district calender
# Cowin api

import requests
from datetime import datetime
import time
from os import environ

bot_token=environ['bot_token']
group_id=environ['group_id']
district_id=environ['district_id']
pincode=environ['pincode']


cowin_base_url= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now=datetime.now()
today_date=now.strftime("%d-%m-%Y")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
api_url_telegram = "https://api.telegram.org/bot"+bot_token+"/sendMessage?chat_id={chat_id}&text="

def fetch_data_from_cowin(district_id):
	query_params="?district_id={}&date={}".format(district_id,today_date)
	final_url=cowin_base_url+query_params
	response=requests.get(final_url, headers=headers)
	#print(response.text,final_url)
	extract_availabilty_data(response)

def extract_availabilty_data(response):
	response_json=response.json()
	for center in response_json["centers"]:
		if center["pincode"]==pincode:
			for session in center["sessions"]:
				if session["available_capacity_dose1"]>0 and session["min_age_limit"]==18:
					message="Center id: {}\nCenter name: {}\nDate: {}\nVaccine: {}\nSlots: {}\nAge limit: {}".format(center["center_id"],
						center["name"],session["date"],session["vaccine"],session["available_capacity"],session["min_age_limit"])
					send_message_telegram(message)

def send_message_telegram(message):
	final_telegram_url=api_url_telegram.replace("{chat_id}",group_id)
	final_telegram_url=final_telegram_url+message;
	response=requests.get(final_telegram_url)
	print(response)

if __name__=="__main__":
	while(1==1):
		fetch_data_from_cowin(district_id)
		time.sleep(300)