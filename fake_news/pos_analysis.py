'''Parts of Speech Analysis

POS KEY
CC	coordinating conjunction
CD	cardinal digit
DT	determiner
EX	existential there (like: "there is" ... think of it like "there exists")
FW	foreign word
IN	preposition/subordinating conjunction
JJ	adjective	'big'
JJR	adjective, comparative	'bigger'
JJS	adjective, superlative	'biggest'
LS	list marker	1)
MD	modal	could, will
NN	noun, singular 'desk'
NNS	noun plural	'desks'
NNP	proper noun, singular	'Harrison'
NNPS	proper noun, plural	'Americans'
PDT	predeterminer	'all the kids'
POS	possessive ending	parent's
PRP	personal pronoun	I, he, she
PRP$	possessive pronoun	my, his, hers
RB	adverb	very, silently,
RBR	adverb, comparative	better
RBS	adverb, superlative	best
RP	particle	give up
TO	to	go 'to' the store.
UH	interjection	errrrrrrrm
VB	verb, base form	take
VBD	verb, past tense	took
VBG	verb, gerund/present participle	taking
VBN	verb, past participle	taken
VBP	verb, sing. present, non-3d	take
VBZ	verb, 3rd person sing. present	takes
WDT	wh-determiner	which
WP	wh-pronoun	who, what
WP$	possessive wh-pronoun	whose
WRB	wh-abverb	where, when

'''

import matplotlib.pyplot as plt

def plot_pos(full_distr, zero_distr, one_distr):
    print("\t\t...in [plot_pos]...")

    figure = plt.figure(figsize=(10, 8))

    x = ['avg. # of pronouns', 'avg. # of nouns', 'avg. # of adjectives', 'avg. # of verbs', 'avg. # of foreign words']

    #title
    y1, y2, y3 = [], [], []
    for i in range(5):
        y1.append(full_distr[i])
        y2.append(zero_distr[i])
        y3.append(one_distr[i])

    ax = plt.subplot(211)
    ax.plot(x, y1, label="all news")
    ax.plot(x, y2, label="class 0 news")
    ax.plot(x, y3, label="class 1 news")
    ax.set_title("Title POS Distribution")
    plt.legend()

    #content
    z1, z2, z3 = [], [], []
    for i in range(5,10):
        z1.append(full_distr[i])
        z2.append(zero_distr[i])
        z3.append(one_distr[i])

    ax2 = plt.subplot(212)
    ax2.plot(x, z1, label="all news")
    ax2.plot(x, z2, label="class 0 news")
    ax2.plot(x, z3, label="class 1 news")
    ax2.set_title("Content POS Distribution")

    plt.legend()
    plt.show()