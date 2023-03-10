import gscholar
import re
import time


def get_title(title):
    bibtex = gscholar.query(title)
    regex = "journal\s*=\s*{(.*?)},"
    if(len(bibtex) == 0):
        return "\n"
    m = re.search(regex, bibtex[0])
    if m:
        print(m.group(1))
        return m.group(1) + "\n"
    else:
        return "\n"



if __name__ == '__main__':
    journals = []
    with open('文献126-170(任务序号1-908)-林250-330.csv', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            time.sleep(2)
            print(line)
            journals.append(get_title(line))

    print(journals)


    with open('title.txt', 'a', encoding='utf-8') as f:
        for journal in journals:
            f.write(str(journal))


