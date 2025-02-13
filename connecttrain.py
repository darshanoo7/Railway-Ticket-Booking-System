from flask import Flask, render_template, request

app = Flask(__name__, template_folder='C:\\Users\\Asus\\OneDrive\\Desktop\\template')

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    train_no = request.form['train_no']
    train_name = request.form['train_name']
    arrival_time= request.form['arrival_time']
    return render_template('confirmation.html', train_no=train_no, train_name=train_name, arrival_time=arrival_time)

if __name__ == '__main__':
    app.run(debug=True)