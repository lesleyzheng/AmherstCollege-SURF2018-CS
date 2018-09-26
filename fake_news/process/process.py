import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import string
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import dateparser
from word2number import w2n
from multiprocessing import Pool
import time
from collections import defaultdict
import collections

# create sorted list
def extract_info(X):
    '''
    A function to extract a lot of information from an article by calling various functions on it.
        Uses NLTK and regex to get lingustic information.
    :param X: A list with five columns: an index, a unique ID, a title of an article,
        the full original text of the article, and a cleaned version of the article
        (stripped of punctuation and made lower-case).
    :return: A list containing richer information about the article passed in, including
        the different parts of speech it contains, how many words it has, etc.
    '''

    temp_list = []

    # uid
    temp_list.append(X[1])  # temp_list[0]

    ## TITLE
    if X[2] == 'NaN' or isinstance(X[2], float) or len(X[2]) == 0:
        # add 10 empty lists
        for i in range(6):  # temp_list[1], 2, 3, 4, 5, 6
            temp_list.append([])
        temp_list.append(defaultdict(list))  # temp_list[7]
        temp_list.append([])  # temp_list[8]
        temp_list.append([])  # temp_list[9]
        temp_list.append(defaultdict(int))  # temp_list[10]
    else:
        # raw and clean title
        ti_di = X[2]
        ti_cl = cleaning(X[2])
        temp_list.append(ti_di)  # temp_list[1]
        temp_list.append(ti_cl)  # temp_list[2]

        # tokenize title by word
        ti_di_to = word_tokenize(ti_di)
        ti_cl_to = word_tokenize(ti_cl)
        temp_list.append(ti_di_to)  # temp_list[3]
        temp_list.append(ti_cl_to)  # temp_list[4]

        # number of letters in each word of title
        # we're using the clean title so it only includes full words (not numbers, punctuation, etc)
        letter_per_word = something_per_somethingelse(ti_cl_to)
        temp_list.append(letter_per_word[0])  # list of letters in each word      # temp_list[5]

        # part of speech tagging for title
        ti_di_to_tag = nltk.pos_tag(ti_di_to)
        temp_list.append(ti_di_to_tag)  # temp_list[6]

        # dict of different parts of speech
        pos_list = pos_analysis(ti_di_to_tag)
        temp_list.append(pos_list)  # this is temp_list[7]

        # named entity recognition (NER) for title

        ##TAKE INTO ACCOUNT USELESS TITLES
        ti_di_to_tag_ne = NE_recognition([ti_di_to_tag])
        temp_list.append(ti_di_to_tag_ne)  # temp_list[8]

        # get list of named entities
        NES = getNEinfo(ti_di_to_tag_ne)
        temp_list[7]["PLACES"] = NES[0]
        temp_list[7]["PEOPLE"] = NES[1]
        temp_list[7]["ORGS"] = NES[2]

        # money value extraction
        t_money = findMoney(ti_di)
        temp_list[7]["MONEY"] = t_money

        # percentage value extraction
        t_pcts = findPercents(ti_di)
        temp_list[7]["PERCENTS"] = t_pcts

        # date and number extraction
        t_dates = findValidDates(ti_di)
        temp_list[7]["DATES"] = t_dates

        # sentiment analysis
        t_sent = sentiment(ti_di)
        temp_list.append(t_sent)  # temp_list[9]

        # bag of words
        words = defaultdict(int)
        for word in ti_cl_to:
            words[word] += 1
        temp_list.append(words)  # temp_list[10]

    ## CONTENT
    # raw and clean content
    co_di = X[3]
    co_cl = X[4]
    temp_list.append(co_di)  # temp_list[11]
    temp_list.append(co_cl)  # temp_list[12]

    # tokenize content by word and sentence
    co_di_to = word_tokenize(co_di)
    co_cl_to = word_tokenize(co_cl)
    co_di_sent_to = sent_tokenize(co_di)
    co_di_sent_word_to = []
    for sent in co_di_sent_to:
        co_di_sent_word_to.append(nltk.word_tokenize(sent))  ## double check that this is correct
    temp_list.append(co_di_to)  # temp_list[13]
    temp_list.append(co_cl_to)  # temp_list[14]
    temp_list.append(co_di_sent_to)  # temp_list[15]
    temp_list.append(co_di_sent_word_to)  # temp_list[16]

    # number of letters in each word of the article
    # we're using the clean article so it only includes full words (not numbers, punctuation, etc)
    letter_per_word = something_per_somethingelse(co_cl_to)
    temp_list.append(letter_per_word[0])  # list of letters in each word             # temp_list[17]

    # number of words in each sentence of the article
    # this includes some junk because it includes punctuation, numbers, etc
    word_per_sent = something_per_somethingelse(co_di_sent_word_to)
    temp_list.append(word_per_sent[0])  # list of #s            # temp_list[18]

    # part of speech tagging for content
    ## wanna tokenize by sentence and word
    co_di_to_pos = nltk.pos_tag(co_di_to)
    temp_list.append(co_di_to_pos)  # temp_list[19]
    co_di_to_tag = []
    for sent in co_di_sent_word_to:
        co_di_to_tag.append(nltk.pos_tag(sent))
    temp_list.append(co_di_to_tag)  # temp_list[20]

    # dict of different parts of speech
    c_pos_dict = pos_analysis(co_di_to_pos)
    temp_list.append(c_pos_dict)  # this is temp_list[21]

    # list of diff words and number of times they appear as respective POS
    temp_list.append(word_pos_analysis(co_di_to_pos))  # temp_list[22]

    # NER for content
    co_di_ne_tag = NE_recognition(co_di_to_tag)
    temp_list.append(co_di_ne_tag)  # temp_list[23]

    NES = getNEinfo(co_di_ne_tag)
    temp_list[21]["PLACES"] = NES[0]
    temp_list[21]["PEOPLE"] = NES[1]
    temp_list[21]["ORGS"] = NES[2]

    # money value extraction
    c_money = findMoney(co_di)
    temp_list[21]["MONEY"] = c_money

    # percentage value extraction
    c_pcts = findPercents(co_di)
    temp_list[21]["PERCENTS"] = c_pcts

    # date and number extraction
    c_dates = findValidDates(co_di)
    temp_list[21]["DATES"] = c_dates

    # sentiment analysis (p.1)
    c_sent = sentiment(co_di)
    temp_list.append(c_sent)  # temp_list[24]

    # quotes
    quotes = re.findall("\".*?\"", co_di)
    temp_list[21]["QUOTES"] = quotes

    # expletives analysis; returns list of expletives that appear in an article
    co_cl_to_expletives = expletives_analysis(co_cl_to)
    temp_list[21]["EXPLETIVES"] = co_cl_to_expletives

    # bag of words model
    words_co = defaultdict(int)
    for word in co_cl_to:
        words_co[word] += 1
    temp_list.append(words_co)  # temp_list[25]

    return temp_list


