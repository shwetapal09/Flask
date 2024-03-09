from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pal1234'
app.config['MYSQL_DATABASE_DB'] = 'userdetails'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, mobile) VALUES (%s, %s, %s)", (name, email, mobile))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('display_user', name=name))

    return render_template('Index1.html')

@app.route('/user/<string:name>')
def display_user(name):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name=%s", (name,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('user.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
