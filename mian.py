import argparse
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six
import sys


def sentimentText(text):
    """Detects sentiment in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    sentiment = client.analyze_sentiment(document).document_sentiment
    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))


# txt = '80 people were killed in chemical attack in north-western Syria'
# txt = 'USA attacked Syria'
txt = 'USA attacked Syria while Syria is supported by Russia'

sentimentText(txt)
