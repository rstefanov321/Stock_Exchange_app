import requests
from twilio.rest import Client

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


def send_message(arrow, title, description):
    # Twilio data
    account_sid = 'account_sid'
    auth_token = 'account token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"{STOCK}: {arrow} {round(diff_percent, 2)}%\nHeadline: {title}\nDescription: {description}",
        from_="sender_phone",
        to='recipient_phone',
    )

    print(message.status)


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
alpha_api_key = "api_key"

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": alpha_api_key,
}

# Get the data
url = "https://www.alphavantage.co/query"
r = requests.get(url, params=parameters)
r.raise_for_status()

# Extract the data
data = r.json()
daily = data["Time Series (Daily)"]
list_daily = list(daily)

# find the last 2 trading days
yesterday = daily[list_daily[0]]
b4_ystrdy = daily[list_daily[1]]

# their closing prices
close_ystrdy = float(yesterday["4. close"])
close_b4_ystrdy = float(b4_ystrdy["4. close"])

# and the % change for the day
diff = close_ystrdy - close_b4_ystrdy
diff_percent = (diff/close_b4_ystrdy)*100


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_api = "news_api"
news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": news_api,
    "sortBy": "relevancy"  # Optional

}
news_url = "https://newsapi.org/v2/everything"
news_r = requests.get(news_url, params=news_parameters)
news_r.raise_for_status()

news_data = news_r.json()

news_list = [news_data["articles"][i] for i in range(3)]
article_text = news_list[0]["title"]


if diff > 5 or diff < 5:
    if diff > 5:
        arrow = "⬆️"
    else:
        arrow = "⬇️"

    for i in range(3):
        title = news_list[i]['title']
        description = news_list[i]['description']
        print(f"Article title: {title}")
        print(f"Article description: {description}")
        send_message(arrow, title, description)

    print(f"The difference is over 5%: {round(diff_percent, 2)}%")


# Format of the SMS message:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

