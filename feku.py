import httplib, urllib, base64, json

def bingNewsScrape(queryStr):
    #print "Query String:",queryStr
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'b75a18102b6b43d9bfa1b01fd9072f65',
    }

    params = urllib.urlencode({
        # Request parameters
        'q': queryStr,
        'count': '5',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/news/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        # print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


    jsonData = json.loads(data)
    url1 =  jsonData['value'][0]['url']
    url2 = jsonData['value'][1]['url']
    url3 = jsonData['value'][2]['url']
    url4 = jsonData['value'][3]['url']
    url5 = jsonData['value'][4]['url']
    

    urlList = [url1, url2, url3, url4, url5]

    return urlList

# Here are some imports that you'll need
import pandas as pd
import requests, json 
import math
import requests
from nltk.tokenize import SpaceTokenizer, WhitespaceTokenizer
from bs4 import BeautifulSoup
import string
import re
from newspaper import Article
    
def NormalizeContraction(text):
    text = text.replace("can't", "can not")
    text = text.replace("couldn't", "could not")
    text = text.replace("don't", "do not")
    text = text.replace("didn't", "did not")
    text = text.replace("doesn't", "does not")
    text = text.replace("shouldn't", "should not")
    text = text.replace("haven't", "have not")
    text = text.replace("aren't", "are not")
    text = text.replace("weren't", "were not")
    text = text.replace("wouldn't", "would not")
    text = text.replace("hasn't", "has not")
    text = text.replace("hadn't", "had not")
    text = text.replace("won't", "will not")
    text = text.replace("wasn't", "was not")
    text = text.replace("can't", "can not")
    text = text.replace("isn't", "is not")
    text = text.replace("ain't", "is not")
    text = text.replace("it's", "it is")
    text = text.replace("i'm", "i am")
    text = text.replace("i'm", "i am")
    text = text.replace("i've", "i have")
    text = text.replace("i'll", "i will")
    text = text.replace("i'd", "i would")
    text = text.replace("we've", "we have")
    text = text.replace("we'll", "we will")
    text = text.replace("we'd", "we would")
    text = text.replace("we're", "we are")
    text = text.replace("you've", "you have")
    text = text.replace("you'll", "you will")
    text = text.replace("you'd", "you would")
    text = text.replace("you're", "you are")
    text = text.replace("he'll", "he will")
    text = text.replace("he'd", "he would")
    text = text.replace("he's", "he has")
    text = text.replace("she'll", "she will")
    text = text.replace("she'd", "she would")
    text = text.replace("she's", "she has")
    text = text.replace("they've", "they have")
    text = text.replace("they'll", "they will")
    text = text.replace("they'd", "they would")
    text = text.replace("they're", "they are")
    text = text.replace("that'll", "that will")
    text = text.replace("that's", "that is")
    text = text.replace("there's", "there is")
    return text


def getArticleData(url):
    # Here are some imports that you'll need
    import pandas as pd
    import requests, json 
    import math
    import requests
    from nltk.tokenize import SpaceTokenizer, WhitespaceTokenizer
    from bs4 import BeautifulSoup
    import string
    import re
    from newspaper import Article
    
    article = Article(url)
    article.download()
    article.html
    article.parse()
    #print article

    try:
        r = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        text = re.sub(r, " URLURLURL", article.text)
        # Strip html tags
        soup = BeautifulSoup(text)
        for tag in soup.findAll(True):
            tag.replaceWithChildren()
            text = soup.get_text()
        # Normalize everything to lower case
        text = text.lower()
        # Strip line breaks and endings \r \n
        r = re.compile(r"[\r\n]+")
        text = re.sub(r, "", text)
        # get rid of em dashes
        # table = {
        #     ord(u'\u2018') : u"'",
        #     ord(u'\u2019') : u"'",
        #     ord(u'\u201C') : u'"',
        #     ord(u'\u201d') : u'"',
        #     ord(u'\u2026') : u'',
        #     ord(u'\u2014') : u'',
        # }
        # text = text.translate(table)

        # Normalize contractions
        # e.g. can't => can not, it's => it is, he'll => he will
        text = NormalizeContraction(text)

        # Strip punctuation (except for a few)
        punctuations = string.punctuation
        # includes following characters: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
        excluded_punctuations = ["$", "%"]
        for p in punctuations:
            if p not in excluded_punctuations:
                text = text.replace(p, " ")

        # Condense double spaces
        text = text.replace("  ", " ")
        text = article.text.encode('utf-8').strip()
        text = re.sub(r'[^\x00-\x7F]+',' ', text)
        title = article.title.encode('utf-8').strip()
        title = re.sub(r'[^\x00-\x7F]+',' ', title)
        return [text, title]
    except:
        print "error"
        
def get_wordnet_pos(pos_tag):
    import nltk.corpus
    import nltk.tokenize.punkt
    import nltk.stem.snowball
    from nltk.corpus import wordnet
    import string
    if pos_tag[1].startswith('J'):
        return (pos_tag[0], wordnet.ADJ)
    elif pos_tag[1].startswith('V'):
        return (pos_tag[0], wordnet.VERB)
    elif pos_tag[1].startswith('N'):
        return (pos_tag[0], wordnet.NOUN)
    elif pos_tag[1].startswith('R'):
        return (pos_tag[0], wordnet.ADV)
    else:
        return (pos_tag[0], wordnet.NOUN)
    
def is_ci_lemma_stopword_set_match(a, b, threshold=0.5):
    import re
    import nltk.corpus
    import nltk.tokenize.punkt
    import nltk.stem.snowball
    from nltk.corpus import wordnet
    import string
    
    tokenizer = nltk.tokenize.punkt.PunktWordTokenizer()
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    # Get default English stopwords and extend with punctuation
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(string.punctuation)
    stopwords.append('')
    
    """Check if a and b are matches."""
    pos_a = map(get_wordnet_pos, nltk.pos_tag(tokenizer.tokenize(a)))
    pos_b = map(get_wordnet_pos, nltk.pos_tag(tokenizer.tokenize(b)))
    lemmae_a = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_a \
                    if pos == wordnet.NOUN and token.lower().strip(string.punctuation) not in stopwords]
    lemmae_b = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_b \
                    if pos == wordnet.NOUN and token.lower().strip(string.punctuation) not in stopwords]

    # Calculate Jaccard similarity
    ratio = len(set(lemmae_a).intersection(lemmae_b)) / float(len(set(lemmae_a).union(lemmae_b)))
    return ratio

