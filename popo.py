'''
This second spider populates the dataset with the accounts
of the top x reviews for the given movie
Notes: Will read n-1 pages where n is page_max, so don't use n<2
it works by checking what the number for the next page so if you
set it to (ie) 1 which it'll never see it'll just go forever
It seems there are about 12 reviews per page so you'll be getting
n * 12 users (per movie).
'''
import scrapy
import csv
import os.path

class PopoSpider(scrapy.Spider):
    name = "popo"

    # We build an array of movie links to be passed as start_urls
    head = []
    url_base = "https://letterboxd.com"
    movie_urls = []
    page_max = "2" # Yes, a string, for concatenation purposes.
    ready = 0
    
    if (ready == 1 and os.path.isfile('users.csv')):
      with open('users.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        head = next(csvreader)
        for row in csvreader:
          movie_urls.append(url_base + row[1] + "reviews/by/activity/")
      # Creates a list from the dict of the list of itself :D because the dict clears duplicates.
      movie_urls = list(dict.fromkeys(movie_urls))
      
    start_urls = movie_urls

    custom_settings = {
      'FEED_FORMAT': 'csv',
      'FEED_URI': 'basegenpop.csv',
    }

    def parse(self, response):
        for review in response.xpath("//ul/li[@class='film-detail']"):
          yield{
            "user": review.xpath("a/@href").get(),
          }
        
        # Note that even checking just one page per movie is a lot if you have a lot of movies watched by the users
        # So start small and increase page_max slowly if you want more data and have time to burn.
        end_url = PopoSpider.movie_urls[0].split("letterboxd.com")[-1]
        end_url += "page/" + PopoSpider.page_max + "/"
        next_page = response.xpath("//div[@class='pagination']").xpath("div/a[@class='next']").xpath("@href").get()
        if next_page != (end_url or None):
          yield response.follow(next_page, self.parse)
        else:
          print(f"Reached end_url: {end_url}")