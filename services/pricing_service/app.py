from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "pricing Service running!"})

if __name__ == '__main__':
    app.run(port=5003) 