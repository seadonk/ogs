import scrapy
from scrapy.exceptions import CloseSpider


class OgsSpider(scrapy.Spider):
    name = 'ogs'
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
            streaming = (location.css('a:contains("Streaming Meeting")::attr(href)').get() or '').strip() or None
            recorded = (location.css('a:contains("Recorded Meeting")::attr(href)').get() or '').strip() or None

            if agenda is not None:
                agenda = self.root_url + agenda
            if minutes is not None:
                minutes = self.root_url + minutes

            meta = {'meeting': meeting, 'agenda': agenda, 'streaming': streaming, 'recorded': recorded, 'minutes': minutes}

            if minutes is not None:
                yield scrapy.Request(minutes, callback=self.parse_minutes, meta=meta)
            else:
                yield meta


    def parse_minutes(self, response):
        document_id = response.css('input#NewDocumentViewerDocumentID::attr(value)').get()
        url = f"{self.document_base}{document_id}?org={self.org}"
        response.meta['minutes_link'] = url
        meta = {
            'meeting': response.meta['meeting'],
            'agenda': response.meta['agenda'],
            'streaming': response.meta['streaming'],
            'recorded': response.meta['recorded'],
            'minutes': response.meta['minutes'],
            'minutes_link': url
        }
        yield meta
