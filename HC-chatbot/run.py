from flask import Flask, flash, redirect, render_template, request, session, abort, get_flashed_messages
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

filenumber=int(os.listdir('saved_conversations')[-1])
filenumber=filenumber+1
file= open('saved_conversations/'+str(filenumber),"w+")
file.write('bot : Hi There! I am a medical chatbot. You can begin conversation by typing in a message and pressing enter.\n')
file.close()

app = Flask(__name__)

Flask(__name__, template_folder="templates")

english_bot = ChatBot('HealthCare',
             storage_adapter='chatterbot.storage.SQLStorageAdapter',
             logic_adapters=[
   {
       'import_path': 'chatterbot.logic.BestMatch'
   },
   
],
trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)

# database connection

import psycopg2

connection = psycopg2.connect(user = "postgres",
                                  password = "admin",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "hc_chatbot")

cursor = connection.cursor()

select_Query = "select * from user_account"

cursor.execute(select_Query)
before_record_count = cursor.rowcount 
#user_records = cursor.fetchall() 

#@app.route("/")
#def home():
#    return render_template("index.html")

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        username = request.form['username']
        return render_template("index.html", username = username)

@app.route("/new-user")
def newUser():
    return render_template("register.html")

@app.route("/register", methods=['POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # insert value in user account table
        from datetime import datetime        
        today = datetime.today()

        insert_query = """ INSERT INTO user_account (username, password, email, created_on, last_login) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (username, password, email, today, today)
        cursor.execute(insert_query, record_to_insert)
        connection.commit()

        select_Query = "select * from user_account"
        cursor.execute(select_Query)
        after_record_count = cursor.rowcount 

        if after_record_count != before_record_count:
            return home()

@app.route('/login', methods=['POST'])
def do_admin_login():
    error = ''
    username = request.form['username']
    password = request.form['password']

    select_Query = "select * from user_account WHERE username = %s AND password = %s "
    record_to_select = (username, password)
    cursor.execute(select_Query, record_to_select)
    user_records = cursor.fetchone()

    if  username == '' and password == '':
        return newUser() 
    elif not user_records[1] and user_records[2]:
        print ("Error while connecting to PostgreSQL", error)
    else:
        session['logged_in'] = True
        return home()  
    
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))

    appendfile=os.listdir('saved_conversations')[-1]
    appendfile= open('saved_conversations/'+str(filenumber),"a")
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    appendfile.close()

    return response


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='localhost', port=8000, debug=True)
