# Sentiment Analysis Web Application

## Overview

This project is a Django web application that analyzes the sentiment of text extracted from a given URL. It utilizes various libraries such as `TextBlob`, `transformers`, and `VADER` to perform sentiment analysis and provide insights based on the content of the webpage.


[![Watch the video](https://img.youtube.com/vi/65basIlogT0/maxresdefault.jpg)](https://www.youtube.com/watch?v=65basIlogT0)

## Features

- Input a URL to analyze the sentiment of its content.
- Displays sentiment score and reasons for the sentiment.
- Utilizes multiple sentiment analysis models for accurate results.
- Handles session management to clear previous data on refresh.

## Technologies Used

- **Django**: Web framework for building the application.
- **Requests**: For making HTTP requests to fetch webpage content.
- **BeautifulSoup**: For parsing HTML and extracting text.
- **TextBlob**: For basic sentiment analysis.
- **Transformers**: For advanced sentiment analysis using pre-trained models.
- **VADER**: For sentiment analysis specifically tuned for social media text.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sentiment_analysis
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Django server:
   ```bash
   python manage.py runserver
   ```

5. Open your browser and navigate to `http://127.0.0.1:8000/`.

## Usage

1. Enter a valid URL in the input field.
2. Click the submit button to analyze the sentiment.
3. The application will display the sentiment score and reasons based on the content of the webpage.

## Code Explanation

### Main Functions

- **url_input(request)**: Handles GET and POST requests. On POST, it retrieves the URL, analyzes the sentiment, and saves the result in the database.

- **analyze_sentiment(url)**: Fetches the content from the provided URL, extracts text, and performs sentiment analysis using the `transformers` library. Returns the sentiment score and reasons.

- **generate_reasons(sentiment_label, text)**: Generates reasons for the sentiment based on the analysis results and any numbers found in the text.

- **extract_numbers(text)**: Uses regex to find and return all numbers present in the text.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


```

├── nlp_app/
│   ├── db.sqlite3
│   ├── README.md
│   ├── .env
│   ├── manage.py
│   ├── nlp_app/
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── sentiment_analysis/
│   │   ├── models.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │   ├── templates/
│   │   │   ├── sentiment_analysis/
│   │   │   │   └── url_input.html
