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
    id = scrapy.Field()
    name = scrapy.Field()
    success_ratio = scrapy.Field()
    max_score = scrapy.Field()
    difficulty_name = scrapy.Field()

class ProblemDetail(scrapy.Item):
    id = scrapy.Field()
    problem = scrapy.Field()
    sample_input = scrapy.Field()
    sample_output = scrapy.Field()
    pl_id = scrapy.Field()

class Leader(scrapy.Item):
    id = scrapy.Field()
    username = scrapy.Field()
    rank = scrapy.Field()
    score = scrapy.Field()
    pl_id = scrapy.Field()