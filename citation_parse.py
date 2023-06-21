import re
import PyPDF2

def get_pdf(pdf_file, regex):
    text = ''
    with open(pdf_file, 'rb') as f:
        pdf_reader = PyPDF2.PdfFileReader(f)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extractText()
        print(text)
    return text


def get_cita_num(title, content):
    print(type(content))
    
    pass


def parse_pdf(pdf_path):
    results = {}
    text_list = []
    big_money = 0.0
    currency_symbols = ['¥', '￥']
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text_list.append(element.get_text())
        break
    print(text_list)
    




def get_citation(content):
    pass


if __name__ == '__main__':
    content = get_pdf("22.pdf", "\[\d+\]\s*(?=.*Gu)(?=.*Qiao).*?\.")
    title = "Self-learning optimal regulation for discrete-time nonlinear systems under event-driven formulation"
    get_cita_num(title, content)
