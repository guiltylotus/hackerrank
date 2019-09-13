import json
import scrapy
from hackerrank.items import ProblemList, ProblemDetail, Leader
import time

class HackerrankScraper(scrapy.Spider):

    def __init__(self):
        self.offset = 0
        self.count_problems = 0
        self.count_leaders = 0

    name = 'hackerrank'
    problems_api = 'https://www.hackerrank.com/rest/contests/master/tracks/algorithms/challenges?offset={}&limit=10&track_login=true'
    start_urls = [problems_api.format(0)]

    def parse(self, response):
        items = ProblemList()
        datas = json.loads(response.text)['models']

        for data in datas:
            problem_url = 'https://www.hackerrank.com/challenges/' + \
                data['slug'] + '/problem'
            leader_board_url = 'https://www.hackerrank.com/challenges/' + \
                data['slug'] + '/leaderboard?limit=100&page=1'

            items['name'] = data['name'],
            items['id'] = data['id'],
            items['success_ratio'] = data['success_ratio']
            items['max_score'] = data['max_score']
            items['difficulty_name'] = data['difficulty_name']

            yield items

            yield scrapy.Request(url=problem_url, callback=self.parse_problems, cb_kwargs=dict(pl_id=data['id']))
            yield scrapy.Request(url=leader_board_url, callback=self.parse_leader_board, cb_kwargs=dict(pl_id=data['id']))

        if len(datas) > 0:
            self.offset = self.offset + 10
            yield scrapy.Request(url=self.problems_api.format(self.offset), callback=self.parse)

    def parse_problems(self, response, pl_id):
        items = ProblemDetail()

        self.count_problems += 1
        data = response.css(
            'div.challenge_problem_statement div.hackdown-content').css('p, ul, pre').css('::text').extract()

        problem_statement = ' '.join(data).replace('\n', '')
        problem_statement = ' '.join(problem_statement.split())

        data = response.css(
            'div.challenge_sample_input div.hackdown-content').css('pre').css('::text').extract()

        input_statement = ' '.join(data)
        input_statement = ' '.join(input_statement.split())

        data = response.css(
            'div.challenge_sample_output div.hackdown-content').css('pre').css('::text').extract()

        output_statement = ' '.join(data)
        output_statement = ' '.join(output_statement.split())

        items['id'] = self.count_problems
        items['sample_input'] = input_statement,
        items['sample_output'] = output_statement,
        items['problem'] = problem_statement
        items['pl_id'] = pl_id

        yield items

    def parse_leader_board(self, response, pl_id):
        items = Leader()

        datas = response.css('a[data-action="hacker-modal"]')
        for data in datas:
            self.count_leaders += 1
            username = data.css('::attr(username)').extract_first()
            rank = data.css('::attr(data-attr8)').extract_first()
            score = data.css('::attr(data-attr10)').extract_first()
            
            items['id'] = self.count_leaders,
            items['username'] = username,
            items['rank'] = rank,
            items['score'] = score,
            items['pl_id'] = pl_id

            yield items
