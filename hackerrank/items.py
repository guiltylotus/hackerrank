# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HackerrankItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProblemList(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    success_ratio = scrapy.Field()
    max_score = scrapy.Field()
    difficulty_name = scrapy.Field()

class ProblemDetail(scrapy.Item):
    problem = scrapy.Field()
    sample_input = scrapy.Field()
    sample_output = scrapy.Field()
    problem_name = scrapy.Field()

class Leader(scrapy.Item):
    username = scrapy.Field()
    rank = scrapy.Field()
    score = scrapy.Field()