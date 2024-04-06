import requests
from bs4 import BeautifulSoup
import pandas as pd

data=[]

def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve the webpage: {url}")
        return None

def parse(url):
    soup = get_soup(url)

    if soup:
        suppliers = soup.find_all("div",class_="titled-list titled-list--dropdown")  # Update the selector as needed
        for supplier in suppliers[0:17]:
            supplier_anchor=supplier.find('a')
            link = supplier_anchor.get('href')
            name = supplier_anchor.text
            print(f"Visiting link: {link}-----------------------")
            print(f"Visiting name: {name}-----------------------")
            parse_supplier(name,url+link)

            print("Saving data...")

            # Create a DataFrame from the data
            df = pd.DataFrame(data)

            # Drop duplicates
            df = df.drop_duplicates()

            # Save the DataFrame to an Excel file
            df.to_excel('output.xlsx', index=False)



def parse_supplier(first_name,link):
    print(link)
    soup = get_soup(link)
    if soup:
        supplier_div = soup.find(class_="indent")
        suppliers = []
        supplier_ols = supplier_div.find_all("ol")
        for ol in supplier_ols:
            suppliers += ol.find_all("li")  # Update the selector as needed
        # print(suppliers)
        for supplier in suppliers:
            supplier_anchor = supplier.find('a')
            link = supplier_anchor.get('href')
            name = supplier_anchor.text
            print(f"\tVisiting link: {link}-------------")
            print(f"\tVisiting name: {name}-------------")
            parse_sublevel_supplier(first_name,name,link)

        next_page = soup.find("a", string='Next')
        if next_page:
            next_page_url = next_page.get('href')
            print(f"\tVisiting next page of second level supplier: {next_page_url}")
            if next_page_url != "#":
                parse_supplier(first_name,next_page_url)

def parse_sublevel_supplier(first_name,second_name,link):
    soup = get_soup(link)
    if soup:
        supplier_div = soup.find(class_="indent")
        if supplier_div:
            suppliers=[]
            supplier_ols=supplier_div.find_all("ol")
            for ol in supplier_ols:
                suppliers += ol.find_all("li")  # Update the selector as needed
            # print(suppliers)
            for supplier in suppliers:
                supplier_anchor = supplier.find('a')
                link = supplier_anchor.get('href')
                name = supplier_anchor.text
                # print(f"\t\tVisiting link: {link}-----")
                # print(f"\t\tVisiting name: {name}-----")
                data.append({'Supplier name': name, 'link': link,"Sub category":second_name,"Category":first_name})  # Add the data to the global list
                # df = pd.DataFrame(data)
                # df.to_excel('output.xlsx', index=False)
                # Store the data or do something with it here

            next_page = soup.find("a", string='Next')
            if next_page:
                next_page_url = next_page.get('href')
                # print(f"Visiting next page of third level supplier: {next_page_url}")
                if next_page_url!="#":
                    parse_sublevel_supplier(first_name,second_name,next_page_url)

# Start the script by calling the parse function with the starting URL
start_url = "https://www.thomasnet.com"
parse(start_url)

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Drop duplicates
df = df.drop_duplicates()

# Save the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)

# import scrapy
# import json
# from w3lib.html import remove_tags
#
#
# class EllsworthSpider(scrapy.Spider):
#     name = 'ellsworth'
#     start_urls = ['URL_of_the_webpage_where_script_is']
#
#     def parse(self, response):
#         # Extract the script content
#         script_content = response.xpath('//script[contains(., "__NEXT_DATA__")]/text()').get()
#
#         # Remove HTML tags if any
#         script_content_clean = remove_tags(script_content)
#
#         # Convert JSON data to Python dictionary
#         data = json.loads(script_content_clean)
#
#         # Traverse the dictionary to find the phone number
#         phone_number = data.get("props", {}).get("pageProps", {}).get("businessDetails", {}).get("primaryPhone")
#
#         # Yield the result
#         yield {'phone_number': phone_number}

# Run the spider
