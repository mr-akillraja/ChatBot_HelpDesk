from flask import Flask,render_template,request,jsonify
import os
from dotenv import load_dotenv
import openai
from gevent.pywsgi import WSGIServer


load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"]
#print(openai.api_key)

# setup a Flask app
app = Flask(__name__)

# define the HomePage
@app.route("/")
def home():
    return render_template("sample.html")

# define the Chat Route  
@app.route("/chatbot",methods = ['POST'])
def chatbot():
# get the message from the user.
    user_input= request.form['message']
    # use Openai API to generate Response
    prompt = f"User : {user_input}\n Chatbot : "
    chat_history = []
    # creation openai engine's to response
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt = prompt,
        temperature = 0.5,
        max_tokens = 60,
        top_p = 1,
        frequency_penalty = 0,
        stop=['\n User : ','\nChatBot : ']
    )
    
    # extract the response from the Result
    bot_response = response.choices[0].text.strip()

    


    # add the user input and bot respomse to the chat history 
    chat_history.append(f"User : {user_input}\n ChatBot : {bot_response}")

    # render the chatbot template with the response text
    return render_template(
        "sample.html",
        user_input = user_input,
        bot_response = bot_response
    )






if __name__ == "__main__":
    # http_server = WSGIServer(("127.0.0.1", 8080), app)
    # http_server.serve_forever()
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
