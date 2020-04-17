import pandas as pd
import numpy as np
from parser import get_dataset_from_url
from analyzer import cleaned_data_set, text_cleaner
from bokeh.models import TextInput, Button, Paragraph
from bokeh.plotting import figure, curdoc, show
from bokeh.layouts import column,Row
from bokeh.models import HoverTool
from bokeh.transform import linear_cmap
from bokeh.models import Button
from bokeh.models import *
from wordcloud import WordCloud
from bokeh.models import ImageURL
from collections import Counter
from nltk.util import ngrams
import nltk
from bokeh.models import Paragraph
import collections
from bokeh.models.widgets import Div
import os
#print(os.path.abspath(os.getcwd()))

nltk.download('punkt')

input = TextInput(value="Enter the URL to be parsed!")

def plot_stars(cleaned_data):

    star_count = cleaned_data.groupby(['Star_count']).count()['Review']
    x_value=[1,2,3,4,5]
    #Implementing column data source
    data = {'x_values': x_value,
        'y_values': star_count}

    col_datasrc = ColumnDataSource(data)
    p = figure(title='Star Ratings for 150 pages of reviews',plot_width=450, plot_height=450, background_fill_color='beige', background_fill_alpha=0.9 ,x_axis_label = 'Stars', y_axis_label = 'Count')
    labels = LabelSet(x='x_values', y='y_values', text='y_values', level='glyph',x_offset=0, y_offset=0, source=col_datasrc, render_mode='canvas', text_align='center',text_font_size='10pt')
    p.title.align='center'
    p.vbar(x='x_values', width=0.5, bottom=0, top='y_values', line_color='white',source=col_datasrc, fill_color='#58a4b0')
    p.add_layout(labels)
    return(p)

def plot_word_cloud(cleaned_data):

    words =str(cleaned_data[(cleaned_data['Star_count'] < 6 )]['Review'].values)
    word_cloud = WordCloud(max_font_size=50, max_words=100, background_color="white",width = 400,height = 400).generate(words)
    word_cloud.to_file("word_cloud.png")

    w = figure(x_range=(0,500), y_range=(0,500))
    w.xaxis.visible = False 
    w.yaxis.visible = False
    w.toolbar_location = None
    url = '/home/ubuntu/Desktop/Diwakar/Works/AI_ML/NLP/Flipkart_Parser'
    w.image_url(url="url",x=0, y=0, w=400, h=400, anchor="bottom_left")
    return(w)

    
def update_graphs():

    #Store the URL and pass it to other functions
    main_url = input.value
    input.value=""
    #Get the dataset from URL
    data_set = get_dataset_from_url(main_url)

    #Clean the data in the dataset
    cleaned_data = cleaned_data_set(data_set)
    
    #Plot the Star rating bar-graph
    star_plot = plot_stars(cleaned_data)
    #curdoc().add_root(column(star_plot))

    #Plot the word cloud
    word_cloud_img=plot_word_cloud(cleaned_data)       

    curdoc().add_root(column(star_plot,star_rating))
    return(cleaned_data_set)

def extract_ngrams(data, num, top_n):    
    
    ngrams_Xstar = ngrams(nltk.word_tokenize(data), num)
    ngrams_XFreq = collections.Counter(ngrams_Xstar)
    word_list = ngrams_XFreq.most_common(top_n)
    return(word_list)

def update_reviews(attr, old, new):

    data_set = pd.read_csv('Outputs/data_set.csv')
    i = int(star_rating.value)
    output_review_list = extract_ngrams(str(data_set[(data_set['Star_count'] == i)]['Review'].values),2,3)
    
    text1 = Paragraph(style={'font-variant': 'small-caps',
          'font-family': "Tahoma"})
    text1.text=""    
    review1 = text_cleaner(str(output_review_list[0]))
    review2 = text_cleaner(str(output_review_list[1]))
    #review3 = text_cleaner(str(output_review_list[2])
    text1.text = "Top "+str(i)+" star reviews feel: "+review1+", followed by "+review2    
    curdoc().add_root(Row(text1))

#Adding logo image to background
div_image = Div(text="""<img src="https://pngimage.net/wp-content/uploads/2018/06/review-logo-png-5.png" alt="div_image">""", width=300, height=120,
style={'opacity': '0.1'})


button = Button(label="Get Reviews")
button.on_click(update_graphs)

STAR_RATING = ['5','4','3','2','1']
star_rating = Select(value='5', title='Filter keywords by Star rating', options=STAR_RATING)
star_rating.on_change('value', update_reviews)


curdoc().add_root(column(input,button,div_image))
curdoc().title = "Flipkart Review Parser"

