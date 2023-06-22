import sys, fitz
import re
import os


def get_pdf_content(file_path):
    doc = fitz.open(file_path)
    pages = []
    content = ""

    for page in doc:
        content = page.get_text().encode("utf8")
        pages.append(content)
    return pages

def parse_pdf_ref(file_path):
    doc = fitz.open(file_path)
    pagenum = len(doc)
    ref_list=[]
    for num, p in enumerate(doc):
        content = p.get_text('blocks')
        #matches = re.findall(regex, content)
        for pc in content:
            # line num
            # print(pc)
            txtblocks = list(pc[4:-2])
            txt=''.join(txtblocks)
            #print(pc, txt)
            if 'References' in txt or 'REFERENCES' in txt or 'referenCes' in txt:
                refpagenum = [i for i in range(num, pagenum)]
                for rpn in refpagenum:
                    refpage = doc[rpn]
                    refcontent=refpage.get_text('blocks')
                    for n, refc in enumerate(refcontent):
                        txtblocks=list(refc[4:-2])
                        ref_list.extend(txtblocks)
    print(''.join(ref_list))
    return ref_list

def parse_pdf_content(pages, regex):
    for p in pages:
        #print(p)
        #print(type(p))
        txt = ''.join(p.decode('utf-8'))
        matches = re.findall(regex, txt)
        if matches:
            print(matches)
            #return matches
            return True
    return False

def get_dir_pdf(dir_path):
    pdf_list = []
    if not os.path.exists(dir_path):
        return False
    else:
        pdf_list = os.listdir(dir_path)
        return pdf_list


if __name__ == '__main__':
    # get all pdf file in dir
    #pages = get_pdf_content('22.pdf')
    parse_pdf_ref('22.pdf')



