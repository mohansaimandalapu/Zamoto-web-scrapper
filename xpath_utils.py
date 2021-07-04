"""
Dictionary mapping to contain all the required xpaths to scrap
dish data from zomato
"""
from string import Template

xpath_maps = {
    "menu_sections": {
        "xpath": '//*[@id="root"]/div/main/div/section[4]/section/section[2]',
        "child": '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[*]',
        "veg_only": '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[1]/section/label',
        "section_dish_xpath_child": Template('//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[$section_index]/div[2]/div[*]/div/div'),
        "section_dish_xpath": Template('//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[$section_index]/div[2]/div[$section_dish_index]/div/div'),
    },
    "menu_section_subsections": {
        "xpath": Template(
            '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[$subsection_num]'
        ),
        "child": Template(
            '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[$section_index]/div[$subsection_index]/p'
        ),
        "read_more_child": Template(
            '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[$section_index]/div[$subsection_index]/div[*]/div/div/div[2]/p/span'
        ),
        "read_more_xpath": Template(
            '//*[@id="root"]/div/main/div/section[4]/section/section[2]/section[$section_index]/div[$subsection_index]/div[$read_more_index]/div/div/div[2]/p/span'
        ),
    },
    "user_reviews": {
        "xpath": '//*[@id="root"]/div/main/div/section[4]/div/div/section[2]',
        "num_review_xpath": '//*[@id="root"]/div/main/div/section[4]/div/div/section[2]/div[1]/div[1]',
        "review_child": '//*[@id="root"]/div/main/div/section[4]/div/div/section[2]/div[2]/p[*]',
    },
}


# //*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]
# //*[@id="root"]/div/main/div/section[4]/section/section[2]/section[3]
# subsections
# //*[@id="root"]/div/main/div/section[4]/section/section[2]/section[3]/div[2]/p
# //*[@id="root"]/div/main/div/section[4]/section/section[2]/section[3]/div[4]/p
# //*[@id="root"]/div/main/div/section[4]/section/section[2]/section[3]/div[6]/p
# //*[@id="root"]/div/main/div/section[4]/section/section[2]/section[2]/div[2]/div[4]/div/div/div[2]/p/span
