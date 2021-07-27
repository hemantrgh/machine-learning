# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 13:49:32 2021

@author: Hemant Ghodke
"""

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import Word
from flask import Flask, render_template, request, jsonify
import string

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('dictionary-ui.html')


@app.route('/', methods=['POST'])
def dictionary():
    if request.method == 'POST':
        try:
            input_txt = request.form.get('input_txt')
            print(input_txt)
            if input_txt:
                clear_txt = clean_text(request.form.get('input_txt'))
                synonyms = Word(clear_txt).definitions
                output = []
                for i in range (0, len(synonyms)-1):
                    output.append(synonyms[i].title()) 
                return render_template("dictionary-ui.html", result=output)
            else:
                return render_template("dictionary-ui.html", error="Please enter the text")
        except Exception as e:
            return (str(e))

    
@app.route('/result', methods = ['GET', 'POST'])
def result():
    clear_txt = clean_text(request.form.get('input_txt'))
    synonyms = Word(clear_txt).definitions
    output = []
    for i in range (0, len(synonyms)-1):
        output.append(synonyms[i].title()) 

    return render_template('dict-res-ui.html', result="\n".join(output))

word_lemmatizer = WordNetLemmatizer()
def clean_text(input_text):
    clean_data = []
    for word in nltk.word_tokenize(input_text):
        if word not in string.punctuation:
            if word not in stopwords.words('english'):
                clean_data.append(word_lemmatizer.lemmatize(word, pos='v'))
    return " ".join(clean_data)

if __name__ == '__main__':
    app.run(debug=True)

