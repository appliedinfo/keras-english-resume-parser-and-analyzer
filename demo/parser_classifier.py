
import dl_based_parser_train
import dl_based_parser_predict

from read import read_pdf_from_path
from annotate_results import annotate_predictions
import os

class ResumeParseClassifier:
    def __init__(self,classifier='CNN',model_dir='/models'):
        if classifier == 'CNN_LSTM':
            self.classifier_type='CNN_LSTM'
        else:
            self.classifier_type='CNN'
        self.model_dir=model_dir

    def read_sections(self,resume=''):
        if not resume=='' and os.path.exists(resume) and os.path.isfile(resume): 
            self.resume=resume
        else:
            print('Pass correct resume information')
            return
        
        self.file_content,self.bb = read_pdf_from_path(resume)
        return [self.file_content,self.bb]

    def fit(self,train_dir, batch_size = 64, epochs = 20, test_size=0.2):
        # dl_based_parser_train.main(train_dir)
        dl_based_parser_train.train_model(training_data=train_dir, model_dir=self.model_dir, batch_size = batch_size, epochs = epochs, test_size=test_size,classifier_type=self.classifier_type)


    def predict(self,res_samples_dir):
        dl_based_parser_predict.main(res_samples_dir)

    def predict_content(self,file_content):
        preds=dl_based_parser_predict.parse_resume_content(file_content,classifier_type=self.classifier_type, model_dir=self.model_dir)
        return preds
    
    def mark_resume(self,bboxes,resume,labels):
        annotate_predictions({resume:bboxes},{resume:labels})

if __name__ == '__main__':

    resume='data/resume_samples/26 Tanya_s CV.pdf'

    class_type='CNN' # CNN or CNN_LSTM
    # class_type='CNN_LSTM'
    
    model='/models'
    classifier = ResumeParseClassifier(class_type,model_dir=model)

    # classifier.fit('/data/training_data_mser',model_dir='/models', batch_size=62,epochs=25,test_size=0.2)

    file_content , bboxes = classifier.read_sections(resume)

    # print(file_content)
    # print('-'*75)
    # print(bboxes)
    # print('---'*20)

    labels=classifier.predict_content(file_content)

    # for x,y in zip (file_content,labels):
    #     print(x," : ",y)
    # print('---'*20)

    classifier.mark_resume(bboxes,resume,labels)
    print('okay')
