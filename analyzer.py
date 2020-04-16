import pandas as pd
import numpy as np
import string
import re
import collections
import nltk
from nltk.corpus import stopwords

#Text cleaner

#Contractions Map
contraction_map = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"how're": "how are",
"you've": "you have"
}

def expand_contractions(text, contraction_mapping=contraction_map):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

def text_cleaner(input_text):
    #input_text=input_text.lower()
    input_text = re.sub('^rt', '', input_text)
    input_text = re.sub('\[.*?\]', '', input_text)
    input_text = re.sub(r"http\S+",'',input_text)
    input_text = re.sub('<.*?>+', '', input_text)
    input_text = re.sub('@\w+', '', input_text)
    input_text = re.sub('[%s]' % re.escape(string.punctuation), '', input_text)
    input_text = re.sub('\n', '', input_text)
    input_text = re.sub('\w*\d\w*', '', input_text)
    return input_text

def stemmer_output(input_string):    
    stemmer = nltk.stem.PorterStemmer()
    for token in input_string:
        output_string=stemmer.stem(input_string)
        return output_string

def cleaned_data_set(data_set_temp):

    data_set_heading = data_set_temp.copy()

    #Text cleaning begin
    #Lower the text
    data_set_temp['Review_lower'] = data_set_temp['Review'].apply(lambda x:x.lower())

    #Expand contractions
    data_set_temp['No_Contractions'] = data_set_temp['Review_lower'].apply(lambda x:expand_contractions(x))

    #Remove punctuations, URLs, etc
    data_set_temp['Cleaned_text'] = data_set_temp['No_Contractions'].apply(lambda x:text_cleaner(x))

    nltk.download('stopwords')
    stop_words= stopwords.words('english')
    stop_words.remove('no')
    stop_words.remove('not')

    #Remove all stop words
    data_set_temp['No_stop_words'] = data_set_temp['Cleaned_text'].str.split() \
        .apply(lambda x: [word for word in x if word not in stop_words]) \
        .apply(lambda x: ' '.join(x))

    #Stem the input
    data_set_temp['Stemmed_review'] = data_set_temp['No_stop_words'].apply(lambda x:stemmer_output(x))

    data_set_heading['Heading_lower'] = data_set_heading['Heading'].apply(lambda x:x.lower())
    data_set_heading['No_Contractions'] = data_set_heading['Heading_lower'].apply(lambda x:expand_contractions(x))
    data_set_heading['Cleaned_text'] = data_set_heading['No_Contractions'].apply(lambda x:text_cleaner(x))

    data_set_heading['No_stop_words'] = data_set_heading['Cleaned_text'].str.split() \
    .apply(lambda x: [word for word in x if word not in stop_words]) \
    .apply(lambda x: ' '.join(x))

    data_set_final = pd.DataFrame()
    data_set_final['Heading'] = data_set_heading['No_stop_words'].copy()
    data_set_final['Review'] = data_set_temp['No_stop_words'].copy()
    data_set_final['Star_count'] = data_set_temp['Star_count'].copy()
    data_set_final.to_csv('Outputs/data_set.csv',index=False)
    return(data_set_final)




    


