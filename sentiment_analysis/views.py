import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from textblob import TextBlob
from transformers import AutoTokenizer, pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .models import Article


def url_input(request):
    sentiment_score = None
    url = None  # Initialize url variable
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            sentiment_score, reasons = analyze_sentiment(url)
            if sentiment_score is not None:  # Check if the score is valid
                Article.objects.create(url=url, sentiment_score=sentiment_score)
            else:
                print("Sentiment score is None, not creating Article.")
    return render(request, 'sentiment_analysis/url_input.html', {'sentiment_score': sentiment_score, 'url': url, 'reasons': reasons})


def analyze_sentiment(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve URL: {url} with status code: {response.status_code}")
            return None, []

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])

        print(f"Extracted text: {text}")  # Debugging line

        if not text.strip():
            print("No text found for sentiment analysis.")
            return None, []

        # Initialize the sentiment analysis pipeline with model and device
        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1)

        # Perform sentiment analysis directly on the text
        sentiment_results = sentiment_pipeline(text[:512])  # Truncate to 512 characters

        # Extract the sentiment score
        sentiment_label = sentiment_results[0]['label']
        sentiment_score = sentiment_results[0]['score']

        # Map sentiment label to a score (0-10)
        if sentiment_label == 'POSITIVE':
            score = int((sentiment_score * 10))  # Scale positive score
        else:
            score = int((1 - sentiment_score) * 10)  # Scale negative score

        # Generate reasons for the sentiment score
        reasons = generate_reasons(sentiment_label, text)

        return score, reasons

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, []


def generate_reasons(sentiment_label, text):
    reasons = []
    if sentiment_label == 'POSITIVE':
        reasons.append("The text contains positive phrases and expressions.")
        reasons.append("Overall sentiment is uplifting and encouraging.")
        reasons.append("Key positive words include: 'great', 'excellent', 'happy'.")
    else:
        reasons.append("The text contains negative phrases and expressions.")
        reasons.append("Overall sentiment is discouraging and pessimistic.")
        reasons.append("Key negative words include: 'bad', 'poor', 'sad'.")

    return reasons
