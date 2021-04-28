#################################### HOFSTEDE DATASCRAPER       #########################################################
# by ALESSIO STEFAN                                             #########################################################
#################################### HOW THE DATA SCRAPER WORKS #########################################################
#analyizing the website 
# the main link that the data scrap have to acess is https://www.hofstede-insights.com/country-comparison/
# than for check a country's info we need to acess to https://www.hofstede-insights.com/country-comparison/[NAME_OF_THE_COUNTRY]
#  
# also checking the HTML documents of the website we notice a list (inside hostedeHTMLelement) containing all the names of the countries that we need to add to the main url
# and we are creating a list with all the countries name with the function extract_from_txt() 
# 
# for every country's page there is a canva containing all the info we need and with get_canva(x) the data scrap connect to the link (main link + name of the country[x])
# and save the canva as a DATA URL (with a JS script) and with canva_to_image(country,x) saving the DATA URL as image (named as x.png)
#
# than with extract_all_canvas(x) give x as list of the names of the countries for every country name save the image of the plot containing the info we need (inside images_scrapped)


# I tried to use a machine learning code called tesseract (the python version) for reading all the text inside an image but
# for every image the code give different result making really hard (or maybe impossible for me) so I had (with patience) to create
# the csv using notepad and copying the image and write on the file than saving the csv progetto.csv where for every country
# we can observe all the 6 dimension's value



# ATTENTION : I used the driver of Google Chrome if u need to try this code u need to change all the path inside the code and adapt the command for the driver you need 




import pandas       #lib for wqork with csv             
import requests     #lib for save the text of the HTML request(or response)
from selenium import webdriver  #lib for use browser driver usefull for interface with the website
from selenium.webdriver.common.keys import Keys
from binascii import a2b_base64 #lib for work with base64 strings
import urllib                   #lib for URL handling modules
from urllib.request import urlopen
from bs4 import BeautifulSoup   #lib for parsing HTML (even XML but dont need here) documents (the HTML of the website)
import re #regular expression operation
import cv2 
import numpy as np # lib for cahnge  
import time as t   # lib for use a timer inside the data scrap (see extract_all_canva() function)



def get_canva(x):                                                               #return the canva of the selected country as DATA URL                                                            
    # prepare the option for the chrome driver
    options = webdriver.ChromeOptions()                                         #save the options for the browser we choose (in my case CHROME)
    options.add_argument('headless')                                            #option run an headless chrome browser
    base_url = 'https://www.hofstede-insights.com/country/'                     
    new_url =str(x+'/')                                                         #the base_url plus the country name make the final url 
    path = r'C:\Users\alste\Desktop\chromium\chromedriver.exe'                  #path of the driver of the browser
    myscript = 'var canvas = document.getElementById("bar-chart"); var image=canvas.toDataURL("image/png").replace("image/png","image/octet-stream"); return(image); ' #JS javascript 
    browser = webdriver.Chrome(path,chrome_options=options)     # start chrome browser
    browser.get(base_url+new_url)                               # obtain the response of the url we create
    result = browser.execute_script(myscript)                   # save the result of the JS script (DATAURL STRING)
    browser.quit()                                              # quit chrome browser
    return(result)                                              



def canva_to_image(data_url,country):                       # return the image (.PNG) of the DATA URL input (the field COUNTRY is a string for the name of the saved image)
    response = urllib.request.urlopen(data_url)             # open the data url 
    path = 'images_scrapped/'+country+'.png'                # path where to save the images 
    with open(path, 'wb') as f:                             
        f.write(response.file.read())                       # "write" the image inside the path 




def get_hostede_plot(x): # x = country to save the plot  / RETURN image (PNG) of the specific country    (get_canva + canva_to_image)
    canva_to_image(get_canva(x),x)



def extract_fromtxt(): # save in a array all the countries inside the SELECT element (saved in hofstedeHTMLelement.txt) of hostede website with string fixed
    text = open(r"C:\Users\alste\Documents\UNI\PROGRAMMAZIONE\lavoro\DATA SCRAP\hostedeHTMLelements.txt")           
    data= text.read().replace('<select multiple="" placeholder="Type a country" tabindex="-1" class="select2-hidden-accessible" aria-hidden="true" data-select2-id="3">',"")
    data=data.replace("</select>","")
    words =re.split("</option>", data)
    for i in range(0,len(words)):
        words[i]=re.sub('<[^>]+>', '', words[i])
        if (words[i].find(' ')):
            words[i]=re.sub(' ','-',words[i])   
    text.close()
    return(words)


def later():                        # save all countries names and saved it as numpy array (usefull for change elements inside)
    names_first = extract_fromtxt()
    final = np.array(names_first)
    return final


def adjust_char(words):             # function for delete the char * 
    for i in range(0,len(words)):
            words[i]=words[i].replace('*','')
    return(words)




def extract_all_canvas(x):              # containing a list of countries save all imgs of the canva (x = list of countries)
    for i in range(0,len(x)):           
        t.sleep(3)
        print("Taking the "+x[i]+" plot")
        get_hostede_plot(x[i])
    print("DONE")

    

countries = later()
new_countries = np.delete(countries,88,) #string error     (need to delete this country)
new_countries = np.delete(new_countries,117) #string error (need to delete this country)

###change this countries's name with the HOFSTEDE model of this particular countries
new_countries[26] = "the-dominican-republic"
new_countries[72] = "the-netherlands"
new_countries[81] = "the-philippines"
new_countries[110] = "the-united-arab-emirates"
new_countries[111] = "the-uk"
new_countries[112] = "the-usa"

#run the code
extract_all_canvas(adjust_char(new_countries))
