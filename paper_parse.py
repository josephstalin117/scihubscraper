import sys, fitz
import re
import os

print("test")
fname = "test.pdf"
doc = fitz.open(fname)  # open document
out = open(fname + ".txt", "wb")  # open text output
for page in doc:  # iterate the document pages
    text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
    out.write(text)  # write text of page
    out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
out.close()


def get_pdf_content(file_path):
    doc = fitz.open(file_path)
    pages = []
    content = ""

    for page in doc:
        content = page.get_text().encode("utf8")
        pages.append(content)
    return pages

def parse_pdf_ref(pages):
    pagenum = len(pages)
    ref_list=[]
    for num, p in enumerate(pages):
        #matches = re.findall(regex, content)
        for pc in p:
            # line num
            #print(pc)
            txtblocks = list(pc[4:-2])
            txt=''.join(txtblocks)
            print(pc, txt)
            if 'References' in txt or 'REFERENCES' in txt or 'referenCes' in txt:
                refpagenum = [i for i in range(num, pagenum)]
                for rpn in refpagenum:
                    refpage = p[rpn]
                    refcontent=refpage.getText('blocks')
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
    pdf_list = get_dir_pdf("176")
    #print(pdf_list)

    fellow_list = []
    # filter pdf file
    for pdf in pdf_list:
        print(pdf)
        pages = get_pdf_content("176/" + pdf)
        #is_fellow = parse_pdf_content(pages)
        is_fellow = parse_pdf_content(pages, "Fellow")
        if is_fellow:
            fellow_list.append(pdf)
        #parse_pdf_content(pages, "Fellow")

    # save fellow list
    with open('fellow.txt', 'a', encoding='utf-8') as f:
        for fellow in fellow_list:
            f.write(str(fellow))
            f.write('\n')



