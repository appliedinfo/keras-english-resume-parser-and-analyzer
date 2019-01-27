import sys
import os


def main():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    from keras_en_parser_and_analyzer.library.dl_based_parser import ResumeParser
    from keras_en_parser_and_analyzer.library.utility.io_utils import read_pdf_and_docx

    from keras_en_parser_and_analyzer.library.classifiers.cnn import WordVecCnn


    from read import read_pdfs


    current_dir = os.path.dirname(__file__)
    current_dir = current_dir if current_dir is not '' else '.'
    data_dir_path = current_dir + '/data/resume_samples' # directory to scan for any pdf and docx files

    def parse_resume(file_path, file_content):
        print('parsing file: ', file_path)

        parser = ResumeParser()

        # for WordVecCnn
        parser.line_label_classifier = WordVecCnn()
        parser.line_type_classifier = WordVecCnn()
        

        parser.load_model(current_dir + '/models')
        parser.parse(file_content) # line_type and line_labels are predicted within this method
        # print(parser.raw)  # print out the raw contents extracted from pdf or docx files

        # if parser.unknown is False:
        #     print(parser.summary())

        print('++++++++++++++++++++++++++++++++++++++++++')

    # collected = read_pdf_and_docx(data_dir_path, command_logging=True, callback=lambda index, file_path, file_content: {
    #     parse_resume(file_path, file_content)
    # })

    # method 2 (mser)
    collected = read_pdfs(data_dir_path, command_logging=True, callback=lambda index, file_path, file_content: {
        parse_resume(file_path, file_content)
    })

    print('count: ', len(collected))


if __name__ == '__main__':
    main()