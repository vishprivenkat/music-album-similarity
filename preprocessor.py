from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd 
import re 
import sys

lemmatizer = WordNetLemmatizer()

class Preprocessor: 

    def __init__(self) -> None:
        pass

    def convert_to_lower(self, string):
        '''
        Function to convert string to lower case 
        '''
        return string.lower()

    def get_lemmatized_form(self, word): 
        '''
        Function to lemmatize word to root form 
        '''
        return lemmatizer.lemmatize(word)

    def remove_symbols(self, string):
        '''
        Remove symbols except the . from the descriptions 
        '''
        resultant_string = re.sub(r'[^\w\s.]', ' ', string)
        return resultant_string

    def sentence_analysis(self, description): 
        '''
        * Takes in one description with several sentences and splits the sentences. 
        * Tokenizes every sentence and removes the stop words.
        * Lemmatizes each token to bring it to its root form. 
        * Retains only those sentences that have less than 20 tokens. 
        '''
        preprocessed_description = []
        sentences = sent_tokenize(description)

        for sentence in sentences:
            preprocessed_sentence = ''
            word_tokens = word_tokenize(sentence) 
        
            tokens_without_stop_words =  [word for word in word_tokens if not word in stopwords.words()]
            
            '''
            Edge Case Alert: 
            * Check if the tokens is less than 20. If yes, then it's taken into account.
            * If no, it's dropped from consideration. 
            * But, if there are a list of tokens whose size is more than 20, and the record, 
            in the dataframe has no preprocessed description, to prevent the field from being empty, 
            that token alone is taken into consideration. 
            
            '''
            if len(tokens_without_stop_words)<20:
                preprocessed_sentence+= ' '.join(tokens_without_stop_words)
            elif len(tokens_without_stop_words) >=20 and tokens_without_stop_words[-1]=='.' and len(preprocessed_description)==0:
                preprocessed_sentence+= ' '.join(tokens_without_stop_words)
                

            if len(preprocessed_sentence)>0:
                preprocessed_description.append(preprocessed_sentence)

        
        preprocessed_description = ''.join(preprocessed_description)
        
        return preprocessed_description

    def preprocess_data(self, description):
        '''
        Function to read the dataframe and preprocess data
        '''
        #Removing symbols except the '.'
        description = [ self.remove_symbols(each) for each in description] 

        #Converting all words to lowercase 
        description = [self.convert_to_lower(each) for each in description] 

        preprocessed_description = [self.sentence_analysis(sentence) for sentence in description] 

        return preprocessed_description

    

    def open_csv(self, csv_file_name):
        '''
        Function to read the csv
        '''
        dataframe = pd.read_csv(csv_file_name)
        return dataframe


if __name__ == "__main__":
    file_to_open = sys.argv[1]
    file_to_write_into = sys.argv[2]
    preprocessor = Preprocessor()
    dataframe = preprocessor.open_csv(file_to_open) 
    print('Preprocessing the Descriptions.......')
    dataframe['description'] = preprocessor.preprocess_data(dataframe['description'])
    dataframe.to_csv(file_to_write_into, index=False, header=True)
