#cowin district calender
# Cowin api

import requests
from datetime import datetime
import time
from os import environ

bot_token=environ['BOT_TOKEN']
group_id=[i for i in environ['GROUP_ID'].split(",")]
district_id=[int(i) for i in environ['DISTRICT_ID'].split(",")]
pincode=[int(i) for i in environ['PINCODE'].split(",")]

oldmsg=[]
cowin_base_url= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now=datetime.now()
today_date=now.strftime("%d-%m-%Y")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
api_url_telegram = "https://api.telegram.org/bot"+bot_token+"/sendMessage?chat_id={chat_id}&text="
google_maps_api="https://www.google.com/maps/search/?api=1%26amp;query="

def fetch_data_from_cowin(district_id):
	query_params="?district_id={}&date={}".format(district_id,today_date)
	final_url=cowin_base_url+query_params
	response=requests.get(final_url, headers=headers)
	#print(response.text,final_url)
	extract_availabilty_data(response)

def extract_availabilty_data(response):
	response_json=response.json()
	for center in response_json["centers"]:
		if center["pincode"]==pincode[district_id.index(dist)] or pincode[district_id.index(dist)]==0:
			for session in center["sessions"]:
				if session["available_capacity"]>0:
					final_map_url=google_maps_api+(str(center["name"])+" "+str(center["address"])).replace(' ','+')
					message="Center name: {}\nPincode: {}\nDate: {}\nVaccine: {}\nSlots: {}\nAge limit: {}".format(
						'['+center["name"]+' '+center["address"]+']('+final_map_url+')',center["pincode"],session["date"],session["vaccine"],session["available_capacity"],session["min_age_limit"])
					if center["fee_type"]=="Paid":
						for fee in center["vaccine_fees"]:
							if session["vaccine"]==fee["vaccine"]:
								message+="\nCost: {}".format('₹'+fee["fee"])
					message+="&parse_mode=Markdown&disable_web_page_preview=True"
					if message not in oldmsg:
						oldmsg.append(message)
						print(message+'\n'+group_id[district_id.index(dist)])
						send_message_telegram(message)
						time.sleep(1)

def send_message_telegram(message):
	final_telegram_url=api_url_telegram.replace("{chat_id}",group_id[district_id.index(dist)])
	final_telegram_url=final_telegram_url+message;
	response=requests.get(final_telegram_url)
	print(response)

if __name__=="__main__":
	while(1==1):
		for dist in district_id:	
			fetch_data_from_cowin(dist)
		time.sleep(300)
