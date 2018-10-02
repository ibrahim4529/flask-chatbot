from flask import Flask, render_template, request, jsonify, url_for
import aiml
import os

app = Flask(__name__)
kernel = aiml.Kernel()
def save(force):
	if force == True:
		kernel.saveBrain("bot_brain.brn")

@app.route("/")
def hello():
    return render_template('chat.html')
@app.route('/chat')
def chat():
	return render_template('chat2.html')
@app.route('/we')
def we():
	return render_template('chat3.html')

@app.route("/ask", methods=['POST','GET'])
def ask():
	message = str(request.form['chatmessage'])
	
	if os.path.isfile("bot_brain.brn"):
	    kernel.bootstrap(brainFile = "bot_brain.brn")
	else:
	    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	    kernel.saveBrain("bot_brain.brn")
	
	if message == "save":
	    save(True)
	    return jsonify({'status':'OK','answer':"Saved"})
	elif message == "quit":	
	    exit()
		

	# kernel now ready for use
	while True:
		bot_response = kernel.respond(message)
	        # print bot_response
	        return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
    app.run()
