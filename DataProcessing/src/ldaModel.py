from gensim.models.ldamodel import Ldamodel

def ldaTraining(corpus=corpus_tfidf,id2word=dictionary,num_topics=2):
    lda = LdaModel(corpus=corpus_tfidf,id2word=dictionary,num_topics=2)
    return lda.show_topics(num_topics)
