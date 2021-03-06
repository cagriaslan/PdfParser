import textract
import string
import nltk
from nltk import bigrams
from nltk import trigrams
import re
import os
import sys
import getopt
import operator


class PdfParser:
    def __init__(self, keywords_file, folder_name):
        self.keywords_file = keywords_file
        self.keywords = self.keyword_handler()
        self.folder_name = folder_name
        self.total_count_dict = {str(key): 0 for key in self.keywords}
        self.unables = []

    def keyword_handler(self):
        keywords = []
        with open(self.keywords_file, "r", encoding="UTF-8") as fp:
            for line in fp:
                keywords.append(line.lower().split())
        return keywords

    def mainer(self):
        with open("output", "w", encoding="UTF-8") as fp:
            for each in os.listdir(self.folder_name):
                """ for each file in the folder """
                count_dict = {str(key): 0 for key in self.keywords}
                text_of_the_pdf = ""
                try:
                    text_of_the_pdf = textract.process(os.path.join(self.folder_name, each))
                    text_of_the_pdf = text_of_the_pdf.decode("utf-8", errors="ignore")
                except:
                    self.unables.append(each)
                    continue
                punc_cleaned = re.sub('[%s]' % re.escape(string.punctuation), '', text_of_the_pdf)
                tokenized = nltk.word_tokenize(punc_cleaned.lower().replace("\n", ""))
                text_bigrams = bigrams(tokenized)
                bigram = [each for each in text_bigrams]
                text_trigrams = trigrams(tokenized)
                trigram = [each for each in text_trigrams]
                for key in self.keywords:
                    if len(key) == 1:
                        for tokens in tokenized:
                            if key[0] in tokens:
                                self.total_count_dict[str(key)] += 1
                                count_dict[str(key)] += 1
                    elif len(key) == 2:
                        for tokens in bigram:
                            if key[0] in tokens and key[1] in tokens:
                                self.total_count_dict[str(key)] += 1
                                count_dict[str(key)] += 1
                    elif len(key) == 3:
                        for tokens in trigram:
                            if key[0] in tokens and key[1] in tokens and key[2] in tokens:
                                self.total_count_dict[str(key)] += 1
                                count_dict[str(key)] += 1
                fp.write("----- File name: " + each + " -----\n")
                sorted_x = sorted(count_dict.items(), key=operator.itemgetter(1))
                fp.write(str(sorted_x) + "\n")
            sorted_y = sorted(self.total_count_dict.items(), key=operator.itemgetter(1))
            fp.write("*** Total Count Values ***\n" + str(sorted_y))
            fp.write("\n" + str(len(self.unables)))


def main(argv):
    keywords = ''
    folder = ''
    try:
        opts, args = getopt.getopt(argv, "hk:f:", ["kfile=", "ffile="])
    except getopt.GetoptError:
        print('test.py -k <keyword_file> -f <folder_name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -k <keyword_file> -f <folder_name>')
            sys.exit()
        elif opt in ("-k", "--kfile"):
            keywords = arg
        elif opt in ("-f", "--ffile"):
            folder = arg
    print('Keyword file is: ', keywords)
    print('Article folder is: ', folder)
    pars = PdfParser(keywords, folder)
    pars.mainer()


if __name__ == "__main__":
    main(sys.argv[1:])