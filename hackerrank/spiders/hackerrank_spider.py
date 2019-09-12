import json
import scrapy
from hackerrank.items import ProblemList, ProblemDetail, Leader

class HackerrankScraper(scrapy.Spider):
    def __init__(self):
        self.offset = 0

    name = 'hackerrank'
    problems_api = "https://www.hackerrank.com/rest/contests/master/tracks/algorithms/challenges?offset={}&limit=50&track_login=true"
    start_urls = [problems_api.format(0)]

    def parse(self, response):
        items = ProblemList()
        datas = json.loads(response.text)["models"]

        for data in datas:
            problem_url = 'https://www.hackerrank.com/challenges/' + \
                data['slug'] + '/problem'
            leader_board_url = 'https://www.hackerrank.com/challenges/' + \
                data['slug'] + '/leaderboard?limit=100&page=1'

            items['name'] = data["name"],
            items['url'] = problem_url,
            items['success_ratio'] = data["success_ratio"]
            items['max_score'] = data["max_score"]
            items['difficulty_name'] = data["difficulty_name"]

            yield items

            yield scrapy.Request(url=problem_url, callback=self.parseProblems, cb_kwargs=dict(problem_name=data["name"]))
            # yield scrapy.Request(url=leader_board_url, callback=self.parseLeaderBoard, cb_kwargs=dict(problem_name=data["name"]))

        if len(datas) > 0:
            self.offset = self.offset + 50
            yield scrapy.Request(url=self.problems_api.format(self.offset), callback=self.parse)

    def parseProblems(self, response, problem_name):
        items = ProblemDetail()

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

        items['sample_input'] = inputStatement,
        items['sample_output'] = outputStatement,
        items['problem'] = problemStatement
        items['problem_name'] = problem_name

        yield items

    def parseLeaderBoard(self, response, problem_name):
        items = Leader()
        datas = response.css('a[data-action="hacker-modal"]')
        for data in datas:
            username = data.css('::attr(username)').extract_first()
            rank = data.css('::attr(data-attr8)').extract_first()
            score = data.css('::attr(data-attr10)').extract_first()
            items['username'] = username,
            items['rank'] = rank,
            items['score'] = score,
            yield items
