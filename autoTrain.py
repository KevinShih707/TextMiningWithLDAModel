from DataProcessing.src.corpora import Corpora
from DataProcessing.src.lda import Lda
import Web.crawl.CrawlCuration.mlab as mlab
import sys, os
from pprint import pprint

def foo(classify):
    strlist = mlab.getAllNewsContent(classify)
    corpora = Corpora(strlist)
    print("creating corpora success\n")
    for seed in range(79, 80):
        lda = Lda(corpora, numTopics = 15, seed = 38)
        lda.saveModel(classify)
        print("#\n# " + str(seed) + "\n#\n")
        pprint(lda.showTopicsStr())
        print("代表性文章")
        print(lda.showAuthenticArticle())
        with open(classify + ".txt", 'at', encoding = 'utf-8') as file:
            file.write("#\n# seed = " + str(seed) + "\n#\n")
            file.write("\n".join([str(topic) for topic in lda.showTopicsStr()]))
            file.write("\n#代表性文章\n")
            file.write(str(lda.showAuthenticArticle()))
            file.write("\n\n\n")


if __name__ == "__main__":
    foo(sys.argv[1])
