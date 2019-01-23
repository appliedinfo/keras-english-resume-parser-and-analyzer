import pdf_img
import segments
import text_mser
import os

pdfimg=pdf_img.PdfConverter()
seg=text_mser.SegmentText()
# seg=segments.SegmentText()

def docx_pdf(dir_path):
    
    import docx_to_pdf
    for f in os.listdir(dir_path):
        
        file_path = os.path.join(dir_path, f)
        # print(file_path,f)
        if os.path.isfile(file_path) and (f.lower().endswith('.docx') or f.lower().endswith('.doc')):
            # print(file_path)
            docx_to_pdf.doc2pdf(file_path)
            # print(file_path)
            filename=file_path.split('/')[-1].split('.')[0]
            filename=filename+'.pdf'
            os.rename(filename, 'data/resume_samples/'+filename)
            

def read_pdfs(dir_path, collected=None, command_logging=False, callback=None):
    docx_pdf(dir_path)
    if collected is None:
        collected = dict()
    for f in os.listdir(dir_path):
        file_path = os.path.join(dir_path, f)
        if os.path.isfile(file_path):
            contents=[]
            # txt = []
            # if f.lower().endswith('.docx'):
            #     if command_logging:
            #         print('extracting text from docx: ', file_path)
                
                # txt = docx_to_text(file_path)
                # TODO: call to docs to pdf then pdf to images





            # elif f.lower().endswith('.pdf'):
            if f.lower().endswith('.pdf'):
                if command_logging:
                    print('extracting text from pdf: ', file_path)
                # txt = pdf_to_text(file_path)
                # print(os.getcwd())
                for x in os.listdir('data/resume_images'):
                    os.remove('data/resume_images/'+x)
                print(file_path)
                pdfimg.convert(file_path)
                file_list = os.listdir('data/resume_images/')
                file_list.sort()
                # print(type(file_list))
                for x in file_list:

                    txt=seg.find_segments('data/resume_images/'+x)
                    contents.extend(txt)
                # print(contents)


                
            if contents is not None and len(contents) > 0:
                if callback is not None:
                    callback(len(collected), file_path, contents)
                collected[file_path] = contents
        elif os.path.isdir(file_path):
            read_pdfs(file_path, collected, command_logging, callback)

    return collected






# def read_pdf_and_docx(dir_path, collected=None, command_logging=False, callback=None):
#     if collected is None:
#         collected = dict()
#     for f in os.listdir(dir_path):
#         file_path = os.path.join(dir_path, f)
#         if os.path.isfile(file_path):
#             txt = None
#             if f.lower().endswith('.docx'):
#                 if command_logging:
#                     print('extracting text from docx: ', file_path)
#                 txt = docx_to_text(file_path)
#             elif f.lower().endswith('.pdf'):
#                 if command_logging:
#                     print('extracting text from pdf: ', file_path)
#                 txt = pdf_to_text(file_path)
#             if txt is not None and len(txt) > 0:
#                 if callback is not None:
#                     callback(len(collected), file_path, txt)
#                 collected[file_path] = txt
#         elif os.path.isdir(file_path):
#             read_pdf_and_docx(file_path, collected, command_logging, callback)

#     return collected




# def read_pdf(dir_path, collected=None):
#     if collected is None:
#         collected = dict()
#     for f in os.listdir(dir_path):
#         file_path = os.path.join(dir_path, f)
#         if os.path.isfile(file_path):
#             txt = None
#             if f.lower().endswith('.pdf'):
#                 txt = pdf_to_text(file_path)
#             if txt is not None and len(txt) > 0:
#                 collected[file_path] = txt
#         elif os.path.isdir(file_path):
#             read_pdf(file_path, collected)

#     return collected

if __name__ == '__main__':
    read_pdfs('data/resume_samples/', collected=None, command_logging=False, callback=None)
    # docx_pdf('data/resume_samples/')