from pdf2image import convert_from_path

class PdfConverter(object):
    def __init__(self):
        pass

    def convert(self,path,f):
        # import os

        # pages = convert_from_path(os.path.join(path,pdf), 250)
        pages = convert_from_path(path, 300)
        i=0
        for page in pages:
            page.save('data/resume_images/'+f+'/'+ str(i) + '.jpg', 'JPEG')
            # print(type(page))
            i += 1


if __name__ == '__main__':
    convert('9.pdf')
