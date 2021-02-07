from src.AnagramFinder.AnagramFinder import AnagramFinder
from src.WordFinder.WordFinder import WordFinder
from PyDictionary import PyDictionary
import json

dictionaryFile = '../assets/twl06.txt'
wordsFile = '../assets/mostFreqWords_6_8.txt'
resultDictionary = '../assets/dictionary.json'
longWordFile = "../assets/google-10000-english-usa-no-swears-long.txt" # words of length 9+
mediumWordFile = "../assets/google-10000-english-usa-no-swears-medium.txt" # words of length 5 to 8
resultWordFile = '../assets/testWordList.txt'

lengthWords = {"3": "THREE", "4":"FOUR", "5":"FIVE", "6":"SIX", "7": "SEVEN", "8": "EIGHT", "9":"NINE", "10": "TEN"}

def _get_words(fileName):
    with open(fileName) as f:
        return f.read().split('\n')

def getRootWordList(lowerCharLimit, higherCharLimit):
    mediumWords = _get_words(mediumWordFile)
    longWords = _get_words(longWordFile)
    longWords = [x for x in longWords if len(x) <= higherCharLimit and len(x) >= lowerCharLimit]
    mediumWords = [x for x in mediumWords if len(x) <= higherCharLimit and len(x) >= lowerCharLimit]
    print(len(longWords) + len(mediumWords))
    with open(resultWordFile, 'w') as filehandle:
        for listitem in longWords:
            filehandle.write('%s\n' % listitem)
        for listitem in mediumWords:
            filehandle.write('%s\n' % listitem)

def formDictionary(wordList, word_finder, dict_builder):
    count = 0
    mWords = []
    print("Total number of words is %d" % len(wordList))
    for rWord in wordList:
        if not rWord:
            continue
        if count % 100 == 0:
            print("Processed %d number of words" % count)
        getData = word_finder.get_words(rWord)
        if rWord not in getData:
            getData.append(rWord)
        mWords_each = dict.fromkeys(["mChildWordBreakDownDictionary", "mChildWordCount", "mRootWord"])
        mChildWordBreakDownDictionary = {lengthWords[str(len(rWord))] : [] for rWord in getData if len(rWord) >= 3}
        for word in getData:
            if len(word) > 2:
                dict_word = {}
                dict_meaning = dict_builder.meaning(word, disable_errors=True)
                if dict_meaning is not None:
                    dict_word[word] = dict_meaning
                else:
                    dict_word[word] = {'None' : "Couldn't fetch meaning"}
                mChildWordBreakDownDictionary[lengthWords[str(len(word))]].append(dict_word)

        mWords_each["mChildWordBreakDownDictionary"] = mChildWordBreakDownDictionary
        mWords_each["mChildWordCount"] = len(getData)
        mWords_each["mRootWord"] = rWord
        mWords.append(mWords_each)
        count += 1
        print(count)
       # print(mChildWordBreakDownDictionary)
        if(count % 10 == 0):
            print(count)

    dictionary = dict.fromkeys(["mTotalNumberOfWords", "mWords"])
    dictionary["mTotalNumberOfWords"] = count
    dictionary["mWords"] = mWords
    return dictionary

if __name__ == "__main__":
    wordFinder = WordFinder(AnagramFinder(_get_words(dictionaryFile)))
    dict_builder = PyDictionary()
    wordList = _get_words(wordsFile)
    dictionary = formDictionary(wordList, wordFinder, dict_builder)
    with open(resultDictionary, "w") as outfile:
        json.dump(dictionary, outfile)

    #getRootWordList(6, 8) # uncomment this line if we want to generate root words list of desired length

