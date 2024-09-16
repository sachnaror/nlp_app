import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from textblob import TextBlob
from transformers import AutoTokenizer, pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

from .models import Article


def url_input(request):
    sentiment_score = None
    url = None  # Initialize url variable
    reasons = []  # Initialize 'reasons' with a default value

    # Clear session or cookie on refresh
    if request.method == 'GET':
        request.session.flush()  # Clear session data
        # Optionally, clear cookies if needed
        # response.delete_cookie('cookie_name')

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

        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1)
        sentiment_results = sentiment_pipeline(text[:512])  # Truncate to 512 characters

        sentiment_label = sentiment_results[0]['label']
        sentiment_score = sentiment_results[0]['score']

        if sentiment_label == 'POSITIVE':
            score = int((sentiment_score * 10))
        else:
            score = int((1 - sentiment_score) * 10)

        reasons = generate_reasons(sentiment_label, text)

        return score, reasons

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, []


def generate_reasons(sentiment_label, text):
    reasons = []
    numbers = extract_numbers(text)

    if sentiment_label == 'POSITIVE':
        reasons.append("The text contains positive phrases and expressions.")
        reasons.append("Overall sentiment is uplifting and encouraging.")
        if numbers:
            reasons.append(f"Positive data points include: {', '.join(numbers)}.")
    else:
        reasons.append("The text contains negative phrases and expressions.")
        reasons.append("Overall sentiment is discouraging and pessimistic.")
        if numbers:
            reasons.append(f"Negative data points include: {', '.join(numbers)}.")

    return reasons


def extract_numbers(text):
    # Find all numbers in the text (including decimals)
    number_pattern = r'\b\d+(\.\d+)?\b'
    return re.findall(number_pattern, text)
