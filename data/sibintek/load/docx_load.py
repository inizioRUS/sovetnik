import docx
import os


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


for i in os.listdir("docx_doc"):
    print("____")
    print(i + "\n" + getText("docx_doc/" + i).replace("\n\n", ""))