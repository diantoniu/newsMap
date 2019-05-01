from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView
from newsParser.views import *

import json
import argparse
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six
import sys


class NewsAnalyze(ListView):
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    def sentimentText(self, text):
        client = language.LanguageServiceClient()
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)
        result = client.analyze_sentiment(document).document_sentiment
        return result

    def entitySentimentText(self, text):
        """Detects entity sentiment in the provided text."""
        client = language.LanguageServiceClient()
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')
        document = types.Document(
            content=text.encode('utf-8'),
            type=enums.Document.Type.PLAIN_TEXT)
        # Detect and send native Python encoding to receive correct word offsets.
        encoding = enums.EncodingType.UTF32
        if sys.maxunicode == 65535:
            encoding = enums.EncodingType.UTF16
        result = client.analyze_entity_sentiment(document, encoding)
        return result

    def getLocations(self, analyzedEntitySentimentText):
        locations = []
        for entity in analyzedEntitySentimentText.entities:
            if (self.entity_type[entity.type] == self.entity_type[2]):
                for mention in entity.mentions:
                    if mention.type == 1:
                        locations.append(entity.name)
                        break;
        return locations

    def getLongLat(self, locations):
        lng = []
        lat = []
        for location in locations:
            try:
                res = requests.get(
                    'https://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&key=AIzaSyBzPyVG23yVhzErGaVupTqdBIfIq9AKxDQ')
                res = json.loads(res.text)
                lat.append(res['results'][0]['geometry']['location']['lat'])
                lng.append(res['results'][0]['geometry']['location']['lng'])
            except Exception:
                print("error")
        return [locations, lat, lng]

    def getParsedNews(self, dateFrom, dateTo):
        news = NewsView().parseNews(dateFrom, dateTo)
        analyzedTexts = []
        sentimentScore = []
        for n in news:
            analyzedTexts.append(self.entitySentimentText(n[1]))
            sentimentScore.append(self.sentimentText(n[3]).score)
        print("-------------------------")
        for i in range(0, len(news)):
            print(news[i][1] + " " + str(sentimentScore[i]))
        print("-------------------------")

        locations = []
        for i in analyzedTexts:
            locations.append(self.getLocations(i))

        longLat = []
        for i in range(0, len(locations)):
            longLat.append(self.getLongLat(locations[i]) + [sentimentScore[i]])

        return longLat

    def getLocationNameSize(self, dateFrom, dateTo):
        longLat = self.getParsedNews(dateFrom, dateTo)
        names = []
        lat = []
        lng = []
        size = []

        for i in longLat:
            for j in range(0, len(i[0])):
                if (i[0].count(i[0][j])) == 1 and (i[3] < 0):  # if there are no similar elements with the same score
                    names.append(i[0][j])
                    lat.append(i[1][j])
                    lng.append(i[2][j])
                    size.append(100 - (i[3] + 1) * 100)

        n = len(names)
        i = 0

        # here we check if there are no same elements with the same score
        while i < len(names):
            if (names[i] in names):
                for j in range(0, len(names)):
                    if i != j and names[i] == names[j] and size[i] <= size[j]:
                        del names[i]
                        del lat[i]
                        del lng[i]
                        del size[i]
                        i -= 1
                        n -= 1
                        break
            i += 1

        print(names)
        print(lat)
        print(lng)
        print(size)
        return [names, lat, lng, size]

    def get(self, request, **kwargs):
        print("hiefchi")
        return HttpResponse(self.getLocationNameSize())
