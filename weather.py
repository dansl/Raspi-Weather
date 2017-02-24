import pygame
import urllib2
import json
import os
import sys
from datetime import datetime

#Text Colors
WHITE = (255,255,255)
LIGHT_GRAY = (160,160,160)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
ORANGE = (255,160,0)

#Text Size
XXLARGE_FONT = 35
XLARGE_FONT = 30
LARGE_FONT = 25
MEDIUM_FONT = 20
SMALL_FONT = 15

HOTSPOT_FILLING = (255,255,255,0)

Weather_JSON = {}

## This is for the piTFT screen
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
#######

#Init PyGame
pygame.init()
pygame.mixer.init()

#Get Display Info
#infoObject = pygame.display.Info() 
#MAIN_LCD_width = infoObject.current_w
#MAIN_LCD_height = infoObject.current_h
MAIN_LCD_width = 320 #320x240
MAIN_LCD_height = 240
MAIN_LCD_rect = (MAIN_LCD_width, MAIN_LCD_height)
MAIN_LCD = pygame.display.set_mode(MAIN_LCD_rect)

#Init Background Image
bg = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+"/bg2.jpg").convert()
bg = pygame.transform.scale(bg, (MAIN_LCD_width, MAIN_LCD_height))

icon_root = "/png/256x256/"
#chanceflurries = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"chanceflurries.png").convert_alpha()
#chancerain = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"chancerain.png").convert_alpha()
#chancesleet = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"chancesleet.png").convert_alpha()
#chancesnow = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"chancesnow.png").convert_alpha()
#chancetstorms = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"chancetstorms.png").convert_alpha()
#clear = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"clear.png").convert_alpha()
#cloudy = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"cloudy.png").convert_alpha()
#flurries = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"flurries.png").convert_alpha()
#fog = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"fog.png").convert_alpha()
#hazy = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"hazy.png").convert_alpha()
#mostlycloudy = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"mostlycloudy.png").convert_alpha()
#mostlysunny = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"mostlysunny.png").convert_alpha()
#partlycloudy = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"partlycloudy.png").convert_alpha()
#partlysunny = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"partlysunny.png").convert_alpha()
#rain = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"rain.png").convert_alpha()
#sleet = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"sleet.png").convert_alpha()
#snow = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"snow.png").convert_alpha()
#sunny = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"sunny.png").convert_alpha()
#tstorms = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"tstorms.png").convert_alpha()
#unknown = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+"unknown.png").convert_alpha()

#Init Black out the screen
bgBlackout = pygame.Surface((MAIN_LCD_width,MAIN_LCD_height))
bgBlackout.set_alpha(128)           
bgBlackout.fill((0,0,0))

#Simplified call for drawing text on the screen
def DrawText(surface, text, color, position, font_size, max_width = None):
	newFont = pygame.font.SysFont("Nimbus Sans", font_size)
	fontHeight = newFont.size("Tg")[1]
	newText = newFont.render(str(text), True, color)
	lineSpacing = -2

	newText_rect = newText.get_rect()

	centering_width = newText_rect.width
	if position[3] == "center" and max_width != None:
		centering_width = max_width

	if position[0] != None:
		if position[0] == "center":
			newText_rect.top = (MAIN_LCD_height / 2) - (newText_rect.height / 2)
		else:
			newText_rect.top = position[0]
	if position[1] != None:
			newText_rect.right = MAIN_LCD_width-position[1]
	if position[2] != None:
			newText_rect.bottom = MAIN_LCD_height-position[2]
	if position[3] != None:
		if position[3] == "center":
			newText_rect.left = (MAIN_LCD_width / 2) - (centering_width / 2)
		else:
			newText_rect.left = position[3]

	#Wrap text
	if max_width != None:
		temp_y = newText_rect.top
		while text:
			i = 1

			# determine maximum width of line
			while newFont.size(text[:i])[0] < max_width and i < len(text):
				i += 1

			# if we've wrapped the text, then adjust the wrap to the last word      
			if i < len(text): 
				i = text.rfind(" ", 0, i) + 1

			# render the line and blit it to the surface
			image = newFont.render(text[:i], False, color)

			surface.blit(image, (newText_rect.left, temp_y))
			temp_y += fontHeight + lineSpacing

			# remove the text we just blitted
			text = text[i:]
	else:
		surface.blit(newText, newText_rect)

