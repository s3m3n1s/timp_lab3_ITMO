from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open('ip_inf.json', 'r') as file:
    users = json.load(file)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/crt')
def crt():
    ip = request.remote_addr
    data = request.args.get('data')
    users[ip] = data
    print(users)
    return 'OK'


@app.route('/add')
def add():
    ip = request.remote_addr
    data = request.args.get('mem')
    users[ip] += "|memory=" + data + "."
    with open("ip_inf.json", 'w') as file:
        json.dump(users, file)
    return 'OK'


if __name__ == '__main__':
    app.run()
