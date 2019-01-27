
from keras_en_parser_and_analyzer.library.classifiers.lstm import WordVecBidirectionalLstmSoftmax
from keras_en_parser_and_analyzer.library.utility.parser_rules import *
from keras_en_parser_and_analyzer.library.utility.simple_data_loader import load_text_label_pairs
from keras_en_parser_and_analyzer.library.utility.text_fit import fit_text
from keras_en_parser_and_analyzer.library.utility.tokenizer_utils import word_tokenize
import os

# line_labels = {0: 'experience', 1: 'knowledge', 2: 'education', 3: 'project', 4: 'others'}
line_labels ={0: 'Name', 1: 'Personal', 2: 'Summary/Objective', 3: 'Education/Qualification/Workshop', 4: 'Work/Experience', 5: 'Project', 6: 'Knowledge/Skill', 7: 'Certification',
                    8: 'Publication', 9: 'Interest/Hobby', 10: 'SpokenLanguage', 11: 'Trait', 12: 'Label' ,13: 'Others'}
line_types = {0: 'header', 1: 'meta', 2: 'content'}


class ResumeParser(object):

    def __init__(self):
        self.line_label_classifier = WordVecBidirectionalLstmSoftmax()
        self.line_type_classifier = WordVecBidirectionalLstmSoftmax()
        self.email = None
        self.name = None
        self.sex = None
        self.ethnicity = None
        self.education = []
        self.objective = None
        self.mobile = None
        self.experience = []
        self.knowledge = []
        self.project = []
        self.name=None
        self.personal=[]
        self.certification=[]
        self.publication=[]
        self.interest=[]
        self.language=[]
        self.trait=[]
        self.label=[]
        self.others=[]
        self.meta = list()
        self.header = list()
        self.unknown = True
        self.raw = None
        #TODO add variables -> done

    def load_model(self, model_dir_path):
        self.line_label_classifier.load_model(model_dir_path=os.path.join(model_dir_path, 'line_label'))
        self.line_type_classifier.load_model(model_dir_path=os.path.join(model_dir_path, 'line_type'))

    def fit(self, training_data_dir_path, model_dir_path, batch_size=None, epochs=None,
            test_size=None,
            random_state=None):
        line_label_history = self.fit_line_label(training_data_dir_path, model_dir_path=model_dir_path,
                                                 batch_size=batch_size, epochs=epochs, test_size=test_size,
                                                 random_state=random_state)

        line_type_history = self.fit_line_type(training_data_dir_path, model_dir_path=model_dir_path,
                                               batch_size=batch_size, epochs=epochs, test_size=test_size,
                                               random_state=random_state)

        history = [line_label_history, line_type_history]
        return history

    def fit_line_label(self, training_data_dir_path, model_dir_path, batch_size=None, epochs=None,
                       test_size=None,
                       random_state=None):
        text_data_model = fit_text(training_data_dir_path, label_type='line_label')
        text_label_pairs = load_text_label_pairs(training_data_dir_path, label_type='line_label')

        if batch_size is None:
            batch_size = 64
        if epochs is None:
            epochs = 20
        history = self.line_label_classifier.fit(text_data_model=text_data_model,
                                                 model_dir_path=os.path.join(model_dir_path, 'line_label'),
                                                 text_label_pairs=text_label_pairs,
                                                 batch_size=batch_size, epochs=epochs,
                                                 test_size=test_size,
                                                 random_state=random_state)
        return history

    def fit_line_type(self, training_data_dir_path, model_dir_path, batch_size=None, epochs=None,
                      test_size=None,
                      random_state=None):
        text_data_model = fit_text(training_data_dir_path, label_type='line_type')
        text_label_pairs = load_text_label_pairs(training_data_dir_path, label_type='line_type')

        if batch_size is None:
            batch_size = 64
        if epochs is None:
            epochs = 20
        history = self.line_label_classifier.fit(text_data_model=text_data_model,
                                                 model_dir_path=os.path.join(model_dir_path, 'line_type'),
                                                 text_label_pairs=text_label_pairs,
                                                 batch_size=batch_size, epochs=epochs,
                                                 test_size=test_size,
                                                 random_state=random_state)
        return history

    #TOFIX: correct labels fo these methods to new labels 

    @staticmethod
    def extract_education(label, text):
        if label == 'Education/Qualification/Workshop':
            return text
        return None

    @staticmethod
    def extract_project(label, text):
        if label == 'Project':
            return text
        return None

    @staticmethod
    def extract_knowledge(label, text):
        if label == 'Knowledge/Skill':
            return text
        return None

    @staticmethod
    def extract_experience(label, text):
        if label == 'Work/Experience':
            return text
        return None

    @staticmethod
    def extract_summary(label, text):
        if label == 'Summary/Objective':
            return text
        return None

    #TODO: extract methods for all label types

    @staticmethod
    def extract_name(label, text):
        if label == 'Name':
            return text
        return None

    @staticmethod
    def extract_personal(label, text):
        if label == 'Personal':
            return text
        return None

    @staticmethod
    def extract_certification(label, text):
        if label == 'Certification':
            return text
        return None

    @staticmethod
    def extract_publication(label, text):
        if label == 'Publication':
            return text
        return None

    @staticmethod
    def extract_interest(label, text):
        if label == 'Interests/Hobby':
            return text
        return None

    @staticmethod
    def extract_language(label, text):
        if label == 'SpokenLanguage':
            return text
        return None

    @staticmethod
    def extract_trait(label, text):
        if label == 'Trait':
            return text
        return None
    
    @staticmethod
    def extract_label(label, text):
        if label == 'Label':
            return text
        return None
    
    @staticmethod
    def extract_others(label, text):
        if label == 'Others':
            return text
        return None

    def parse(self, texts, print_line=False):
        self.raw = [text.replace('\t',' ') for text in texts]
        
        for p in texts:
            # p=p.replace('\t',' ')
            p=p.replace('-'," ")
            # print('line -->',p)
            if len(p) > 1: #originally >10
                # print('line <->',p)
                s = word_tokenize(p.lower())

                line_label = self.line_label_classifier.predict_class(sentence=p)
                line_type = self.line_type_classifier.predict_class(sentence=p)
                print(p,'->',line_label,'->',line_type)
                print('-'*20)
                
                unknown = True

                name = extract_name(s, p)
                email = extract_email(s, p)
                sex = extract_sex(s, p)
                race = extract_ethnicity(s, p)

                education = self.extract_education(line_label, p)
                if education is None:
                    extract_education(s,p)
                objective = self.extract_summary(line_label, p)
                if objective is None:
                    objective=extract_summary(s,p)
                project = self.extract_project(line_label, p)
                if project is None:
                    project=extract_project(s,p)
                experience = self.extract_experience(line_label, p)
                if experience is None:
                    experience=extract_experience(s,p)
                # objective=self.extract_summary(line_label,p)
                # if objective is None:
                #     objective = extract_objective(s, p)
                knowledge = self.extract_knowledge(line_label, p)
                if knowledge is None:
                    extract_knowledge(s,p)
                #TODO add methods -> done
                name=self.extract_name(line_label,p)
                # if name is None:
                #     extract_name(s,p)
                personal=self.extract_personal(line_label,p)

                certification=self.extract_certification(line_label,p)

                publication=self.extract_publication(line_label,p)

                interest=self.extract_interest(line_label,p)

                language=self.extract_language(line_label,p)

                trait=self.extract_trait(line_label,p)

                label = self.extract_label(line_label,p)

                others=self.extract_others(line_label,p)

                mobile = extract_mobile(s, p)


                if name is not None:
                    self.name = name
                    unknown = False
                if email is not None:
                    self.email = email
                    unknown = False
                if sex is not None:
                    self.sex = sex
                    unknown = False
                if race is not None:
                    self.ethnicity = race
                    unknown = False
                if education is not None:
                    self.education.append(education)
                    unknown = False
                if knowledge is not None:
                    self.knowledge.append(knowledge)
                    unknown = False
                if project is not None:
                    self.project.append(project)
                    unknown = False
                if objective is not None:
                    self.objective = objective
                    unknown = False
                if experience is not None:
                    self.experience.append(experience)
                    unknown = False
                
                if name is not None:
                    self.name = name
                    unknown = False

                if personal is not None:
                    self.personal.append(personal)
                    unknown = False
                if certification is not None:
                    self.certification.append(certification)
                    unknown = False
                if publication is not None:
                    self.publication.append(publication)
                    unknown = False
                if interest is not None:
                    self.interest.append(interest)
                    unknown = False
                if language is not None:
                    self.language.append(language)
                    unknown = False
                if trait is not None:
                    self.trait.append(trait)
                    unknown = False

                if label is not None:
                    self.label.append(label)
                    unknown = False

                if others is not None:
                    self.others.append(others)

                if mobile is not None:
                    self.mobile = mobile
                    unknown = False

                if line_type == 'meta':
                    self.meta.append(p)
                    unknown = False

                # if line_type == 'header':
                #     p='('+line_label+') '+p
                #     self.header.append(p)

                if unknown is False:
                    self.unknown = unknown

                if print_line:
                    print('parsed: ', p)

    def summary(self):
        # TODO add new label info -> done
        text = ''
        # if self.name is not None:
        #     text += 'name: {}\n'.format(self.name)
        
        if self.name is not None:
            text += 'Name: {}\n'.format(self.name)

        if self.mobile is not None:
            text += 'mobile: {}\n'.format(self.mobile)
        if self.email is not None:
            text += 'email: {}\n'.format(self.email)

        for p in self.personal:
            text += 'Personal: {}\n'.format(p)

        if self.ethnicity is not None:
            text += 'ethnicity: {}\n'.format(self.ethnicity)
        if self.sex is not None:
            text += 'sex: {}\n'.format(self.sex)
        if self.objective is not None:
            text += 'objective: {}\n'.format(self.objective)

        for ex in self.experience:
            text += 'experience: {}\n'.format(ex)

        for edu in self.education:
            text += 'education: {}\n'.format(edu)

        for know in self.knowledge:
            text += 'knowledge: {}\n'.format(know)
        for pro in self.project:
            text += 'project: {}\n'.format(pro)
        
        for c in self.certification:
            text += 'Certifications: {}\n'.format(c)
        for pub in self.publication:
            text += 'Publication: {}\n'.format(c)
        for i in self.interest:
            text += 'Interest: {}\n'.format(i)
        for l in self.language:
            text += 'Spoken Languages: {}\n'.format(l)
        for t in self.trait:
            text += 'Certifications: {}\n'.format(t)
        for l in self.label:
            text += 'Labels: {}\n'.format(l)
        for o in self.others:
            text += 'Others: {}\n'.format(o)
        
        for header_data in self.header:
            text += 'header: {}\n'.format(header_data)

        for meta_data in self.meta:
            text += 'meta: {}\n'.format(meta_data)

        return text.strip()
