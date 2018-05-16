import jieba
import csv

def cutTextFile(path = ""):
    with open (path, "rt", encoding = 'utf-8') as file:
        content = file.read()
        words = jieba.lcut(content)
    return " ".join(words)

# def cutCsvFile(path = ""):
#     data = openCsvFileAsDict(path)

def openCsvFileAsDict(path = ""):
    with open (path, "rt", encoding = 'utf-8') as file:
        reader = csv.DictReader(file, fieldnames = ['time', 'id', 'text', 'share', 'likecount', 'sharecount'])
        content = [row for row in reader]#字典串列生成式

    if (content[0]['likecount'] == '讚數'): #移除資料說明欄
        del content[0]

    return content


if __name__ == "__main__":
    cutTextFile("DataProcessing/test_data/testData.txt")
    # cutCsvFile("DataProcessing/test_data/testData.csv")
