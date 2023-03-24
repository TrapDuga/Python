from login_app import app
from flask import render_template, redirect,request,session,flash
from login_app.models.user import User




######################################################
#                   HOME PAGE
######################################################
@app.route('/')
def display():
    return render_template('index.html')

######################################################
#                POST REGISTER FORM
######################################################
@app.route('/welcome',methods=['POST'])
def register_user():
    if not User.validate_register(request.form):
        return redirect('/')
    
    #this generates password submitted in form
    # print("-------------------------------> ", user_id)
    User.register(request.form)
    # session['first_name'] = user_id.first_name
    return redirect('/dashboard')

@app.route('/login',methods=['post'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    session['user_id'] = User.validate_login(request.form).id
    return redirect('/dashboard')
######################################################
#                     DASHBOARD
######################################################



@app.route('/dashboard')
def show_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    #build at user getbyid classmethod
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')