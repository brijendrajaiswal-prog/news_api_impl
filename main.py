import requests
from send_email import send_email
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY =  os.getenv("GOOGLE_API_KEY")
api_key = os.getenv("API_KEY")
url = "https://newsapi.org/v2/everything?q=tesla&" \
      "sortBy=publishedAt&apiKey=" \
      "890603a55bfa47048e4490069ebee18c"

# Make request
request = requests.get(url)

# Get a dictionary with data
content = request.json()
print((content))
articles = content["articles"]
print(type(content))
print(articles)


# AI Sumarizing the news
model = init_chat_model(
    model="gemini-3-flash-preview",   # correct model name
    model_provider="google_genai",
    google_api_key=GOOGLE_API_KEY
)

prompt = f"""
    Summary of news,
    Write a short paragraph summarizing the news article,
    Provide impact on share market,
    Provide the business impact{articles}
"""

response = model.invoke(prompt)
response_str = response.content
print(response_str)

# Access the article titles and description
body = ""
for article in content["articles"]:
    if article["title"] is not None:
        body = body + article["title"] + "\n" + str(article["description"]) + 2*"\n"

body = ("Subject : New News\n\n"+ body).encode("utf-8")
send_email(message=body)