from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import openai
import webbrowser
from pyttsx3 import init
import smtplib
import random
import speech_recognition as sr
import datetime
import wolframalpha
import sys
from playsound import playsound
import wikipedia
# import wikipedia

# # Search for a page
# search_results = wikipedia.search("Python (programming language)")

# # Get the page summary
# page_summary = wikipedia.summary(search_results[0])

# print(page_summary)
engine=init('sapi5')
client=wolframalpha.Client('AYGGRU-P3473P9ETG')
voice=engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)
def speak(audio):
    print('Adua: '+ audio)
    engine.say(audio)
    engine.runAndWait()
def myCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold=1
        audio=r.listen(source)
    try:
        query=r.recognize_google(audio,language='en-in')
        print('User: '+query+ '\n')
    except sr.UnknownValueError:
        speak('Sorry Sir!,Can\'t get that! Try typing the command')
        query=str(input('Command: '))
    return query
def greetMe():
    currentH=int(datetime.datetime.now().hour)
    if currentH>=0 and currentH<12:
        speak('Good Morning!')
    if currentH>=12 and currentH<18:
        speak('Good Afternoon!')
    if currentH>=18 and currentH<=0:
        speak('Good Evening!')
data=[('Example Q: Who created this app','Example Ans: Abhay Bairagi')]
app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        openai.api_key = "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"
        query= request.form['book']
        query=query.lower()
        if 'open' and 'youtube' in query:
            data.append((query,'opening youtube'))
            webbrowser.open('www.youtube.com')
            return redirect('/')
        elif 'what\' up' in query or 'how are you' in query:
            stMsgs=['Just doing my thing','I am nice and full of energy , Thanks to my creator']
            data.append((query,random.choice(stMsgs)))
            return redirect('/')
        else:
            query=query
            try:
                try:
                    # Search for a page
                    search_results = wikipedia.search(query)
                    result= wikipedia.summary(search_results[0])
                    data.append((query,"wiki says : "+result))
                except:
                    res=client.query(query)
                    result=next(res.results).text
                    data.append((query,"wolf says :"+result))
                
            except:
                #webbrowser.open('www.google.com')  
                response = openai.Completion.create(
                model="text-davinci-003",
                prompt=query,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=[" You:", " Adua:"]
                )
                data.append((query,response.choices[0].text ))
                return redirect('/')
    return render_template('chat.html',data=data)
if __name__=='__main__':
    app.run(debug=True)
