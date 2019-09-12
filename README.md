# Crawl data hackerrank

## Install

python : 3.5

scrapy

scrapy-user-agent

## Usage

scrapy crawl hackerrank

### Dataflow

1. Scraped data from hackerrank. Started with Problem_list: https://www.hackerrank.com/rest/contests/master/tracks/algorithms/challenges?offset=<from 0 to end>&limit=50&track_login=true  
2. With each data in Problem_list. Scraped data Problem: https://www.hackerrank.com/challenges/<problem_name>/problem and
top 100 Leader: https://www.hackerrank.com/challenges/<problem_name>/leaderboard  
3. Saved data to Item Containers 
4. Created database and inserted data into database

### Related file

hackerrank.py   (1,2)

items.py        (3)

pipeline.py     (4)

## Database

Using https://sqliteonline.com/ and import myhackerrank.db to view database 

