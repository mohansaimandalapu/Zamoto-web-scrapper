import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
import time
import sqlite3

driver = webdriver.Chrome(ChromeDriverManager().install())

res_url = []

driver.get('https://www.zomato.com/bangalore')

total_height = int(driver.execute_script("return document.body.scrollHeight"))
status = True
i = 0
j=0
while status :
    
    driver.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(.3)
    page_height = int(driver.execute_script("return document.body.scrollHeight"))
    i=i+.01*page_height

    if i > page_height:
        status = False
    


elem = driver.find_element_by_xpath("//*")

source_code = elem.get_attribute("outerHTML")


selector = Selector(source_code)


j=8
while selector.xpath(f'//*[@id="root"]/div/div[{j}]/div/div[1]/div/div/a[2]') !=[]:
    i = 1
    while selector.xpath(f'//*[@id="root"]/div/div[{j}]/div/div[{i}]/div/div/a[2]') !=[]:
        link = selector.xpath(f'//*[@id="root"]/div/div[{j}]/div/div[{i}]/div/div/a[2]').css('a::attr(href)').get()
        link_path = 'https://www.zomato.com/' + link
        res_url.append(link_path)
        i+=1
    j=j+1



conn = sqlite3.connect('resturent_links.db')  
c = conn.cursor() 

c.execute('''CREATE TABLE url_links
             ([resturent_id] INTEGER PRIMARY KEY,[resturent_link] text)''')



for i in range(len(res_url)):
    Url_links_dic = {'resturent_id':i,'resturent_link':res_url[i]}
    c.execute('insert into url_links values (?,?)', [Url_links_dic['resturent_id'], Url_links_dic['resturent_link']])
    


