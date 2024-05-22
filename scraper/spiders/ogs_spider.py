import os
import scrapy
from urllib.parse import urlparse, parse_qs


class OgsSpider(scrapy.Spider):
    name = 'scraper'
    root_url = 'https://meetings.boardbook.org'
    org = 1240
    document_base = "https://meetings.boardbook.org/Documents/DownloadPDF/"
    start_urls = [
        'https://meetings.boardbook.org/Public/Organization/1240'
    ]
    count = 0

    def parse(self, response):
        rows = response.css('tr.row-for-board')
        for row in rows:
            meeting = row.css('td div::text').get().strip()
            location = row.css('td:nth-child(2)')
            details = row.css('td:nth-child(3)')
            agenda = (details.css('a[href^="/Public/Agenda"]::attr(href)').get() or '').strip() or None
            minutes = (details.css('a[href^="/Public/Minutes"]::attr(href)').get() or '').strip() or None
            # this is the same as recorded anyway
            # streaming = (location.css('a:contains("Streaming Meeting")::attr(href)').get() or '').strip() or None
            video = (location.css('a:contains("Recorded Meeting")::attr(href)').get() or '').strip() or None
            meeting_number = None
            if agenda is not None:
                # Parse the URL
                parsed_url = urlparse(agenda)
                # Extract the query string parameters
                params = parse_qs(parsed_url.query)
                # Get the 'meeting' parameter value as a number
                meeting_number = int(params['meeting'][0])
                agenda = self.root_url + agenda
            if minutes is not None:
                minutes = self.root_url + minutes

            meta = {
                'meeting': meeting,
                'agenda': agenda,
                'video': video,
                'minutes': minutes,
                'meeting_number': meeting_number
            }

            if minutes is not None:
                yield scrapy.Request(minutes, callback=self.parse_minutes, meta={'data': meta})
            else:
                yield meta


    def parse_minutes(self, response):
        document_id = response.css('input#NewDocumentViewerDocumentID::attr(value)').get()
        url = f"{self.document_base}{document_id}?org={self.org}"
        meta = response.meta['data']
        meta['minutes_link'] = url
        meta['minutes_id'] = document_id
        yield meta
        yield scrapy.Request(url, callback=self.download_pdf, meta={'document_id': document_id})

    def download_pdf(self, response):
        document_id = response.meta['document_id']
        # Ensure the 'minutes' directory exists
        if not os.path.exists('output/minutes'):
            os.makedirs('output/minutes')
        # Save the file in the 'minutes' directory
        with open(f'minutes/{document_id}.pdf', 'wb') as f:
            f.write(response.body)