"""
直接用Python Console在 DataProcessing\ 底下測試用
用來測其他測資
"""

from src.corpora import Corpora
from src.lda import Lda

CSV_FILE_PATH = "test_data/cnanewstaiwan.csv"
STOPWORDS_FILE_PATH = "src/stopwords.txt"

corpora = Corpora(filePath=CSV_FILE_PATH, isDeleteUrl=False, stopwords=STOPWORDS_FILE_PATH)
lda = Lda(corpora, numTopics=2, seed=10)
print("lda.showTopicsStr()\n", lda.showTopicsStr(), "\n")
print("lda.showTopicsList()[0][1]\n", lda.showTopicsList(), "\n")
print("lda.classifyTopic()\n", lda.classifyTopic(), "\n")
print("lda.findArticleMatched()\n", lda.findArticleMatched(), "\n")