def cleaning(text):
    text = text.lower()
    table = str.maketrans('', '', string.punctuation)
    stripped = text.translate(table)
    return stripped
    # stop_words = stopwords.words('english')


def NE_recognition(text):
    '''
    returns a list of lists (where each element is a sentence) of tuples (where each tuple is a word in the sentence and its POS tag)
    '''
    processed_article = nltk.Text(text)
    to_return = []
    for p in processed_article:
        t = nltk.ne_chunk(p)
        to_return.append(t)
    return to_return


def something_per_somethingelse(text):
    if text == 'NaN' or isinstance(text, float) or len(text) == 0:
        return [0, 0]
    to_return = []
    avg = 0
    for word in text:
        to_return.append(len(word))
        avg += len(word)
    return [to_return, avg / len(text)]


def getNEinfo(list):
    PLACES = []
    PEOPLE = []
    ORGS = []
    for sentence in list:
        for chunk in sentence:
            if hasattr(chunk, 'label'):
                if chunk.label() == 'GPE' or chunk.label() == 'LOCATION' or chunk.label() == 'FACILITY':
                    PLACES.append(' '.join(c[0] for c in chunk))
                if chunk.label() == 'PERSON':
                    PEOPLE.append(' '.join(c[0] for c in chunk))
                if chunk.label() == 'ORGANIZATION':
                    ORGS.append(' '.join(c[0] for c in chunk))
    return [PLACES, PEOPLE, ORGS]


def pos_analysis(tagged_tokens):
    pos_dict = collections.defaultdict(list)
    for k, v in tagged_tokens:
        pos_dict[v].append(k)
    # print(pos_dict)
    return pos_dict

    '''
    issues:
    1. ", [, <, ], > becomes default tag NN (did not identify pos beyond WRB)
    '''


def word_pos_analysis(tagged_tokens):
    word_pos_dict = collections.defaultdict(list)
    for k, v in tagged_tokens:
        d = collections.defaultdict(int)
        for value in v:
            d[value] += 1
        word_pos_dict[k] = d
    # print(word_pos_dict)
    return word_pos_dict


def sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    sents = []
    sents.append(score['pos'])
    sents.append(score['neu'])
    sents.append(score['neg'])
    sents.append(score['compound'])
    return sents


