import ctypes
from time import gmtime,strftime
import time
from datetime import date, datetime
from PIL import Image,ImageDraw,ImageFont
import os
import requests
import random
import datetime
import urllib.request
line= [(843,505),(1090,505)]
Days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
font = ImageFont.truetype(r'C:/Users/NAMIT/Downloads/Font/M.ttf',40)
font2 = ImageFont.truetype(r'C:/Users/NAMIT/Downloads/Font/h.ttf',25)
font3 = ImageFont.truetype(r'C:/Users/NAMIT/Downloads/Font/h.ttf',15)
shape = [(1636,63),( 1857,140)]
def last_tempw(t,temprature,weather_id):
    f =open("C:/Users/NAMIT/Downloads/wallpapers/Last_Temp.txt",'w')
    l = [str(t)+"\n",str(temprature)+"\n",str(weather_id)+"\n"]
    f.writelines(l)
    f.close()
    

def last_tempr():
    
 
    with open("C:/Users/NAMIT/Downloads/wallpapers/Last_Temp.txt") as f:
        Lines = f.read().splitlines() 
    return Lines[0],Lines[1],Lines[2]

def get_icon(icon):
    path = "C:/Users/NAMIT/Downloads/wallpapers/Icon/w_icon.png"
    urllib.request.urlretrieve('http://openweathermap.org/img/wn/{}@2x.png'.format(icon),path)
    return path
    

def time_week():
    dt = datetime.datetime.now()
    Week = date.today().weekday()
    Hour = strftime("%H",time.localtime())
    
    t_date = dt.strftime("%d %b %Y")
    return Days[Week],Hour,t_date
    

def Day_Night(hour):
    
    if int(hour)>5 and int(hour)<18:
        return "day"
        
    else:
        return "night"


def weather_api():
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = "Landran"
    API_KEY = "57dcdbe89a2c978c33424e879d98ade3"
    URL = BASE_URL + "q=" + CITY +"&appid=" + API_KEY
    response = requests.get(URL)
    data = response.json()
    weather = data['weather']
    w_id = weather[0]["id"]
    w_icon = weather[0]["icon"]
    main = data['main']
    temp = main['temp']
    t = strftime("%H:%M",time.localtime())
    return round(temp - 273.15),w_id,w_icon,t
    
    


def netcheck():
    try:
        request = requests.get("https://www.google.com/", timeout=10)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False


def wall_change(today,call,weekday):
    t,temprature,weather_id = last_tempr()
    main_path = "C:/Users/NAMIT/Downloads/wallpapers/{}".format(call)
    if 300<= int(weather_id) <623:
        root_path = main_path+"/rain"

    elif 700<int(weather_id)<782:
        root_path = main_path+"/mist"

    elif int(weather_id)>=800:
        root_path = main_path+"/clear"

    elif 200<=int(weather_id)<=232:
        root_path = main_path+"/thunder"
    l = os.listdir(root_path)
    select_wall = random.choice(l)
    wall_path = root_path + "/{}".format(select_wall)
    img = Image.open(wall_path)
    img2 = Image.open(icon_path)
    img2 = img2.resize((round(img2.size[0]*0.5)+10, round(img2.size[1]*0.5)+10))
    I1 = ImageDraw.Draw(img)
    img.paste(img2,(1790,74),img2)
    I1.rectangle(shape,  outline ="white")
    I1.line(line,fill = (255,255,255))
    I1.text((1650,78),str(temprature)+"°C",font = font2 , fill=(255,255,255))
    I1.text((1650,110),"Landran",font = font2 , fill=(255,255,255))
    I1.text((845,455),weekday,font = font , fill=(255,255,255))
    I1.text((845,505),today,font = font , fill=(255,255,255))
    I1.text((1680,150),"Last Updated at "+t,font = font3 ,fill=(255,255,255))
    img.save(root_path+"/2{}".format(select_wall))
    ctypes.windll.user32.SystemParametersInfoW(20, 0, root_path+"/2{}".format(select_wall) , 3)
    os.remove(root_path+"/2{}".format(select_wall))
    if flag != 0:
        os.remove(icon_path)
        


    

    


while True:
    icon_path = "C:/Users/NAMIT/Downloads/wallpapers/Icon/default.png" # Default Icon Path
    flag =0
    if netcheck() == True:
        temprature,weather_id,icon,t = weather_api()
        last_tempw(t,temprature,weather_id)
        icon_path = get_icon(icon)
        flag = 1
    weekday , hour,today = time_week()
    call = Day_Night(hour)
    wall_change(today,call,weekday)
    time.sleep(600)



        
    
