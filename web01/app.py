from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    number1 = float(request.form['number1'])
    number2 = float(request.form['number2'])
    operation = request.form['operation']

    result = None
    if operation == 'add':
        result = number1 + number2
    elif operation == 'subtract':
        result = number1 - number2

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
