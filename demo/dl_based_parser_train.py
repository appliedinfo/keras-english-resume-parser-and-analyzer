import numpy as np
import sys
import os


def main(training_data=''):
    if training_data == '':
        print('training data dir missing')
    else:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

        from keras_en_parser_and_analyzer.library.dl_based_parser import ResumeParser

        # from keras_en_parser_and_analyzer.library.classifiers.cnn_lstm import WordVecCnnLstm
        from keras_en_parser_and_analyzer.library.classifiers.cnn import WordVecCnn



        classifier = ResumeParser()
        # for cnnlstm
        # classifier.line_label_classifier = WordVecCnnLstm()
        # classifier.line_type_classifier = WordVecCnnLstm()

        # for cnn
        classifier.line_label_classifier = WordVecCnn()
        classifier.line_type_classifier = WordVecCnn()

        random_state = 42
        np.random.seed(random_state)

        current_dir = os.path.dirname(__file__)
        current_dir = current_dir if current_dir is not '' else '.'
        output_dir_path = current_dir + '/models'
        # training_data_dir_path = current_dir + '/data/training_data'

        # for method 2 (mser)
        training_data_dir_path = current_dir + training_data


        # classifier = ResumeParser()
        batch_size = 64
        epochs = 20
        history = classifier.fit(training_data_dir_path=training_data_dir_path,
                                model_dir_path=output_dir_path,
                                batch_size=batch_size, epochs=epochs,
                                test_size=0.2,
                                random_state=random_state)
        
def train_model(training_data='',model_dir='/models',batch_size = 64,epochs = 20,test_size=0.2, classifier_type='CNN'):
    if training_data == '':
        print('training data dir missing')
    else:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

        from keras_en_parser_and_analyzer.library.dl_based_parser import ResumeParser

        classifier = ResumeParser()
        # for cnnlstm
        # classifier.line_label_classifier = WordVecCnnLstm()
        # classifier.line_type_classifier = WordVecCnnLstm()

        # for cnn
        if classifier_type=='CNN':
            from keras_en_parser_and_analyzer.library.classifiers.cnn import WordVecCnn
            classifier.line_label_classifier = WordVecCnn()
            classifier.line_type_classifier = WordVecCnn()
        else:
            from keras_en_parser_and_analyzer.library.classifiers.cnn_lstm import WordVecCnnLstm
            classifier.line_label_classifier = WordVecCnnLstm()
            classifier.line_type_classifier = WordVecCnnLstm()

        random_state = 42
        np.random.seed(random_state)

        current_dir = os.path.dirname(__file__)
        current_dir = current_dir if current_dir is not '' else '.'
        output_dir_path = current_dir + model_dir
        # training_data_dir_path = current_dir + '/data/training_data'

        # for method 2 (mser)
        training_data_dir_path = current_dir + training_data


        # classifier = ResumeParser()
        # batch_size = 64
        # epochs = 20
        test_size=0.2
        history = classifier.fit(training_data_dir_path=training_data_dir_path,
                                model_dir_path=output_dir_path,
                                batch_size=batch_size, epochs=epochs,
                                test_size=test_size,
                                random_state=random_state)


if __name__ == '__main__':
    main(training_data='/data/training_data_mser')
