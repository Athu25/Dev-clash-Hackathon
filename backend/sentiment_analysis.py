import nltk
import requests
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Download VADER lexicon if not already
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

NEWS_API_KEY = "Yd88424f868f649c7b4dfd9a029f5279f"  
def get_news_headlines(stock_symbol, date):
    """
    Fetches top news headlines for a given stock on a specific date using NewsAPI.
    """
    from_date = date
    to_date = date + timedelta(days=1)  # To cover entire day span

    url = (
        f'https://newsapi.org/v2/everything?'
        f'q={stock_symbol}&'
        f'from={from_date}&to={to_date}&'
        f'sortBy=publishedAt&language=en&'
        f'apiKey={NEWS_API_KEY}'
    )

    response = requests.get(url)
    articles = response.json().get('articles', [])
    return [article['title'] for article in articles[:5]]  # Return top 5 headlines

def get_average_sentiment(headlines):
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(headline)['compound'] for headline in headlines]
    return sum(scores) / len(scores) if scores else 0.0

def get_sentiment_score(stock_symbol='AAPL', date=None):
    """
    Returns average sentiment score for given stock symbol on a specific date.
    """
    try:
        if date is None:
            from datetime import date as dt
            date = dt.today()
        headlines = get_news_headlines(stock_symbol, date)
        return get_average_sentiment(headlines)
    except Exception as e:
        print(f"Sentiment fetch error: {e}")
        return 0.0
