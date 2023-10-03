'''
The third spider collects the watched-data of the population
Very similar to the user spider but different requirements
I know copying code is bad practice but it's 5am and I
don't want to make a higher-class spider that they call
up to to reuse the functions (but maybe when I come back to it)
'''
import scrapy
import csv
import os.path

class RevoSpider(scrapy.Spider):
    name = "revo"
    head = []
    url_base = "https://letterboxd.com"
    movie_urls = []
    ready = 0
    
    # You can actually delete "basegenpop.csv" after this finishes making "genpop.csv"
    # Its only purpose is to be the springboard for this csv file.
    if (ready == 1 and os.path.isfile('basegenpop.csv')):
      with open('basegenpop.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        head = next(csvreader)
        for row in csvreader:
          movie_urls.append(url_base + row[0] + "films/")
      movie_urls = list(dict.fromkeys(movie_urls))
    
    start_urls = movie_urls

    custom_settings = {
      'FEED_FORMAT': 'csv',
      'FEED_URI': 'genpop.csv',
    }

    def parse(self, response):
        for movieItem in response.xpath("//ul/li[@class='poster-container']"):
          user = response.xpath("//div[@class='profile-mini-person']/a/@href").get()
          movie = movieItem.xpath("div/@data-poster-url").get().split("image-150")[0]
          rating = movieItem.xpath("p/span/@class").getall()
          if (len(rating) != 0):
            score = ""
            like = ""
            for i in rating:
              if "rated-" in i:
                score = i.split("rated-")[-1]
              if "liked" in i:
                like = i.split(" ")[0]
            rating = [score, like]
          yield{
            "user": user,
            "movie": movie,
            "rating": rating,
          }
        
        next_page = response.xpath("//div[@class='pagination']").xpath("div/a[@class='next']").xpath("@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)