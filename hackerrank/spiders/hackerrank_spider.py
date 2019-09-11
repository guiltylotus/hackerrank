import json
import scrapy


class HackerrankScraper(scrapy.Spider):
	name = 'hackerrank'
	start_urls = ["https://www.hackerrank.com/rest/contests/master/tracks/algorithms/challenges?offset=0&limit=500&track_login=true"]

	def parse(self, response):
		data = json.loads(response.text)
		print('______________________')
		print(len(data["models"]))
