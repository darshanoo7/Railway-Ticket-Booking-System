from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='C:\\Users\\Asus\\OneDrive\\Desktop\\template')

# Function to create a new user table if it doesn't exist
def create_table():
    conn = sqlite3.connect('railway_registration.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name varchar(25) NOT NULL,
                        middle_name varchar(25),
                        last_name varchar(25) NOT NULL,
                        gender TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        mobile INTEGER NOT NULL,
                        city varchar(25) NOT NULL,
                        state varchar(25) NOT NULL,ṇ
                        pincode INTEGER NOT NULL,
                        train_name varchar(25) DEFAULT 'nan',
                        train_no INTEGER DEFAULT 'nan',
                        arrival_time TIME DEFAULT 'nan',
                        destination varchar(25) DEFAULT 'nan')''')
    conn.commit()
    conn.close()

def alter_table():
    conn = sqlite3.connect('railway_registration.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(user)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]

    if 'train_name' in column_names:
        cursor.execute('''ALTER TABLE user RENAME TO user_old''')
        cursor.execute('''CREATE TABLE user (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name varchar(25) NOT NULL,
                            middle_name varchar(25),
                            last_name varchar(25) NOT NULL,
                            gender TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            mobile INTEGER NOT NULL,
                            city varchar(25) NOT NULL,
                            state varchar(25) NOT NULL,
                            pincode INTEGER NOT NULL,
                            train_name varchar(25) DEFAULT 'nan',
                            train_no INTEGER DEFAULT 'nan',
                            arrival_time TIME DEFAULT 'nan',
                            destination varchar(25) DEFAULT 'nan')''')
        cursor.execute('''INSERT INTO user SELECT * FROM user_old''')
        cursor.execute('''DROP TABLE user_old''')

    conn.commit()
    conn.close()

alter_table()

# Function to delete a user registration based on ID
@app.route('/delete', methods=['POST'])
def delete_user():
    user_id = request.form['id']
    conn = sqlite3.connect('railway_registration.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return 'Data deleted successfully.'

# Function to insert a new user record
@app.route('/insert', methods=['POST'])
def insert_data():
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    age = request.form['age']
    mobile = request.form['mobile']
    city = request.form['city']
    state = request.form['state']
    pincode = request.form['pincode']
    train_name = request.form['train_name']
    train_no = request.form['train_no']
    arrival_time = request.form['arrival_time']
    destination = request.form['destination']

    conn = sqlite3.connect('railway_registration.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (first_name, middle_name, last_name, gender, age, mobile, city, state, pincode, train_name, train_no, arrival_time, destination) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (first_name, middle_name, last_name, gender, age, mobile, city, state, pincode, train_name, train_no, arrival_time, destination))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return render_template('delete.html', user_id=user_id)

# Route to display inserted data
@app.route('/view')
def view_data():
    conn = sqlite3.connect('railway_registration.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, first_name, middle_name, last_name, gender, age, mobile, city, state, pincode, train_name, train_no, arrival_time, destination FROM user")
    users = cursor.fetchall()
    conn.close()
    return render_template('view.html', users=users)

# Main function to display the form
@app.route('/')
def display_form():
    return render_template('user.html')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)