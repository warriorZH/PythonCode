from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import selenium
import sys
import os

sel = selenium.webdriver.Firefox()
sel.get("file:///home/warrior/Coding/PythonCode/weibocookie/pagecont")
#sel.get('http://www.baidu.com/')
#sleep(3)
#sel.open("/home/warrior/Coding/PythonCode/weibocookie/pagecont")
pagecont = sel.title
tagsHtml = sel.find_elements_by_class_name("S_txt1")
#text = [comment  for comment in tagsHtml]
print pagecont
if tagsHtml:
    print "success!!"
else:
    print "failure!!"
val ele[]
for element in tagsHtml:
    aa = element.get_attribute('alt') 
    bb = element.get_attribute('usercard') 

    #cc = aa + ' * ' + bb
    print aa; print bb#element.get_attribute('alt')# + ' * ' + element.get_attribute('alt')


# Create a new instance of the Firefox driver
##driver = webdriver.Firefox()

# go to the google home page
##driver.get("http://www.baidu.com/")
#print driver.log_types

# the page is ajaxy so the title is originally this:
##print driver.title

# find the element that's name attribute is q (the google search box)
#inputElement = driver.find_element_by_name("q")

# type in the search
#inputElement.send_keys("cheese!")

# submit the form (although google automatically searches now without submitting)
#inputElement.submit()

#try:
        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
 #   WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

                # You should see "cheese! - Google Search"
    #print driver.title

#finally:
#sel.quit()
#driver.quit()
