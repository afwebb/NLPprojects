import bs4 as bs
import urllib.request
import re
import nltk
import sys

topicName = sys.argv[1]

#Read in some data
scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/'+topicName)
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text

# Remove Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

#tokenize sentences
sentence_list = nltk.sent_tokenize(article_text)

stopwords = nltk.corpus.stopwords.words('english')
print(stopwords)

#find the frequency of each word
word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

#normalize frequencies
maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


#calculate scores for each sentence
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

#find the top 7 sentences
import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

#Generally good to include the intro sentence. Add it if its not already there
#if sentence_list[0] not in summary_sentences:
summary_sentences.insert(0, sentence_list[0])

summary = ' '.join(summary_sentences)

#write output to a file
output = open(topicName+'.txt', 'w')
output.write(summary)
output.close()
