from nltk import bigrams, trigrams
from nltk import word_tokenize
from nltk.corpus import reuters
from collections import Counter, defaultdict
import sys
import random

#placeholder
model = defaultdict(lambda: defaultdict(lambda:0))

#calculate word frequency, trigram frequency
for sentence in reuters.sents():
    for w1, w2, w3 in trigrams(sentence, pad_left=True, pad_right=True):
        model[(w1,w2)][w3]+=1

for w12 in model:
    total = float(sum(model[w12].values()))
    for w3 in model[w12]:
        model[w12][w3] /= total

#I want to exclude numbers from the result. Just not interested in those being included
nums = [str(i) for i in range(10)]

def genSentence(sentence):
    sentence = sentence.split(' ')
    finished = False

    while not finished and len(sentence)<30:
        #random threshold probability
        r = random.random()
        prob = 0.
        
        for word in model[tuple(sentence[-2:])].keys():
            prob+=model[tuple(sentence[-2:])][word]
            if prob>r:
                if not word or not any(w in nums for w in word): #ignore numbers
                    sentence.append(word)
                    break
        
        if sentence[-2:] == [None, None]:
            finished = True

    return sentence[:-2]


startSentence = sys.argv[1]

genWords = open("generatedSentences.txt", "a")
genWords.write('Starting words: '+startSentence+'\n')
for i in range(5):
    genSent = genSentence(startSentence)
    print(genSent)
    genWords.write(' '.join(genSent)+'\n')
genWords.write('\n')
genWords.close()
