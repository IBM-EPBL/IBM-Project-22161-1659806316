from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session, flash
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

import ibm_db

dsn_hostname = "764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
dsn_uid = "gfw33074"
dsn_pwd = "9s4qVEi8iBtYttud"
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"
dsn_port = "32536"
dsn_protocol = "TCPIP"
dsn_security = "SSL"
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,
                            dsn_security)

conn = ibm_db.connect(dsn, "", "")

print(conn)
print("Connecting Successful............")

app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/signup")
def signup():

    return render_template("signup.html")


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        name = request.form['registerFullName']
        username = request.form['registerUsername']
        email = request.form['registerEmailid']
        password = request.form['registerPassword1']
        repass = request.form['registerPassword2']


        sql = "SELECT * FROM COUSTMER_DETAILS  WHERE name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:

            return render_template('signup.html', msg="You are already a member, please login using your details")

        else:
            insert_sql = "INSERT INTO COUSTMER_DETAILS VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.bind_param(prep_stmt, 5, repass)
            ibm_db.execute(prep_stmt)

    return render_template('home.html', msg="Retailer Login successfuly..")


@app.route("/home")
def hello():
    return render_template("home.html")


@app.route("/about")
def profile():
    return render_template("about.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

# @app.route("/chat")
# def chat():
#     return render_template("chat.html", messages=messages)

# messages =[{"title":"message one", "content":"message one content"},{"title":"message one", "content":"message one content"},{"title":"message two","content":"message two content"}]

# @app.route("/create/", methods=('GET','POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']


#         if not title:
#             flash('Title is required!')
#         elif not content:
#             flash('Content is required!')
#         else:
#             messages.append({'title':title, 'content':content})
#             name= 'ganesh'
#             return redirect(url_for('index', messages=messages ))
#     return render_template('create.html')


# @app.route("/creat/" , methods=('GET','POST'))
# def create():
#     if request.method=='POST':
#         title = request.form['title']


# @app.route('/')
# def index():
#     return render_template('index.html', messages=messages)

# @app.route('/admin')
# def hello_admin():
#     return 'hello admin'

# @app.route('/guest/<guest>')
# def hello_guest(guest):
#     return 'hello %s as Guest' % guest

# @app.route('/user/<name>')
# def hello_user(name):
#     if name== 'admin':
#         return redirect(url_for('hello_adimin'))
