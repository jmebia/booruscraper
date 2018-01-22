#! python3
# booruscraper.py - scrapes the danbooru website for specific images by using tags

import sys, os, requests, shutil
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

print("Starting...")


def scrape(tag):

    print("scraping...")

    MAX_PAGE_SEARCH = 1
    page = 1

    # stops when the maximum count of pages to be searched is reached
    for ctr in range(1, MAX_PAGE_SEARCH + 1):
        # html page request, grabs the page
        req = Request('http://danbooru.donmai.us/posts?page=' + str(page)
            + '&tags=' + space_to_underscore(tag), headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        # html parsing
        spage = soup(webpage, "html.parser")
        # finds all the articles in the page that contains images
        images = spage.findAll("article")

        print ("(Found " + str(len(images)) + " images)")

        # create directory for image tags if the directory doesn't exist
        if not os.path.exists(tag):
            print('Creating directory', tag)
            os.makedirs(tag)
        else:
            print('Directory', tag, 'already exists!')

        print ('downloading images...')

        # iterates through the list and extracts the image url and use it to download
        # the image found
        for image in images:
            # finds the urls of the images' large version
            image_url = image["data-large-file-url"]

            r = requests.get('http://danbooru.donmai.us' + image_url, stream=True,
                                headers={'User-agent': 'Mozilla/5.0'})

            if r.status_code == 200:
                # the split function is for extracting the image type (e.g. jpg, png)
                # and the image's name
                name_type = image_url.split('.')
                name_type[0] = '_'.join(name_type[0].split('/'))

                filename = tag + '/' + name_type[0] + '.' + name_type[1]

                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

        # increment page
        page += 1
		
		
def space_to_underscore(string_):
    return "_".join(string_.split())

	
# a simple dialog to get tag from user
tag = input("Danbooru image tag: ")
scrape(tag)