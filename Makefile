scrape:
	scrapy crawl scraper -O output/output.json
sort-data:
	python3 sort_data.py
run: scrape sort-data
deploy:
    aws s3 sync output/* s3://60048-ogs