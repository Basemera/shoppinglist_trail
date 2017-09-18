import os
from flask import Flask, request, render_template, flash, redirect, url_for, get_flashed_messages, session, abort
from .forms import LoginForm, RegistrationForm, ShoppingListForm, additemsForm
from . import app
from app.modals import User, shoppinglist, item, Abstract

def create_session_keys():
    if "users" not in session:
        session["users"] = {}
    if "shopping_list" not in session:
        session["shopping_list"] = {}

    if "items" not in session:
        session["items"] = {}

    if "logged_in" not in session:
        session["logged_in"] = None 


def user_redirect():
    """A method to prevent logged in users from log in and sign up pages"""
    if "logged_in" in session and session["logged_in"] is not None:
        flash({
            "message":
            "You have already logged in!"
        })
        return True
    else:
        return False

def guest_redirect():
    """A method to ensure users log in before proceeding"""
    if "logged_in" in session and session["logged_in"] is None:
        flash({
            "message":
            "Please log in to proceed"
        })
        return True
    else:
        return False


@app.route('/', methods= ['GET', 'POST'])
def index():
    create_session_keys()
    
    if "users" in session:
        return redirect('homepage')
    else:
        return redirect(url_for('signin'))


@app.route('/signup', methods= ['GET', 'POST'])
def signup():
    """Method to sign users up"""
    if user_redirect():
        return redirect(url_for('homepage')) #if user already logged in notify user
    
    create_session_keys()

    form = RegistrationForm() #registering the user

    if request.method == 'POST':
        if form.validate_on_submit():
            
            new_user = User(form.username.data, form.password.data, form.email.data)
            session["users"][new_user.userid] = vars(new_user)
            flash({"message": "You have successfully signed up! Login to continue"})

            return redirect('/signin')

        return render_template("signup.html",
                               title='Create Profile',
                               form=form)               
    elif request.method == 'GET':
        return render_template('signup.html', 
                           title='Sign up',
                           form=form)
    


@app.route('/signin', methods= ['GET', 'POST'])
def signin():
    """Method to sign users in"""
    if user_redirect():
        return redirect(url_for('homepage')) #if user already logged in notify user
    
    create_session_keys()
    
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            users = session["users"]
            for key in users:
                user = users[key]
                
                session['logged_in'] = {'username':form.username.data, 'userid': user['userid']}
                return redirect(url_for('homepage'))
            
            flash({"message":'Login failed! incorrect credentials'})
            return redirect(url_for('signin'))
    
    elif request.method == 'GET':
        return render_template('login.html', title = 'log in', form = form)

@app.route('/homepage', methods= ['GET', 'POST'])
def homepage():
    create_session_keys()
    return render_template('homepage.html')

@app.route('/createlist', methods= ['GET', 'POST'])
def createlist():
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))
    form = ShoppingListForm()

    if form.validate_on_submit():
        newlist = shoppinglist(form.listname.data)
        session["shopping_list"][newlist.list_id] = vars(newlist)
        flash({"message": "You have successfully created a shopping list! Select it to start adding items to it"})
        return redirect(url_for('viewlist'))
    return render_template('createlist.html', form = form)

@app.route('/updatelist/<list_id>', methods= ['GET', 'POST'])
def updatelist(list_id):
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))
    form = ShoppingListForm()

    if form.validate_on_submit():
        session['shopping_list'][list_id]['listname'] = form.listname.data
        flash('message: Update successful')
        return redirect(url_for('viewlist'))
    shoppinglists = session['shopping_list'][list_id]

    return render_template('updatelist.html', form = form, 
                                            listname = shoppinglists['listname'],
                                            list_id = list_id )
    
@app.route('/deletelist', methods= ['GET', 'POST'])    
def deletelist(list_id):
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))
    form = ShoppingListForm()
    if form.validate_on_submit():
        del session['shopping_list']['list_id']
        flash('message: delete successful')
        return redirect(url_for('viewlist'))
    shoppinglists = session['shopping_list']['list_id']

    return render_template('view3.html', form = form, 
                                            listname = shoppinglists['listname'],
                                            list_id = list_id )


@app.route('/viewlist', methods= ['GET', 'POST'])
def viewlist():
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))

    form = ShoppingListForm()
    form_item = additemsForm()

    return render_template("viewlist.html",
                           title='View Shopping Lists',
                           lists=session["shopping_list"],
                            items = session["items"],
                           form=form,
                           user=session["logged_in"]["userid"],
                           form_item = form_item)

@app.route('/additem/<id>', methods= ['GET', 'POST'])
def additem(id):
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))

    form = additemsForm()
    
    if form.validate_on_submit():
        
        new_item = item(form.itemname.data, form.quantity.data, form.price.data, id)
        
        session["items"][new_item.item_id] = vars(new_item)
        
        flash({"message":
                "item successfully added"})
        return redirect(url_for('viewlist'))

    return render_template('additem.html', form = form, list_id=id)