def findValidDates(str):
    dates = []
    dates.extend(re.findall(r'\d{1,2}[-/\.]\d{1,2}[-/\.]\d{4}', str))  # mm/dd/yyyy format
    dates.extend(re.findall(r'\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2}(?=[\s\.,)])', str))  # mm/dd/yy format
    dates.extend(
        re.findall(r'\d{4}[/\.]\d{1,2}[-/\.]\d{1,2}', str))  # yyyy/dd/mm or yyyy/mm/dd format
    dates.extend(
        re.findall(r'(?<=[\s\.,(])\d{2}[/\.]\d{1,2}[-/\.]\d{1,2}', str))  # yy/dd/mm or yy/mm/dd format
    dates.extend(
        re.findall(r'(?<=[\s\.,(])\d{1,2}/[0-3][0-9](?=[\s\., )])', str))  # mm/dd format
    dates.extend(
        re.findall(r'(?<=[iI]n\s)[12][0-9]{3}', str))  # in YYYY format, either in 1000's or 2000's, preceded by "in"
    exp = re.findall(r'([jJ]an|[jJ]anuary|'
                     r'[fF]eb|[fF]ebruary|'
                     r'[mM]ar|[mM]arch|'
                     r'[aA]pr|[aA]pril|'
                     r'[mM]ay|[jJ]un|[jJ]une|'
                     r'[jJ]ul|[jJ]uly|'
                     r'[aA]ug|[aA]ugust|'
                     r'[sS]ep|[sS]eptember|'
                     r'[oO]ct|[oO]ctober|'
                     r'[nN]ov|[nN]ovember|'
                     r'[dD]ec|[dD]ecember)'
                     r'(\s+)([0-2][0-9]|3[0-1]|0?[1-9])'
                     r'(\s|st|nd|rd|th|)'
                     r'(\.|,|\s)'
                     r'(\s*(?:[12][0-9]{3}|\'[0-9]{2})|)', str)
    for e in exp:
        dates.extend([''.join(e)])
    valid_dates = []
    for d in dates:
        date = dateparser.parse(d)
        if date != None:
            valid_dates.append(date)
    return valid_dates


def findPercents(str):
    percents = []
    percents.extend(re.findall(r'[0-9]+%', str))
    percents.extend(re.findall(r'[0-9]+\spct', str))
    percents.extend(re.findall(r'[0-9]+\spercent', str))
    wp = re.findall(r'([A-Za-z]+)(\s|)(%|pct|percent)', str)
    for w in wp:
        try:
            n = w2n.word_to_num(w[0])
            percents.append(''.join(w))
        except ValueError:
            pass
    return percents


def findMoney(str):
    money = []
    money.extend(re.findall(r'[\$¥¢£€][0-9]+', str))
    money.extend(re.findall(r'\[0-9]+(\s|)([\$¥¢£€]|dlrs|dollars|euro|yen|pounds)', str))
    wp = re.findall(r'([A-Za-z]+)(\s|)([\$¥¢£€]|dlrs|dollars|euro|yen|pounds)', str)
    wp.extend(re.findall(r'([\$¥¢£€])(\s|)([A-Za-z]+)', str))
    for w in wp:
        for d in w:
            try:
                n = w2n.word_to_num(d)
                money.append(''.join(w))
            except ValueError:
                pass
    return money


def expletives_analysis(co_cl_to):
    expletives = set(
        ['shit', 'fuck', 'damn', 'bitch', 'crap', 'piss', 'dick', 'darn', 'cock', 'pussy', 'asshole', 'fag', 'liar',
         'jackass', 'bastard', 'slut', 'douche', 'cunt', 'ass', 'arsehole', 'motherfucker', 'nigga', 'nigger',
         'faggot', 'whore', 'chinc', 'bullshitter', 'fucking', 'asshole'])
    co_cl_to_expletives = []
    for w in co_cl_to:
        if w in expletives:
            co_cl_to_expletives.append(w)
    return co_cl_to_expletives


if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('vader_lexicon')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    finn = "./data/FakeNewsData.pkl"
    fin = open(finn, "rb")  # read, byte format
    (X, Y), desc = pickle.load(fin)  # de-serialize a data stream; to serialize, call dumps()

    # execute
    for i in range(130):
        start = time.time()
        l = []
        front = (1000 * i)
        back = front + 1000
        for j in range(front, back):
            if j >= len(X):
                break
            l.append(X[j])
        p = Pool(processes=4)
        sorted = p.map(extract_info, l)
        pickle_desc = f"Data file with indeces {front} to {back}"
        pickle_out = open(f'./data/process_{front}-{back}.pkl', 'wb')
        pickle.dump((sorted, pickle_desc), pickle_out)
        pickle_out.close()
        end = time.time()
        print(f"Dumped articles {front}-{back}. Took {end-start} seconds")


