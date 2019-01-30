import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from keras_en_parser_and_analyzer.library.dl_based_parser import ResumeParser
from keras_en_parser_and_analyzer.library.utility.io_utils import read_pdf_and_docx

from keras_en_parser_and_analyzer.library.classifiers.cnn import WordVecCnn

from read import read_pdfs

from annotate_results import annotate_predictions

def main(resume_samples):
    


    current_dir = os.path.dirname(__file__)
    current_dir = current_dir if current_dir is not '' else '.'
    data_dir_path = current_dir + resume_samples # directory to scan for any pdf and docx files

    predictions=dict()
    collected_bboxes=dict()

    def parse_resume(file_path, file_content):
        print('parsing file: ', file_path)

        parser = ResumeParser()

        # for WordVecCnn
        parser.line_label_classifier = WordVecCnn()
        parser.line_type_classifier = WordVecCnn()


        parser.load_model(current_dir + '/models')
        preds=parser.go_predict(file_content)
        # parser.parse(file_content) # line_type and line_labels are predicted within this method
        # print(parser.raw)  # print out the raw contents extracted from pdf or docx files

        # if parser.unknown is False:
        #     print(parser.summary())

        predictions[file_path]=preds

        print('++++++++++++++++++++++++++++++++++++++++++')


    # collected = read_pdf_and_docx(data_dir_path, command_logging=True, callback=lambda index, file_path, file_content: {
    #     parse_resume(file_path, file_content)
    # })

    # method 2 (mser)
    collected,collected_bboxes = read_pdfs(data_dir_path, command_logging=True, callback=lambda index, file_path, file_content: {
        parse_resume(file_path, file_content)
    })

    print('count: ', len(collected))
    # for k,v in collected_bboxes.items():
    #     print(k,type(v))
    #     for x,y in v.items():
    #         print(x,y)

    # print(collected_bboxes)
    # print('-'*20)
    # for x,y in predictions.items():
    #     print(x,len(y),'\n')
    # for x,y in collected_bboxes.items():
    #     for k,v in y.items():
    #         print(x,k,len(v),'\n')
    # print(collected_bboxes)
    # print('---'*20)
    # print(predictions)
    annotate_predictions(collected_bboxes,predictions)


def parse_resume_content(file_content,classifier_type='CNN',model_dir='/models'):
    current_dir = os.path.dirname(__file__)
    parser = ResumeParser()

    if classifier_type=='CNN':
        from keras_en_parser_and_analyzer.library.classifiers.cnn import WordVecCnn
        parser.line_label_classifier = WordVecCnn()
        parser.line_type_classifier = WordVecCnn()
    else:
        from keras_en_parser_and_analyzer.library.classifiers.cnn_lstm import WordVecCnnLstm
        parser.line_label_classifier = WordVecCnnLstm()
        parser.line_type_classifier = WordVecCnnLstm()

    parser.load_model(current_dir + model_dir)
    preds=parser.go_predict(file_content)
    # parser.parse(file_content) # line_type and line_labels are predicted within this method
    # print(parser.raw)  # print out the raw contents extracted from pdf or docx files

    # if parser.unknown is False:
    #     print(parser.summary())

    

    # print('++++++++++++++++++++++++++++++++++++++++++')

    # print('results: ')
    # print(type(preds))
    # print(preds)

    return preds




if __name__ == '__main__':
    main('/data/resume_samples')