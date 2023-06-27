from flask_login import login_required
from flask import Blueprint, render_template, request, flash, jsonify
import openai

gtw = Blueprint("gtw", __name__)

message = None

@gtw.route('/gtw', methods=['GET', 'POST'])
#@login_required
def gtr():
    global message
    if request.method == 'POST':
        openai.api_key = "your_api_key" #It is recommended to use an .env file
        global userinput
        global payload

        userinput = "None"
        def Ask(msg):
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=msg)
            global message
            message = response.choices[0].text
        
        def getInput():
            userinput = request.form.get("question")
            Ask(userinput)
            
        getInput()


    return render_template("gtw.html")

@gtw.route('/getmsg', methods=['GET'])
def getmsg():
    global message
    if message is None:
        error = "Error occured"
        message = jsonify(error)
    return str(message)