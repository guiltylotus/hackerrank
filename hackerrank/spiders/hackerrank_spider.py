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
            problem_url = 'https://www.hackerrank.com/challenges/' + \
                data['slug'] + '/problem'
            leader_board_url = 'https://www.hackerrank.com/challenges/' + \
                data['slug'] + '/leaderboard?limit=100&page=1'

            yield {
                'name': data["name"],
                'url': problem_url
            }
            yield scrapy.Request(url=problem_url, callback=self.parseProblems)
            yield scrapy.Request(url=leader_board_url, callback=self.parseLeaderBoard)

        if len(datas) > 0 and self.offset < 3:
            self.offset = self.offset + 2
            yield scrapy.Request(url=self.problems_api.format(self.offset), callback=self.parse)

    def parseProblems(self, response):
        data = response.css(
            "div.challenge_problem_statement div.hackdown-content").css('p, ul').css('::text').extract()

        problemStatement = ' '.join(data).replace('\n', '')
        problemStatement = ' '.join(problemStatement.split())

        data = response.css(
            "div.challenge_sample_input div.hackdown-content").css('pre').css('::text').extract()

        inputStatement = ' '.join(data)
        inputStatement = ' '.join(inputStatement.split())

        data = response.css(
            "div.challenge_sample_output div.hackdown-content").css('pre').css('::text').extract()

        outputStatement = ' '.join(data)
        outputStatement = ' '.join(inputStatement.split())

        yield {
            'sample_input': inputStatement,
            'sample_output': outputStatement,
            'problems': problemStatement
        }

    def parseLeaderBoard(self, response):
        datas = response.css('a[data-action="hacker-modal"]')
        for data in datas:
            username = data.css('::attr(username)').extract_first()
            rank = data.css('::attr(data-attr8)').extract_first()
            score = data.css('::attr(data-attr10)').extract_first()
            yield {
                'username': username,
                'rank': rank,
                'score': score
            }
