import PyPDF2
import re

def get_pdf(pdf_file):
    with open(pdf_file, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
            if page_num == 0:
                page_1st = page.extract_text()




def get_citation(content):
    pass


if __name__ == '__main__':
    content = get_pdf()