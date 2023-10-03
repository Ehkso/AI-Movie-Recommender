'''
Finally, this fourth spider takes a movie and collects its list of tags
Observe that it isn't necessary to perform this for the movies
gathered from the main users because all the movies they've
watched will have been watched by other people here as that's
how the people were collected.
'''
import scrapy
import csv
import os.path

class MovoSpider(scrapy.Spider):
    name = "movo"

    head = []
    url_base = "https://letterboxd.com"
    movie_urls = []
    ready = 0
    
    if (ready == 1 and os.path.isfile('genpop.csv')):
      with open('genpop.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        head = next(csvreader)
        for row in csvreader:
          movie_urls.append(url_base + row[1] + "genres/")
      movie_urls = list(dict.fromkeys(movie_urls))

    start_urls = movie_urls

    custom_settings = {
      'FEED_FORMAT': 'csv',
      'FEED_URI': 'tags.csv',
    }

    def parse(self, response):
        movie = response.url.split("letterboxd.com")[-1].split("genres")[0]
        taglist = []
        
        '''
        Note: The [:-1] in the for loop is because the last one is always
        "/film/[movie]/themes/" because it leads to a full themes page (excl. genres).
        '''
        for tag in response.xpath("//div[@id='tab-genres']/child::*/child::*").xpath("a/@href")[:-1]:
          rawtag = tag.get().split("films")[-1].split("by/best-match")[0]
          taglist.append(rawtag)
        yield{
          "movie": movie,
          "tags": taglist,
        }