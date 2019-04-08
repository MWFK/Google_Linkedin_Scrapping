import csv
import parameters_google #this current pg will call this indicated script
from time import sleep
from parsel import Selector
#selenium imports
from selenium import webdriver #pip install -U selenium #-U Upgrade all specified packages to the newest available version.
from selenium.webdriver.common.keys import Keys #pip install -U selenium
from selenium.common.exceptions import TimeoutException #slenesse timeout exception
from selenium.webdriver.common.by import By #used wih functions that have by
from selenium.webdriver.support.ui import WebDriverWait #selenesse wait (like the pause in python)


####################chrome controlled by test machine
driver = webdriver.Chrome('C:\chromedriver.exe')#,chrome_options=options#download chromedriver (to test a scenario by a machine)
###################

#################################search queries on google
driver.get('https:www.google.com')#chromedriver will go to the following links
sleep(3)

#mettre une recherche au niveau de google
#<input id="id-search-field" name="q" role="textbox" class="search-field placeholder" placeholder="Search" tabindex="1" type="search">
search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters_google.search_query) 
sleep(0.5)

driver.page_source
search_query.send_keys(Keys.RETURN)#Tapez entrer pour chercher
sleep(3)
#################################



##############parcourir tt les page de resultat
link = 1
page = 1
while page <= 100 :

#stocker les urls de lien trouver en google
 urls = driver.find_elements_by_class_name('iUh30') 
 urls = [url.text for url in urls]
 sleep(0.5)
 
 for cmpt in urls:
   #driver.get(cmpt)#go inside the website so if the site is unreachable, the script will exit!!!!
   #driver.navigate().to(cmpt) if does not work it can be version incompatibility with selenium ide and chromre
   #and because this last function keep cookies, then u can do  driver.navigate().back() driver.navigate().forward() driver.navigate().refresh().
   #sleep(5)
   #sel = Selector(text=driver.page_source)
   
   ###############print URLs
   link += 1
   print('\ngoogle search page number= '+str(page)+'\nLink number= '+str(link)+'\n'+str(cmpt)) 
   ###############
   
   #################store URL's in csv
   writer = csv.writer(open(parameters_google.save_to, 'a', newline='', encoding='utf-8')) #utf-32 this encoding solve all probs but its to big!!!
   writer.writerow([str(cmpt)])
   #.encode('utf-8') adds b'' to the string, and we can use encoding='utf-8' 
   #binary mode doesn't take an encoding argument
   ######################################
   
 #############END FOR

 ###########################################click google next button
 page += 1
 driver.find_element_by_id("pnnext").click()
 sleep(2)
 ##########################################
 
 #################END While

# terminates the application
driver.quit()