#Simplified call for drawying images on the screen
def DrawImage(surface, image, position, scale):
	newImage = pygame.transform.scale(image, scale)

	newImage_rect = newImage.get_rect()
	if position[0] != None:
		if position[0] == "center":
			newImage_rect.top = (MAIN_LCD_height / 2) - (newImage_rect.height / 2)
		else:
			newImage_rect.top = position[0]
	if position[1] != None:
		newImage_rect.right = MAIN_LCD_width-position[1]
	if position[2] != None:
		newImage_rect.bottom = MAIN_LCD_height-position[2]
	if position[3] != None:
		if position[3] == "center":
			newImage_rect.left = (MAIN_LCD_width / 2) - (newImage_rect.width / 2)
		else:
			newImage_rect.left = position[3]

	return surface.blit(newImage, newImage_rect)

def DrawBackground():
	MAIN_LCD.blit(bg, bg.get_rect())
	MAIN_LCD.blit(bgBlackout, (0,0))

def UpdateWeatherJSON():
	wunder_key = "aecd1d9781943a6e"
	weather_link = 'https://api.wunderground.com/api/'+wunder_key+'/forecast/q/KS/Mission.json'

	parsed_json = {}
	# Use Web
	# try:
	# 	f = urllib2.urlopen(weather_link)
	# 	json_string = f.read()
	# 	parsed_json = json.loads(json_string)
	# 	f.close()
	# except Exception as excpt:
	# 	print("oops somthin broke")
	#######

	# Use Local file
	with open(os.path.dirname(os.path.abspath(__file__))+'/test.json') as data_file:
		parsed_json = json.loads(data_file.read())
	#######

	return parsed_json

def DrawTime():
	cur_date = datetime.now()
	format_time = cur_date.strftime("%I:%M%p")
	format_date = cur_date.strftime("%a %b %m")
	DrawText(MAIN_LCD, format_time, WHITE, [5, None, None, 5], XXLARGE_FONT)
	DrawText(MAIN_LCD, format_date, WHITE, [5, 5, None, None], XXLARGE_FONT)

