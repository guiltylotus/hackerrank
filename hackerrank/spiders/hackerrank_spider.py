import json
import scrapy


class HackerrankScraper(scrapy.Spider):
    name = 'hackerrank'
    start_urls = [
        "https://www.hackerrank.com/rest/contests/master/tracks/algorithms/challenges?offset=0&limit=50&track_login=true"]

    def parse(self, response):
        datas = json.loads(response.text)["models"]

        for data in datas:
            yield {
                'name': data["name"]
            }
