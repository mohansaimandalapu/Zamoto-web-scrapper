import time
from selenium import webdriver
from parsel import Selector, selector
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3
import re
import scrapy


from xpath_utils import xpath_maps


class RestaurantScraper(object):
    """
  Class to extract all dynamic html content from a given zomato
  Restaurant page
  """

    def __init__(self, restaurant_url: str = None, driver: webdriver = None):
        self.restaurant_url = restaurant_url
        self.driver = driver

        # visit restaurant webpage
        self.driver.get(self.restaurant_url)


    def fetch_menu_sections(self):
        """
    Method to fetch all menu section web elements
    using menu_sections xpath
    """
        menu_section_child_elements = self.driver.find_elements_by_xpath(
            xpath_maps["menu_sections"]["child"]
        )

        # check if there is veg only section and if exists neglect the first child
        if (
            menu_section_child_elements[0]
            .find_element_by_xpath(xpath_maps["menu_sections"]["veg_only"])
            .text
            == "veg only"
        ):
            del menu_section_child_elements[0]
        menu_num_sections = len(menu_section_child_elements)
        return menu_num_sections, menu_section_child_elements

    def render_readmore(self, section: WebElement = None, section_num: int = None):
        """
    Method to render the full description of each dish
    if it exists

    section: the section webelement from selenium
    section_num: the index of the current section in the menu section
    """
        # check if there are subsections within given section
        if (
            section_num > 0
        ):  # because 0 is reserved for recommended section and it wont have any subsections
            num_subsection_child_elements = len(
                self.driver.find_elements_by_xpath(
                    xpath_maps["menu_section_subsections"]["child"].substitute(
                        {"section_index": section_num, "subsection_index": "*"}
                    )
                )
            )
            if num_subsection_child_elements>0:
                for index in range(1, num_subsection_child_elements + 1):
                    subsection_index = index * 2

                    # generate xpath for each subsection block
                    xpath = xpath_maps["menu_section_subsections"][
                        "read_more_child"
                    ].substitute(
                        {"section_index": section_num, "subsection_index": subsection_index}
                    )

                    # get number dishes in each subsection
                    num_dishes = len(
                        self.driver.find_elements_by_xpath(
                            xpath_maps["menu_section_subsections"]["read_more_child"].substitute({"section_index": section_num, "subsection_index": subsection_index})
                        )
                    )
                    
                    for j in range(1, num_dishes+1):
                        dish_xpath = xpath_maps["menu_section_subsections"][
                            "read_more_xpath"
                        ].substitute(
                            {
                                "section_index": section_num,
                                "subsection_index": subsection_index,
                                "read_more_index": j,
                            }
                        )
                        # if readmore exists then load 
                        try:
                            time.sleep(0.5)
                            # get the element into visibility
                            
                            ActionChains(self.driver).move_to_element(
                                self.driver.find_element_by_xpath(dish_xpath)
                            ).perform()
                            time.sleep(1)
                            
                            # click on readmore section
                            self.driver.find_element_by_xpath(dish_xpath).click()
                        except Exception as e:
                            print(f"DEBUG:{e}")
                            
                            pass
            else:


                # number of dishes in each section
                num_section_dishes = len(self.driver.find_elements_by_xpath(
                    xpath_maps["menu_sections"]["section_dish_xpath_child"].substitute(
                        {'section_index':section_num})))
                
                for i in range(1, num_section_dishes+1):
                    dish_xpath = xpath_maps["menu_sections"]["section_dish_xpath"].substitute({'section_dish_index':i,
                    'section_index':section_num})
                    read_more_xpath = dish_xpath + '/div[2]/p/span'
                    # if readmore exists then load 
                    try:
                        # get the element into visibility
                        ActionChains(self.driver).move_to_element(
                            self.driver.find_element_by_xpath(dish_xpath)
                        ).perform()
                        time.sleep(1)
                        # click on readmore section
                        self.driver.find_element_by_xpath(read_more_xpath).click()
                    except Exception as e:
                        print(f"DEBUG:{e}")
            
                        pass
                


    def fetch_html_source_code(self):
        """
    Method to get source html code of current
    web page
      """

        elem = self.driver.find_element_by_xpath("//*")
        self.source_code = elem.get_attribute("outerHTML")
        return self.source_code


    def fecth_all_details_of_resturent(self):
        
        
        """
            Method to fetch all the details of the resturent and all dishes in the resturent
            and store them in the sqlite database
        """

        # scrapy selector to extract data
        selector = Selector(self.source_code)
    
        #empty dic and  to append all the details that extracted
        resturent_details = {}
        dishes = []

        #exracting resturent name
        resturent_details['res_name'] = selector.xpath('//*[@id="root"]/div/main/div/section[3]/section/section[1]/div/h1').css('h1::text').get()
                
        #exracting resturent location
        resturent_details['res_loc'] = selector.xpath('//*[@id="root"]/div/main/div/section[3]/section/section[1]/section[1]/a').css('::text').get()

        #exracting resturent number of delivery reviews 
        resturent_details['no_delivery_reviews']  = selector.xpath('//*[@id="root"]/div/main/div/section[3]/section/section[2]/section[2]/div[2]/p').css('::text').re(r'[0-9].')[0]
        
        #extracting resturent reviews
        resturent_details['review_stars'] = selector.xpath('//*[@id="root"]/div/main/div/section[3]/section/section[2]/section[2]/div[1]/p').css('::text').get()

        # loop over every dish section to extract every dish details
        i = 2
        while selector.xpath(f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{i}]/div[2]')!=[]:
            dish_group = selector.xpath(f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{i}]/div[2]')
            j = 1
            while selector.xpath(f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{i}]/div[2]/div[{j}]') != []:
                dish_dic = {}
                
                #extracting food cuisine
                dish_dic['dish_cuisine'] = selector.xpath(f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{i}]').css('::text').get()
                

                
                dish = selector.xpath(f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{i}]/div[2]/div[{j}]')
                
                
                # extracting dish name
                if dish.css('h4::text').get() != None:
                    dish_dic['dish_name'] = dish.css('h4::text').get()
                else:
                    dish_dic['dish_name'] =  'BLANK'#'None'
                    
                
                # extracting dish price
                price_list = dish.css('span::text').getall()
                
                r = re.compile("₹.*")
                dish_dic['dish_price'] = list(filter(r.match, price_list))[0].split('₹')[1]
                
                #exracting dish discription
                if dish.css('p::text').get() != None:
                    dish_dic['dish_dis'] = dish.css('p::text').get()
                else:
                    dish_dic['dish_dis'] = 'BLANK'#'None'
                    
                #exracting dis tag
                if dish.css('div::text').get() != None:
                    dish_dic['dis_tag'] = dish.css('div::text').get()
                else:
                    dish_dic['dis_tag'] = 'BLANK'#'None'
                    
                    
                
                # extracting dish images url if dish has tag of 'MUST TRY'
                if selector.xpath(f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{i}]/div[2]/div[{j}]/div/div/div[1]/div[1]/img').css('::attr(src)').get() == None:
                    dish_dic['dish_img_url'] = 'BLANK'#'None'
                    
                    
                dish_tag = dish.css('div::text').get()
                if dish_tag == 'MUST TRY':
                    dish_dic['dish_img_url'] = selector.xpath(f'//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[{i}]/div[2]/div[{j}]/div/div/div[1]/div[1]/img').css('::attr(src)').get()
                
                else:
                    dish_dic['dish_img_url'] = 'BLANK'#'None'
                    
                    
                # extracting dish_type(ex:veg or non-veg)
                dish_dic['dish_type'] = dish.css('div::attr(type)').get()
                
                
                dishes.append(dish_dic)
                
                
                j=j+1
            i = i+1
            
        # creating sqlite database to store the extracted values
        db = sqlite3.connect(f'{resturent_details["res_name"]}.db')
        cur = db.cursor()

        # creating table resturent details to store resturent details 
        cur.execute('''CREATE TABLE IF NOT EXISTS resturent_details(
                        res_name TEXT, 
                        res_loc TEXT, 
                        no_delivery_reviews INTEGER,  
                        review_stars FLOAT
                        )''')
        
        
        #query to add extracted data to database
        query = "insert into resturent_details " + str(tuple(resturent_details.keys())) + " values" + str(tuple(resturent_details.values())) + ";"
        
        cur.execute(query)


        # creating dishes tabel to store every dish details
        cur.execute('''CREATE TABLE IF NOT EXISTS dishes(
                        dish_cuisine TEXT DEFAULT NULL,
                        dish_name TEXT DEFAULT NULL, 
                        dish_price INTEGER DEFAULT NULL, 
                        dish_dis TEXT DEFAULT NULL,  
                        dis_tag TEXT DEFAULT NULL,
                        dish_img_url TEXT DEFAULT NULL,
                        dish_type TEXT DEFAULT NULL
                        )''')
        

        #loop to add every dish details to database
        for i in range(len(dishes)):
            dish_dic = dishes[i]
            for key in dish_dic.keys():
                if dish_dic[key] is None or dish_dic[key] == 'None' :
                    dish_dic[key] = 'BLANK'
            dishes[i] = dish_dic
            query = "INSERT OR IGNORE INTO dishes " + str(tuple(dishes[i].keys())) + " values" + str(tuple(dishes[i].values())) + ";"
            cur.execute(query)

        db.commit()


        cur.close()



if __name__ == "__main__":
    from browser import RestaurantScraper
    import browser
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    url = 'https://www.zomato.com/bangalore/india-bistro-2-indiranagar-bangalore/order'
    crawler = RestaurantScraper(url,webdriver.Chrome(ChromeDriverManager().install()))
    menu_num_sections, menu_section_child_elements = crawler.fetch_menu_sections()
    for i,element in enumerate(menu_section_child_elements):
        crawler.render_readmore(element,i)
    source_code = crawler.fetch_html_source_code()
    crawler.fecth_all_details_of_resturent()
    crawler.driver.close()