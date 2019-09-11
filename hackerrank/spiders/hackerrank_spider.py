import json
import scrapy


class HackerrankScraper(scrapy.Spider):
    def __init__(self):
        self.offset = 0

    name = 'hackerrank'
    problems_api = "https://www.hackerrank.com/rest/contests/master/tracks/algorithms/challenges?offset={}&limit=2&track_login=true"
    start_urls = [problems_api.format(0)]

    def parse(self, response):
        datas = json.loads(response.text)["models"]

        for data in datas:
            data_url = 'https://www.hackerrank.com/challenges/' + \
                data['slug'] + '/problem'
            yield {
                'name': data["name"],
                'url': data_url
            }
            yield scrapy.Request(url=data_url, callback=self.parseProblems)

        if len(datas) > 0 and self.offset < 3:
            self.offset = self.offset + 2
            yield scrapy.Request(url=self.problems_api.format(self.offset), callback=self.parse)

    def parseProblems(self, response):
        data = response.css(
            "div.challenge_problem_statement div.hackdown-content").css('p, ul').css('::text').extract()

        problemStatement = ' '.join(data).replace('\n', '')
        problemStatement = ' '.join(problemStatement.split())
        yield {
            'problems': problemStatement
        }
