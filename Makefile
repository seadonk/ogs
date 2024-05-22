run:
	scrapy crawl ogs -O output.json
sort-data:
	python3 sort_data.py