import PyPDF2
import re
# from googletrans import Translator
# import requests

# from translation import baidu, google, youdao, iciba
import csv

def get_citation(pdf_name, regex):
    string_list = []
    for pdf_num in range(32,60):

        pdf_file = open(pdf_name, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
            if page_num == 0:
                page_1st = page.extract_text()

        pdf_file.close()

        regex = "\[\d+\]\s*(?=.*Gu)(?=.*Qiao).*?\."

        matches = re.findall(regex, text)
        if not matches:
            string_list.append(str(pdf_num)+',Not Fund,Not Fund')
            continue
        matches_str = matches[0]

        match_cite = re.findall("\d+", matches[0])[0]
        sentence_cited = re.findall("[A-Z][et al.]?[^.?!]*\["+match_cite+"\][^.?!]*\.",text)
        if len(sentence_cited)<1 or len(sentence_cited)>1:
            senten = 'Not Fund'
        else:
            senten = sentence_cited[0].replace('-\n','').replace('\n','')

        fellow_list = re.findall(",?\s?[A-Z][\s\S]*Fellow, IEEE",page_1st)
        if not fellow_list:
            fellow_list = 'Not Fund'

        pdf_str = str(pdf_num)+','+str(senten)+','+str(fellow_list)
        string_list.append(pdf_str)
        print(f'{pdf_num} done')


    with open('output.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for string in string_list:
            writer.writerow(string.split(','))



# llcitations = list(set(matches))





# session = requests.session()
# session.proxies ={
#     "http": "http://127.0.0.1:7890",
#     "https": "http://127.0.0.1:7890"
# }



# proxies = {
#         "http": "http://127.0.0.1:7890",
#         "https": "http://127.0.0.1:7890",
# }


# # from httpcore import SyncHTTPProxy


# # http_proxy = SyncHTTPProxy((b'http',b'http://127.0.0.1',7890))


# # translator = Translator(service_urls=['translate.google.com'],
# #                         proxies={"https": SyncHTTPProxy((b'http', b'http://127.0.0.1', 7890, b''))},
# #                         )





# translator = Translator(service_urls=['translate.google.com'])

# translator.translate(senten, dest='zh-CN')




# translated_citations = []




# for citation in citations:
#     translation = translator.translate(citation, dest='zh-CN')
#     translated_citation = translation.text
#     translated_citations.append(translated_citation)

# print(translated_citations)









if __name__ == '__main__':
    get_citation('Qiao Gu.pdf', regex)