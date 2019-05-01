from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView
from bs4 import BeautifulSoup
import requests
import time


class NewsView(ListView):
    baseUrl =  'https://www.ukrinform.net/rubric-society?page-'

    def getDateTimeHeaderContent(self, news, dateFrom, dateTo):
        newsUrl = news.find('a')['href']
        newsHeader = news.find('a').find('img')['alt']
        newsDateTime = news.find('time')['datetime']
        date = time.strptime(newsDateTime.rsplit('T', 1)[0], "%Y-%m-%d")
        newsContent = news.find('p').text
        if date > dateTo:
            return []
        if dateFrom > date:
            return False
        return [newsUrl, newsHeader, newsDateTime, newsContent]

    def parsePage(self, currentUrl, dateFrom, dateTo):
        url = currentUrl
        r = requests.get(url)
        text = r.text
        soup = BeautifulSoup(text, 'lxml')
        result = []
        for news in soup('article'):
            item = self.getDateTimeHeaderContent(news, dateFrom, dateTo)
            if item == False:
                return[result, False]
            if (len(item) > 0):
                result.append(item)
        return [result, True]

    def parseNews(self, dateFrom, dateTo):
        baseUrl = self.baseUrl
        iterator = 1
        currentUrl = baseUrl + str(iterator)
        currentPageParsedResult = self.parsePage(currentUrl, dateFrom, dateTo)
        result = []
        while currentPageParsedResult[1] == True:
            result += currentPageParsedResult[0]
            iterator += 1
            currentUrl = baseUrl + str(iterator)
            currentPageParsedResult = self.parsePage(currentUrl, dateFrom, dateTo)
        result += currentPageParsedResult[0]
        return result

    def get(self, request,  **kwargs):
        dateFrom = self.request.GET.get('dateFrom')
        dateTo = self.request.GET.get('dateTo')
        return HttpResponse(self.parseNews(dateFrom, dateTo))