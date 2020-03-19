import requests
import shutil
from staticmap import *
import os
from PIL import Image,ImageDraw,ImageFont
from staticmap import StaticMap, CircleMarker
import pyodbc
from datetime import datetime

cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=SERVER;UID=USER;DATABASE=ODB;Trusted_Connection=yes')
cursor = cnxn.cursor()
key = 'KEY'

timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p")
directory_name = datetime.now().strftime("%Y%m%H%M")

os.makedirs('K:\\ZZZZ - OBJ Liberty Lake\\projects\\CurrentProjects\\12_Leonatus\\mxd\\'+directory_name)
load_directory ='K:\\ZZZZ - OBJ Liberty Lake\\projects\\CurrentProjects\\12_Leonatus\\mxd\\'+directory_name

print('Gather Traffic Report--be patient')
with open('K:\\ZZZZ - OBJ Liberty Lake\\projects\\CurrentProjects\\12_Leonatus\\data\\placelocations.sql') as load_places:
    cursor.execute(load_places.read())
    dataFeed = cursor.fetchall()
    counter = 0
    for each in dataFeed:
        latitude_value = each[0]
        longitude_value = each[1]
        place_name = str(each[2])


##        imgholder = Image.new('RGBA', (400,400))
##        imgholder.save(load_directory+'\\img.png')
        
        url = 'https://www.mapquestapi.com/traffic/v2/flow?key='+key+'&mapLat='+str(latitude_value)+'&mapLng='+str(longitude_value)+'&mapHeight=400&mapWidth=400&mapScale=13541'
        response = requests.get(url,stream=True)
        with open(load_directory+'\\img0.png','wb') as out_map:
            shutil.copyfileobj(response.raw,out_map)
        del response

        strHeader = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        m = StaticMap(400,400,url_template='http://a.tile.osm.org/{z}/{x}/{y}.png',headers=strHeader)
        marker_outline = CircleMarker((float(longitude_value),float(latitude_value)), 'white', 18)
        icon_flag = IconMarker((float(longitude_value),float(latitude_value)), 'K:\\ZZZZ - OBJ Liberty Lake\\projects\\CurrentProjects\\12_Leonatus\\data\\optum_map_point.png', 18, 18)
        m.add_marker(icon_flag)
        m.add_marker(marker_outline)


        image = m.render(zoom=15)
        image.save(load_directory+'\\base_'+place_name.replace(' ','')+'.png')

        background = Image.open(load_directory+'\\base_'+place_name.replace(' ','')+'.png').convert('RGBA')
        foreground = Image.open(load_directory+'\\img0.png').convert('RGBA')

        ok = Image.alpha_composite(background, foreground)
        ok.save(load_directory+'\\out_'+place_name.replace(' ','')+'.png')


        map_img = Image.open(load_directory+'\\out_'+place_name.replace(' ','')+'.png')
        markup = ImageDraw.Draw(map_img)
        print_font = ImageFont.truetype("arial.ttf", 17)

        markup.rectangle(((400, 20), (160, 0)), fill=(252,119,34,64))

        markup.text((200, 0),place_name,fill=(252,119,34,255),font=print_font)
        markup.text((0,380),timestamp,fill=(45,45,45,128),font=print_font)

        map_img.save(load_directory+'\\results_'+place_name.replace(' ','')+'.png')
        counter += 1

