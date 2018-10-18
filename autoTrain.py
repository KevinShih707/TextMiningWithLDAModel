from DataProcessing.src.corpora import Corpora
from DataProcessing.src.lda import Lda
import Web.crawl.CrawlCuration.mlab as mlab
import sys, os
from pprint import pprint

def foo(classify):
    strlist = mlab.getAllNewsContent(classify)
    corpora = Corpora(strlist)
    print("creating corpora success\n")
    for seed in range(21, 31):
        lda = Lda(corpora, seed = seed)
        print("#\n# " + str(seed) + "\n#\n")
        pprint(lda.showTopicsStr())
        
        with open(classify + ".txt", 'at', encoding = 'utf-8') as file:
            file.write("#\n# seed = " + str(seed) + "\n#\n")
            file.write("\n".join([str(topic) for topic in lda.showTopicsStr()]))
            file.write("\n\n\n")


if __name__ == "__main__":
    foo(sys.argv[1])