def extract_summary(text, ratio):
    import logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    from gensim.summarization import summarize
    return summarize(text,ratio)
    
def extract_keywords(text, ratio):
    import logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    from gensim.summarization import keywords
    return keywords(text, ratio)

#Score based on Tone analyzer
def tone_score(article):
    from watson_developer_cloud import ToneAnalyzerV3
    tone_analyzer = ToneAnalyzerV3(username='2566aaa5-7a15-47f7-bddf-983c8bf98157',password='74z52FIXmvxX',version='2016-05-19 ')
    import nltk
    import re
    d_tone_score = {}
    d={}
    rel_score=0.5

    tone_dict=tone_analyzer.tone(article)

    for j in range(len(tone_dict["document_tone"]["tone_categories"][0]["tones"])):
        d_tone_score[tone_dict["document_tone"]["tone_categories"][0]["tones"][j]["tone_name"]]=tone_dict["document_tone"]["tone_categories"][0]["tones"][j]["score"]

    d={k:v*100 for (k,v) in d_tone_score.items() if v > rel_score}
    tone_list = []
    for key,value in d.iteritems():
        tone_list.append(key)
        tone_list.append(value)
    return(tone_list)

#Calculate the opinion score for the article
def opi_score(article):
    sentence_count=0
    import nltk
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    from itertools import chain
    import pandas as pd
    from nltk.corpus import wordnet
    opinion = ["your two cents", "perhaps", "frankly", "personally","as far as I'm concerned", "so far as I'm concerned","to my way of thinking", "if you want my advice","if you want my opinion", "if you ask me", "to my mind", "I think","I believe", "I feel", "in my opinion", "my favorite", "the best",
        "I strongly believe", "from my point of view", "it's y belief",
        "based on what I know", "I am convinced", "speaking for myself",
        "I know you will have to", "agree that", "I am confident that",
        "first of all", "next", "after that", "equally important",
        "consequently", "besides", "further", "furthermore", "clearly",
        "obviously", "in addition", "for all these reasons", "finally",
        "in conclusion", "always", "never", "awful", "wonderful",
        "beautiful", "ugly", "better", "best", "worst", "delicious",
        "disgusting", "definitely", "enjoyable", "horrible", "favorite",
        "against", "good", "bad", "inferior", "superior", "oppose",
        "support", "terrible", "unfair", "worthwile", "possibly",
        "perchance", "maybe", "mayhap", "peradventure", "honestly",
        "candidly", "in person", "following", "adjacent",
        "side by side", "future", "succeeding", "accordingly",
        "therefore", "in any case", "too", "also", "likewise",
        "as well", "foster", "promote", "advance", "boost",
        "encourage", "farther", "far", "moreover", "what is more",
        "intelligibly", "understandably", "distinctly", "clear",
        "evidently", "manifestly", "patently", "apparently", "plainly",
        "plain", "eventually", "ultimately", "in the end", "at last",
        "at long last", "last", "lastly", "ever", 
        "constantly", "invariably", "forever", "perpetually",
        "incessantly", "atrocious", "abominable", "dreadful",
        "painful", "unspeakable", "dire", "direful", "dread",
        "dreaded", "fearful", "fearsome", "frightening", "horrendous",
        "horrific", "nasty", "awed", "frightful", "tremendous",
        "amazing", "awe-inspiring", "awesome", "awing", "terribly",
        "awfully", "frightfully", "fantastic", "grand", "howling",
        "marvelous", "marvellous", "rattling", "terrific", "wondrous",
        "surly", "despicable", "vile", "slimy", "unworthy",
        "worthless", "wretched", "horrifying", "bettor", "wagerer",
        "punter", "break", "improve", "amend", "ameliorate",
        "meliorate", "full", "estimable", "honorable", "respectable",
        "beneficial", "just", "upright", "adept", "expert",
        "practiced", "proficient", "skillful", "skilful", "dear",
        "near", "dependable", "safe", "secure", "right", "ripe",
        "well", "effective", "in effect", "in force", "serious",
        "sound", "salutary", "honest", "undecomposed", "unspoiled",
        "unspoilt", "easily", "considerably", "substantially",
        "intimately", "advantageously", "comfortably", "topper",
        "Best", "C. H. Best", "Charles Herbert Best", "outdo",
        "outflank", "trump", "scoop", "pip", "mop up", "whip",
        "rack up", "big", "tough", "spoiled", "spoilt", "regretful",
        "sorry", "uncollectible", "risky", "high-risk", "speculative",
        "unfit", "unsound", "forged", "defective", "Delicious",
        "delightful", "delectable", "luscious", "pleasant-tasting",
        "scrumptious", "toothsome", "yummy", "disgust", "gross out",
        "revolt", "repel", "nauseate", "sicken", "churn up",
        "disgustful", "distasteful", "foul", "loathly", "loathsome",
        "repellent", "repellant", "repelling", "revolting", "skanky",
        "wicked", "yucky", "decidedly", "unquestionably",
        "emphatically", "in spades", "by all odds", "gratifying",
        "pleasurable", "favourite", "darling", "pet", "dearie",
        "deary", "ducky", "front-runner", "favored", "best-loved",
        "preferred", "preferent", "goodness", "commodity",
        "trade good", "thoroughly", "soundly", "badness", "badly",
        "subscript", "deficient", "substandard", "higher-up",
        "superordinate", "victor", "master", "Lake Superior",
        "Superior", "superscript", "ranking", "higher-ranking",
        "fight", "fight back", "fight down", "defend",
        "counterbalance", "pit", "match", "play off", "react",
        "controvert", "contradict", "reinforcement", "reenforcement",
        "documentation", "keep", "livelihood", "living",
        "bread and butter", "sustenance", "supporting", "accompaniment",
        "musical accompaniment", "backup", "financial support",
        "funding", "backing", "financial backing", "back up", "back",
        "endorse", "indorse", "plump for", "plunk for", "hold",
        "sustain", "hold up", "confirm", "corroborate", "substantiate",
        "affirm", "subscribe", "underpin", "bear out", "fend for",
        "patronize", "patronise", "patronage", "keep going", "digest",
        "endure", "stick out", "stomach", "bear", "stand", "tolerate",
        "brook", "abide", "suffer", "put up", "severe", "unjust"]
    df=pd.DataFrame(opinion,columns=['Opinion_Words'])
    df['Opinion_Words'] = df['Opinion_Words'].str.replace("_"," ")
    opinion_words = df.Opinion_Words.unique()

    for i in range(len(tokenizer.tokenize(article))):
        sentence=tokenizer.tokenize(article)[i] #Split to sentences
        sentence=sentence.lower()
        for word in opinion_words:
            if word in sentence:
                sentence_count=sentence_count+1
                break

    opinion_score=float(sentence_count)/len(tokenizer.tokenize(article))
    return (opinion_score*100)

