import nltk
import pronouncing
from urllib.request import Request, urlopen
from random import randint

def getRhymes(word):
    return pronouncing.rhymes(word.lower())


def isRhyme(word1, word2, rhymes):
    isPass = word2 in rhymes
    print("Do " + word2 + " and " + word1 + " rhyme? " + str(isPass))
    return isPass

def getSentences(fileName):
    if fileName[:4] == "http":
        req = Request(fileName, headers={'User-Agent': 'Mozilla/5.0'})
        data = urlopen(req).read().decode('utf-8', errors='replace')
    else:
        fp = open(fileName)
        data = fp.read()
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    final = []
    for sen in tokenizer.tokenize(data):
        final.append(sen.replace("\n"," "))
    return final

def isBase(foundCount):
    return foundCount % 2 == 0

def clean(s):
    s = s.rstrip('?:!.,;"\'')
    return s.lstrip('?:!.,;"\'')

def getLastWord(sen):
    lastWord = sen.split()[-1]
    lastWord = clean(lastWord)
    return lastWord.lower()

def senChecks(sen, rhymeWith, foundCount, SENTENCE_LENGTH, SENTENCE_THRESHOLD, RHYMES_THRESHOLD = 3):
    fitsLength = SENTENCE_LENGTH - SENTENCE_THRESHOLD <= len(sen.split()) \
           <= SENTENCE_LENGTH + SENTENCE_THRESHOLD
    lastWord = getLastWord(sen)
    rhymes = getRhymes(lastWord)

    if isBase(foundCount):
        return fitsLength and len(rhymes) > RHYMES_THRESHOLD
    else:
        return fitsLength and isRhyme(lastWord, rhymeWith, rhymes)

def randIndex(numSentences):
    return randint(0, numSentences)

def buildPoem(sentences, START_INDEX, TOTAL_LINES, SENTENCE_LENGTH, SENTENCE_TARGET):
    numSentences = len(sentences)
    if START_INDEX < 0 or START_INDEX > numSentences:
        START_INDEX = randIndex(numSentences)
    else:
        START_INDEX += (randIndex(numSentences-START_INDEX))

    foundCount = 0
    lastWord = ""
    final = ""

    for i in range(START_INDEX, len(sentences)):
        if not foundCount < TOTAL_LINES:
            break

        sen = sentences[i]
        # print("Checking " + sen)

        if senChecks(sen, lastWord, foundCount, SENTENCE_LENGTH, SENTENCE_TARGET):
            foundCount += 1
            lastWord = getLastWord(sen)
            print("Last Word: " + lastWord)
            final += clean("".join(sen)) + "<br>"
            if isBase(foundCount):
                final+="\n"

    if foundCount < TOTAL_LINES:
        final += "Could not complete."

    return final

def validateInput(URL, START_INDEX, TOTAL_LINES, SENTENCE_LENGTH, SENTENCE_THRESHOLD):

    START_INDEX = int(START_INDEX)
    TOTAL_LINES = int(TOTAL_LINES)
    SENTENCE_LENGTH = int(SENTENCE_LENGTH)
    SENTENCE_THRESHOLD = int(SENTENCE_THRESHOLD)

    if TOTAL_LINES < 0:
        TOTAL_LINES = 0
    if SENTENCE_LENGTH < 0:
        SENTENCE_LENGTH = 0
    if SENTENCE_THRESHOLD < 0:
        SENTENCE_THRESHOLD = 0

    print()
    print("File location: " + URL)
    print("Start index: " + str(START_INDEX))
    print("Target lines: " + str(TOTAL_LINES))
    print("Target sentence length: " + str(SENTENCE_LENGTH))
    print("Target sentence length threshold: " + str(SENTENCE_THRESHOLD))
    print()

    return {"si" : START_INDEX, "tl" : TOTAL_LINES, "sl" : SENTENCE_LENGTH, "st" : SENTENCE_THRESHOLD}

def getPoem(URL, START_INDEX = 154, TOTAL_LINES = 4, SENTENCE_LENGTH = 5, SENTENCE_THRESHOLD = 15):
        try:
            valid = validateInput(URL, START_INDEX, TOTAL_LINES, SENTENCE_LENGTH, SENTENCE_THRESHOLD)
            START_INDEX = valid["si"]
            TOTAL_LINES = valid["tl"]
            SENTENCE_LENGTH = valid["sl"]
            SENTENCE_THRESHOLD = valid["st"]
            return("\n\n" + buildPoem(getSentences(URL), START_INDEX, TOTAL_LINES, SENTENCE_LENGTH, SENTENCE_THRESHOLD))
        except TypeError as e:
            print(e)
            return("Input error (maybe try another URL, and check the settings).")


def getTwoLines(DONE, URL, START_INDEX=-1, TOTAL_LINES=2, SENTENCE_LENGTH=5, SENTENCE_THRESHOLD=15):
    try:
        valid = validateInput(URL, START_INDEX, TOTAL_LINES, SENTENCE_LENGTH, SENTENCE_THRESHOLD)
        START_INDEX = valid["si"]
        TOTAL_LINES = valid["tl"]
        SENTENCE_LENGTH = valid["sl"]
        SENTENCE_THRESHOLD = valid["st"]
        return (DONE + "<br><br>" + buildPoem(getSentences(URL), START_INDEX, TOTAL_LINES, SENTENCE_LENGTH, SENTENCE_THRESHOLD))
    except TypeError as e:
        print(e)
        return ("Input error (maybe try another URL, and check the settings).")