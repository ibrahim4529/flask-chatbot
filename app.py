from flask import Flask, render_template, request, jsonify, url_for
import aiml
import os

kernel = aiml.Kernel()

def load_kern(forcereload):
	if os.path.isfile("bot_brain.brn") and not forcereload:
		kernel.bootstrap(brainFile= "bot_brain.brn")
	else:
		kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
		kernel.saveBrain("bot_brain.brn")


app = Flask(__name__)
@app.route("/")
def hello():
	load_kern(False)
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
	if message == "save":
	    kernel.saveBrain("bot_brain.brn")
	    return jsonify({"status":"ok", "answer":"Brain Saved"})
	elif message == "reload":
		load_kern(True)
		return jsonify({"status":"ok", "answer":"Brain Reloaded"})
	elif message == "quit":
		exit()
		return jsonify({"status":"ok", "answer":"exit Thank You"})

	# kernel now ready for use
	else:
		# while True:
		bot_response = kernel.respond(message)
		# print bot_response
		return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
    app.run(debug=False)
