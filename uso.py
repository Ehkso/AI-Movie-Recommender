'''
This is the first spider, it takes the two users' profiles
and scrapes all their movies watched (+ respective ratings/liked)
'''
import scrapy

class UsoSpider(scrapy.Spider):
    name = "uso"
    # Insert links to target user profiles here
    # Links should look like this:
    # "https://letterboxd.com/[user]/films/"
    start_urls = [
      "https://letterboxd.com/aeio/films/",
      "https://letterboxd.com/celdinner/films/",
    ]
    custom_settings = {
      'FEED_FORMAT': 'csv',
      'FEED_URI': 'tusers.csv',
    }

    def parse(self, response):
        for movieItem in response.xpath("//ul/li[@class='poster-container']"):
          user = response.xpath("//div[@class='profile-mini-person']/a/@href").get()
          movie = movieItem.xpath("div/@data-poster-url").get().split("image-150")[0]
          rating = movieItem.xpath("p/span/@class").getall()

          # Letterboxd has both "likes" and "ratings" for movies
          # This is just slightly annoying because they appear as sibling nodes or don't exist otherwise.
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