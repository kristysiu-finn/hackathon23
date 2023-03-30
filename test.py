import requests
from utils import text_to_docs, embed_docs, search_docs, get_answer
from bs4 import BeautifulSoup


url = 'https://www.becu.org/everyday-banking/credit-card/cash-back-visa'
response = requests.get(url) 
soup = BeautifulSoup(response.content, 'html.parser') 
    
doc = soup.get_text()
# doc = 'BECU offers a low-rate, traditional Visa credit card and a Cash Back Visa rewards credit card that offers 1.5% cash back on every purchase. BECU also offers affinity card options. To see the full list of credit card products, visit our Credit Card page.'

query = 'what are the benefits of the cashback credit card?'

text = text_to_docs(doc)

print('Indexing document... This may take a while⏳')
index = embed_docs(text)

print('Searching docs')
sources = search_docs(index, query)

print('Getting answer')
answer = get_answer(sources, query)

print("Answer: ", answer)