import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline, AutoTokenizer

from .models import Article


def url_input(request):
    sentiment_score = None
    url = None  # Initialize url variable
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            sentiment_score = analyze_sentiment(url)
            if sentiment_score is not None:  # Check if the score is valid
                Article.objects.create(url=url, sentiment_score=sentiment_score)
            else:
                print("Sentiment score is None, not creating Article.")
    return render(request, 'sentiment_analysis/url_input.html', {'sentiment_score': sentiment_score, 'url': url})


def analyze_sentiment(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve URL: {url} with status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])

    print(f"Extracted text: {text}")  # Debugging line

    if not text.strip():
        print("No text found for sentiment analysis.")
        return None

    # Initialize the sentiment analysis pipeline
    sentiment_pipeline = pipeline("sentiment-analysis")

    # Perform sentiment analysis directly on the text
    sentiment_results = sentiment_pipeline(text)
    print(f"Sentiment results: {sentiment_results}")  # Debugging line

    # Extract the sentiment score
    sentiment_label = sentiment_results[0]['label']
    sentiment_score = sentiment_results[0]['score']

    # Map sentiment label to a score (0-10)
    if sentiment_label == 'POSITIVE':
        score = int((sentiment_score * 10))  # Scale positive score
    else:
        score = int((1 - sentiment_score) * 10)  # Scale negative score

    return score
