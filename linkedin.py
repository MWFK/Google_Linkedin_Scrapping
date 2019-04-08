from time import sleep
from selenium import webdriver #pip install -U selenium #-U Upgrade all specified packages to the newest available version.
from selenium.webdriver.common.keys import Keys #pip install -U selenium
from parsel import Selector
import csv
import parameters_linkedin #with this current scipt i have another one called paramters.py
import urllib.parse #convert string to url

####################chrome controlled by test machine
#options = webdriver.ChromeOptions()
#options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
driver = webdriver.Chrome('C:\chromedriver.exe')#chrome_options=options#download chromedriver (to test a scenario by a machine)
###################

####################sign in to linkedin
driver.get('https://www.linkedin.com/')	#the website to be opened
username = driver.find_element_by_class_name('login-email') 
username.send_keys(parameters_linkedin.linkedin_username) #import parameters
sleep(0.5)#mimic human behaviour otherwise google will instantly will know its a robot

password = driver.find_element_by_class_name('login-password')
password.send_keys(parameters_linkedin.linkedin_password) #import parameters
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]') #tell the chromedriver to find a html element that ends with [@type="submit"]
sign_in_button.click()#hit the submit button
sleep(1)
####################


##################################Read the file that contains the linked urls scrapped from google(google.py)
fileHandler = open (parameters_linkedin.read_from, "r") 
# encoding='utf-8' with this encoding, any char can be read with no error
listOfLines = fileHandler.readlines()
fileHandler.close()
##################################


####################################This csv file will contain the data of every link
# defining new variable passing two paramaters
writer = csv.writer(open(parameters_linkedin.save_to, 'w', newline='', encoding='utf-32'))
# utf-8 is very important encoding, because it recognises the whole world caracters, and its sizes increases as the lenght of the char increases

# writerow() method to the write to the file object
writer.writerow(['Name','Job Title','Company','College', 'Location','URL'])
#####################################


##################################Parcourir les URL et extraire les informations
profile_nbr=1
for linkedin_url in listOfLines:

 driver.get(linkedin_url)
 sleep(2)
 sel = Selector(text=driver.page_source) #very important (with sel we can access each element xpath)
 # xpath to extract the text from the class containing the name


#################################################Strip data from the website 
 name = sel.xpath('//*[starts-with(@class,"pv-top-card-section__name inline t-24 t-black t-normal")]/text()').extract_first()
#extract the first occurrence of that element (since its on the top of the page)
#XPath is NOT reliable. If the DOM of the website changes, so does the XPath and your script is bound to crash then. After working with multiple scripts on scrapping, I've come to a conclusion that use XPath as a last resort.   
 if name:
  name = name.strip()

# xpath to extract the text from the class containing the job title
 job_title = sel.xpath('//*[starts-with(@class, "pv-top-card-section__headline")]/text()').extract_first()
 if job_title:
  job_title = job_title.strip()

# xpath to extract the text from the class containing the company
 company = sel.xpath('//*[starts-with(@class,"pv-top-card-v2-section__entity-name pv-top-card-v2-section__company-name")]/text()').extract_first()
 if company:
  company = company.strip()

# xpath to extract the text from the class containing the college
 college = sel.xpath('//*[starts-with(@class,"pv-top-card-v2-section__entity-name pv-top-card-v2-section__school-name")]/text()').extract_first()
 if college:
  college = college.strip()

# xpath to extract the text from the class containing the location
 location = sel.xpath('//*[starts-with(@class,"pv-top-card-section__location")]/text()').extract_first()
 if location:
  location = location.strip()

 linkedin_url = driver.current_url
###########################################################


###############################################print stripped data
 print('profile number= '+str(profile_nbr)) 
 print('Name: ' + str(name)) #on peut pas concatener str avec un encode 
 print('Job Title: ' + str(job_title))
 print('Company: ' + str(company))
 print('College: ' + str(college))
 print('Location: ' + str(location))
 print('URL: ' + str(linkedin_url))
 print('\n')
 profile_nbr+=1#the number of the profile
 ###############################################
 
      	  
 ###########################"""" store the extracted data into a csv wth utf-8 encoding 		  
 writer.writerow([str(name), str(job_title), str(company), str(college), str(location), str(linkedin_url)])
 ############################################

# terminates the application
driver.quit()