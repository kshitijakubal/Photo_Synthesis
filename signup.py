from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sports_synthesis'

mysql = MySQL(app)


@app.route('/signup',methods=['POST'])
def signup():
    if request.is_json:
        content = request.get_json()
        # Getting Details from JSON
        username = content['username']
        email = content['email']
        password = content['password']
        confirm_password = content['confirm_password']
        user_type = content['user_type']

        # MySql Database Connection
        cur = mysql.connection.cursor()
    
        if password == confirm_password:
            cur.execute("INSERT INTO users(username, email, password, user_type_id) VALUES (%s, %s, %s, %s)", (username, email, password, user_type))
            mysql.connection.commit()
            cur.close()
            return 'Signed Up Successfully'
        else:
            return 'Password does not match'

@app.route('/login',methods=['POST'])
def login():
    if request.is_json:
        content = request.get_json()

        id = request.args['id']
        username = content['username']
        password = content['password']

        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM users WHERE id = %s""",(id,))
        data = cur.fetchone()
        if username == data[1] and password == data[3]:
            return "Login Successful"


if __name__ == '__main__':
    app.run()