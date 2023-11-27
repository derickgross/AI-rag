import pandas as pd
import os
import tiktoken
import openai
import urllib.request
import json
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

urlData = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

request = urllib.request.Request(
    urlData,
    headers={
        "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
    }
)
webURL = urllib.request.urlopen(request)
raw_data = webURL.read()
data = json.loads(raw_data.decode())

  # Create a list to store the text files
texts=[]

season = data["events"][0]["season"]["year"]
week = data["events"][0]["week"]["number"]

for game in data["events"]:
  summary = ""

  teams = game["name"].split(" at ")
  road_team = teams[0]
  home_team = teams[1]
  home_score = game["competitions"][0]["competitors"][0]["score"]
  road_score = game["competitions"][0]["competitors"][1]["score"]

  summary += f"In week {week} of the {season} NFL season, the {home_team} hosted the {road_team}."
  if "winner" in game["competitions"][0]["competitors"][0].keys():
    if game["competitions"][0]["competitors"][0]["winner"]:
        summary += f" The {home_team} won the game, by a score of {home_score}-{road_score}."
    else:
        summary += f" The {road_team} won the game, by a score of {road_score}-{home_score}."
  else:
    summary += " The game is still in progress."
    if int(home_score) > int(road_score):
      summary += f" The {home_team} is leading by a score of {home_score}-{road_score}."
    if int(road_score) > int(home_score):
      summary += f" The {road_team} is leading by a score of {road_score}-{home_score}."
    if int(road_score) == int(home_score):
      summary += f" The score is tied at {home_score}."
#   for headline in game["headlines"]:


  texts.append(summary)

def remove_newlines(series):
  series = series.str.replace('\n', ' ')
  series = series.str.replace('\\n', ' ')
  series = series.str.replace('  ', ' ')
  series = series.str.replace('  ', ' ')
  return series

# Create a dataframe from the list of texts
df = pd.DataFrame(texts, columns=['text'])


# Set the text column to be the raw text with the newlines removed
df['text'] = remove_newlines(df.text)
df.to_csv('processed/scraped.csv')

# Load the cl100k_base tokenizer which is designed to work with the ada-002 model
tokenizer = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv('processed/scraped.csv', index_col=0)
df.columns = ['text']

# Tokenize the text and save the number of tokens to a new column
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

chunk_size = 1000  # Max number of tokens

text_splitter = RecursiveCharacterTextSplitter(
		# This could be replaced with a token counting function if needed
    length_function = len,  
    chunk_size = chunk_size,
    chunk_overlap  = 0,  # No overlap between chunks
    add_start_index = False,  # We don't need start index in this case
)

shortened = []

for row in df.iterrows():

  # If the text is None, go to the next row
  if row[1]['text'] is None:
    continue

  # If the number of tokens is greater than the max number of tokens, split the text into chunks
  if row[1]['n_tokens'] > chunk_size:
    # Split the text using LangChain's text splitter
    chunks = text_splitter.create_documents([row[1]['text']])
    # Append the content of each chunk to the 'shortened' list
    for chunk in chunks:
      shortened.append(chunk.page_content)

  # Otherwise, add the text to the list of shortened texts
  else:
    shortened.append(row[1]['text'])

df = pd.DataFrame(shortened, columns=['text'])
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])

df.to_csv('processed/embeddings2.csv')