def Draw4DayForcast():
	global Day1Button
	global Day2Button
	global Day3Button
	global Day4Button

	if Weather_JSON != None and len(Weather_JSON) > 0:
		JSON_root = Weather_JSON['forecast']
		
		#######
		#day = JSON_root['txt_forecast']['forecastday'][0]['title']
		#forcast_day = JSON_root['txt_forecast']['forecastday'][0]['fcttext']
		#forcast_night = JSON_root['txt_forecast']['forecastday'][1]['fcttext']
		conditions = JSON_root['simpleforecast']['forecastday'][0]['conditions']
		high = JSON_root['simpleforecast']['forecastday'][0]['high']['fahrenheit']
		low = JSON_root['simpleforecast']['forecastday'][0]['low']['fahrenheit']
		iconName = JSON_root['simpleforecast']['forecastday'][0]['icon']

		weatherIcon = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+iconName+".png").convert_alpha()
		DrawImage(MAIN_LCD, weatherIcon, [50, None, None, 10], (40,40))

		DrawText(MAIN_LCD, "Today  "+high+"* / "+low+"*", WHITE, [50, None, None, 60], XLARGE_FONT)
		DrawText(MAIN_LCD, conditions, LIGHT_GRAY, [70, None, None, 60], XLARGE_FONT)
		#DrawText(MAIN_LCD, "Day: "+forcast_day, WHITE, [25, None, None, 50], MEDIUM_FONT)
		#DrawText(MAIN_LCD, "Night: "+forcast_night, WHITE, [38, None, None, 50], MEDIUM_FONT)

		button = pygame.Surface((MAIN_LCD_width,40), pygame.SRCALPHA)
		button.fill(HOTSPOT_FILLING)
		Day1Button = MAIN_LCD.blit(button, (0,50))
		
		#######

		day = JSON_root['txt_forecast']['forecastday'][2]['title']
		#forcast_day = JSON_root['txt_forecast']['forecastday'][2]['fcttext']
		#forcast_night = JSON_root['txt_forecast']['forecastday'][3]['fcttext']
		conditions = JSON_root['simpleforecast']['forecastday'][1]['conditions']
		high = JSON_root['simpleforecast']['forecastday'][1]['high']['fahrenheit']
		low = JSON_root['simpleforecast']['forecastday'][1]['low']['fahrenheit']
		iconName = JSON_root['simpleforecast']['forecastday'][1]['icon']

		weatherIcon = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+iconName+".png").convert_alpha()
		DrawImage(MAIN_LCD, weatherIcon, [95, None, None, 10], (40,40))

		DrawText(MAIN_LCD, day+"  "+high+"* / "+low+"*", WHITE, [95, None, None, 60], XLARGE_FONT)
		DrawText(MAIN_LCD, conditions, LIGHT_GRAY, [115, None, None, 60], XLARGE_FONT)
		#DrawText(MAIN_LCD, "Day: "+forcast_day, WHITE, [80, None, None, 50], MEDIUM_FONT)
		#DrawText(MAIN_LCD, "Night: "+forcast_night, WHITE, [93, None, None, 50], MEDIUM_FONT)

		button = pygame.Surface((MAIN_LCD_width,40), pygame.SRCALPHA)
		button.fill(HOTSPOT_FILLING)
		Day2Button = MAIN_LCD.blit(button, (0,95))

		#######

		day = JSON_root['txt_forecast']['forecastday'][4]['title']
		#forcast_day = JSON_root['txt_forecast']['forecastday'][4]['fcttext']
		#forcast_night = JSON_root['txt_forecast']['forecastday'][5]['fcttext']
		conditions = JSON_root['simpleforecast']['forecastday'][2]['conditions']
		high = JSON_root['simpleforecast']['forecastday'][2]['high']['fahrenheit']
		low = JSON_root['simpleforecast']['forecastday'][2]['low']['fahrenheit']
		iconName = JSON_root['simpleforecast']['forecastday'][2]['icon']

		weatherIcon = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+iconName+".png").convert_alpha()
		DrawImage(MAIN_LCD, weatherIcon, [140, None, None, 10], (40,40))

		DrawText(MAIN_LCD, day + "  "+high+"* / "+low+"*", WHITE, [140, None, None, 60], XLARGE_FONT)
		DrawText(MAIN_LCD, conditions, LIGHT_GRAY, [160, None, None, 60], XLARGE_FONT)
		#DrawText(MAIN_LCD, "Day: "+forcast_day, WHITE, [135, None, None, 50], MEDIUM_FONT)
		#DrawText(MAIN_LCD, "Night: "+forcast_night, WHITE, [148, None, None, 50], MEDIUM_FONT)

		button = pygame.Surface((MAIN_LCD_width,40), pygame.SRCALPHA)
		button.fill(HOTSPOT_FILLING)
		Day3Button = MAIN_LCD.blit(button, (0,140))
		#######

		day = JSON_root['txt_forecast']['forecastday'][6]['title']
		#forcast_day = JSON_root['txt_forecast']['forecastday'][6]['fcttext']
		#forcast_night = JSON_root['txt_forecast']['forecastday'][7]['fcttext']
		conditions = JSON_root['simpleforecast']['forecastday'][3]['conditions']
		high = JSON_root['simpleforecast']['forecastday'][3]['high']['fahrenheit']
		low = JSON_root['simpleforecast']['forecastday'][3]['low']['fahrenheit']
		iconName = JSON_root['simpleforecast']['forecastday'][3]['icon']

		weatherIcon = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+iconName+".png").convert_alpha()
		DrawImage(MAIN_LCD, weatherIcon, [185, None, None, 10], (40,40))

		DrawText(MAIN_LCD, day + "  "+high+"* / "+low+"*", WHITE, [185, None, None, 60], XLARGE_FONT)
		DrawText(MAIN_LCD, conditions, LIGHT_GRAY, [205, None, None, 60], XLARGE_FONT)
		#DrawText(MAIN_LCD, "Day: "+forcast_day, WHITE, [190, None, None, 50], MEDIUM_FONT)
		#DrawText(MAIN_LCD, "Night: "+forcast_night, WHITE, [203, None, None, 50], MEDIUM_FONT)

		button = pygame.Surface((MAIN_LCD_width,40), pygame.SRCALPHA)
		button.fill(HOTSPOT_FILLING)
		Day4Button = MAIN_LCD.blit(button, (0,185))
	else:
		DrawText(MAIN_LCD, "Error Loading Weather...", WHITE, [50, None, None, 5], XLARGE_FONT)

