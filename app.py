from flask import Flask, request, redirect, render_template, jsonify
import simpleclient as oo
import os
app = Flask(__name__)

@app.route("/bot")
def index():
	#Oos.system("python3 ./botserver.py")
	return render_template('index.html')


@app.route("/bot/ask", methods=["POST"])
def ask():
	msg = request.form
	while True:
		message=msg['messageText']
		if message == "quit":
			ask()
		elif message == "exit" or message == "exit()":
			ask()
		else:
			bot_response=oo.client(message)
			return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
	#os.system("python botserver.py")
	app.run(host='localhost')
