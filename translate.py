from dotenv import load_dotenv
import os
import requests, json

def main():
    global translator_endpoint
    global cog_key
    global cog_region

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')
        translator_endpoint = 'https://api.cognitive.microsofttranslator.com'

      #Get text from user from the command line
        text = input("Enter text you would like to translate:  ")
        if len(text) < 5000:
            # Detect the language
            language = GetLanguage(text)
            target_language = input("Enter target language code eg 'en', 'de', 'fr', 'hi' ")
            print('Source language:',language)

           
            translation = Translate(text, language, target_language)
            print("\nTranslation:\n{}".format(translation))

        else:
            print("The text exceeds maximum limit of 5000 characters")
                
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

if __name__ == "__main__":
    main()