def DrawDaysWeather(cur_day):
	global DayButton

	if Weather_JSON != None and len(Weather_JSON) > 0:
		JSON_root = Weather_JSON['forecast']
	
		day = ""
		forcast_day = ""
		forcast_night = ""
		conditions = ""
		high = ""
		low = ""
		iconName = ""

		if cur_day == 1:
			day = JSON_root['txt_forecast']['forecastday'][0]['title']
			forcast_day = JSON_root['txt_forecast']['forecastday'][0]['fcttext']
			forcast_night = JSON_root['txt_forecast']['forecastday'][1]['fcttext']
			conditions = JSON_root['simpleforecast']['forecastday'][0]['conditions']
			high = JSON_root['simpleforecast']['forecastday'][0]['high']['fahrenheit']
			low = JSON_root['simpleforecast']['forecastday'][0]['low']['fahrenheit']
			iconName = JSON_root['simpleforecast']['forecastday'][0]['icon']
		elif cur_day == 2:
			day = JSON_root['txt_forecast']['forecastday'][2]['title']
			forcast_day = JSON_root['txt_forecast']['forecastday'][2]['fcttext']
			forcast_night = JSON_root['txt_forecast']['forecastday'][3]['fcttext']
			conditions = JSON_root['simpleforecast']['forecastday'][1]['conditions']
			high = JSON_root['simpleforecast']['forecastday'][1]['high']['fahrenheit']
			low = JSON_root['simpleforecast']['forecastday'][1]['low']['fahrenheit']
			iconName = JSON_root['simpleforecast']['forecastday'][1]['icon']
		elif cur_day == 3:
			day = JSON_root['txt_forecast']['forecastday'][4]['title']
			forcast_day = JSON_root['txt_forecast']['forecastday'][4]['fcttext']
			forcast_night = JSON_root['txt_forecast']['forecastday'][5]['fcttext']
			conditions = JSON_root['simpleforecast']['forecastday'][2]['conditions']
			high = JSON_root['simpleforecast']['forecastday'][2]['high']['fahrenheit']
			low = JSON_root['simpleforecast']['forecastday'][2]['low']['fahrenheit']
			iconName = JSON_root['simpleforecast']['forecastday'][2]['icon']
		elif cur_day == 4:
			day = JSON_root['txt_forecast']['forecastday'][6]['title']
			forcast_day = JSON_root['txt_forecast']['forecastday'][6]['fcttext']
			forcast_night = JSON_root['txt_forecast']['forecastday'][7]['fcttext']
			conditions = JSON_root['simpleforecast']['forecastday'][3]['conditions']
			high = JSON_root['simpleforecast']['forecastday'][3]['high']['fahrenheit']
			low = JSON_root['simpleforecast']['forecastday'][3]['low']['fahrenheit']
			iconName = JSON_root['simpleforecast']['forecastday'][3]['icon']


		weatherIcon = pygame.image.load(os.path.dirname(os.path.abspath(__file__))+icon_root+iconName+".png").convert_alpha()

		DrawImage(MAIN_LCD, weatherIcon, [20, None, None, "center"], (85,85))

		DrawText(MAIN_LCD, day, WHITE, [100, None, None, "center"], XLARGE_FONT)
		DrawText(MAIN_LCD, "High: "+high+"* / Low: "+low+"*", LIGHT_GRAY, [120, None, None, "center"], XLARGE_FONT)
		#DrawText(MAIN_LCD, conditions, LIGHT_GRAY, [70, None, None, 60], XLARGE_FONT)
		DrawText(MAIN_LCD, "Day: "+forcast_day, WHITE, [140, None, None, "center"], MEDIUM_FONT, 300)
		DrawText(MAIN_LCD, "Night: "+forcast_night, WHITE, [190, None, None, "center"], MEDIUM_FONT, 300)

		button = pygame.Surface((MAIN_LCD_width,MAIN_LCD_height), pygame.SRCALPHA)
		button.fill(HOTSPOT_FILLING)
		DayButton = MAIN_LCD.blit(button, (0,0))
		
		#######


def ShowLoadingScreen():
    #Fill the screen with black
    MAIN_LCD.fill(BLACK)
    #Hide mouse Pointer
    #pygame.mouse.set_visible(False)
    #Show loading Text
    DrawText(MAIN_LCD, "Loading... Please Wait", WHITE, [10, None, None, 10], MEDIUM_FONT)
    pygame.display.update()

#First thing, show a loading screen
ShowLoadingScreen()

#starter tick
start_ticks=pygame.time.get_ticks()

#Show which page... 0 = 4 Day weather, 1 = day 1, 2 = day 2... etc
show_page = 0

#Infinate Loop to render the screen stuff
running = 1
while running:
	#calculate how many seconds
	seconds = (pygame.time.get_ticks()-start_ticks) * 0.001

	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0
	elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_ESCAPE:
			running = 0
	elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: #Click Buttons
		if show_page == 0:
			if Day1Button != None and Day1Button.collidepoint(event.pos):
				show_page = 1
			elif Day2Button != None and Day2Button.collidepoint(event.pos):
				show_page = 2
			elif Day3Button != None and Day3Button.collidepoint(event.pos):
				show_page = 3
			elif Day4Button != None and Day4Button.collidepoint(event.pos):
				show_page = 4
		else:
			if DayButton != None and DayButton.collidepoint(event.pos):
				show_page = 0


	if(seconds % 10800) == 0: #every 3 Hours
		Weather_JSON = UpdateWeatherJSON()
		
	#Draw Calls
	DrawBackground()
	DrawTime()
	if show_page > 0:
		DrawDaysWeather(show_page)
	else:
		Draw4DayForcast()


	pygame.display.update()