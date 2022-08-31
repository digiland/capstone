import os
import re
from urllib import response
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
import requests

global translator_endpoint
global cog_key
global cog_region

try:
    # Get Configuration Settings
    load_dotenv()
    cog_key = os.getenv('COG_SERVICE_KEY')
    cog_region = os.getenv('COG_SERVICE_REGION')
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'

except Exception as ex:
    print(ex)


def GetLanguage(text):
    # Default language is English
    language = 'en'

   # Use the Translator detect function
    path = '/detect'
    url = translator_endpoint + path

    # Build the request
    params = {
        'api-version': '3.0'
    }

    headers = {
    'Ocp-Apim-Subscription-Key': cog_key,
    'Ocp-Apim-Subscription-Region': cog_region,
    'Content-type': 'application/json'
    }

    body = [{
        'text': text
    }]

    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()

    # Parse JSON array and get language
    language = response[0]["language"]

    # Return the language
    return language

def Translate(text, source_language, target_language):
    translation = ''

    # Use the Translator translate function
    path = '/translate'
    url = translator_endpoint + path

    # Build the request
    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [target_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region': cog_region,
        'Content-type': 'application/json'
    }

    body = [{
        'text': text
    }]

    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()

    # Parse JSON array and get translation
    translation = response[0]["translations"][0]["text"]
    return translation




app = Flask(__name__)



# Home page route
@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")
    

@app.route("/translate", methods=['POST'])
def translate():
    # text = request.args["translate"]
    # target = request.args["target_language"]

    data = request.form

  
    text =data['translate']
    target= data['target_language']  

    language = GetLanguage(text)
    target_language = target

    translation = Translate(text, language, target_language) 

    return render_template("index.html", translation =translation)