def get_indicators(article_url):
    article_data = getArticleData(article_url)
    from nltk.corpus import stopwords
    cachedStopWords = stopwords.words("english")
    article_title = ' '.join([word for word in article_data[1].split() if word not in cachedStopWords])
    article_data = getArticleData(article_url)
    similar_urls = bingNewsScrape(article_title)
    similar_data = []
    for i in similar_urls:
        t = getArticleData(i)
        similar_data.append(t)
    similar_urls = bingNewsScrape(article_title)
    similar_data = []
    for i in similar_urls:
        similar_data.append(getArticleData(i))
    article_sentences = article_data[0].split('\n')
    article_sentences = [x for x in article_sentences if x]
    import re
    for i in range(0,len(article_sentences)):
        article_sentences[i] = re.sub( '\s+', ' ', article_sentences[i]).strip()
    ratio = 0.4
    article_summary = str(extract_summary(article_data[0], ratio))
    article_keywords = str(extract_keywords(article_data[0], ratio))
    other_summary = []
    other_keyword = []
    count = 0
    for each_alternate_article in similar_data:
        #alt_article_sentences = each_alternate_article[0].split('\n')
        #alt_article_sentences = [x for x in alt_article_sentences if x]
        #t = ''.join(alt_article_sentences)
        #print ("---------------------")
        if count==3:
            break
        try:
            kw = extract_keywords(each_alternate_article[0],ratio)
            summary = extract_summary(each_alternate_article[0],ratio)
            count = count+1
            other_summary.append(summary)
            other_keyword.append(kw)
        except:
            continue
    average_summary_similarity = []
    average_keyword_similarity = []
    for i in range(0,3):
        #print i
        average_summary_similarity.append(is_ci_lemma_stopword_set_match(article_summary, other_summary[i]))
        average_keyword_similarity.append(is_ci_lemma_stopword_set_match(article_keywords, other_keyword[i]))
    average_summary_similarity = sorted(average_summary_similarity,reverse=True)
    average_keyword_similarity = sorted(average_keyword_similarity,reverse=True)
    net_summary_avg = (average_summary_similarity[0]*0.6+average_summary_similarity[1]*0.3+average_summary_similarity[2]*0.1)*100
    net_keyword_avg = (average_keyword_similarity[0]*0.6+average_keyword_similarity[1]*0.3+average_keyword_similarity[2]*0.1)*100
    tone_score_data = tone_score(article_data[0])
    opinion_score_data = opi_score(article_data[0])
    return net_summary_avg,net_keyword_avg, opinion_score_data, len(tone_score_data), tone_score_data


print get_indicators("http://www.nbcnews.com/news/us-news/trump-s-options-north-korea-include-placing-nukes-south-korea-n743571")