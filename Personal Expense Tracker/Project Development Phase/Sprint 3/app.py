from flask import Flask,render_template,redirect,url_for,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, date

todays_date = date.today()


app = Flask(__name__)
app.secret_key = "made by humans"
app.permanent_session_lifetime = timedelta(days=6)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#creating db models
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),unique=True,nullable=False)
    fname = db.Column(db.String(20),nullable=False)
    lname = db.Column(db.String(20))
    pswd = db.Column(db.String(50),nullable=False,default=None)
    expense = db.relationship('Expense', backref='user')
    income = db.relationship('Income', backref='user')
    
    def __repr__(self):
        return f'<User "{self.fname}">'

class  Expense(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(50),nullable=True,default=None)
    category = db.Column(db.String(50),nullable=True,default=None)
    amount = db.Column(db.Integer,nullable=False)
    date = db.Column(db.String(10),nullable=True,default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #date
    #payer

    def __repr__(self):
        return f'<Expense "{self.amount}">'

class  Income(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(50),nullable=True,default=None)
    category = db.Column(db.String(50),nullable=True,default=None)
    amount = db.Column(db.Integer,nullable=False)
    date = db.Column(db.String(10),nullable=True,default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #payer

    def __repr__(self):
        return f'<Income "{self.amount}">'

class  Payer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    #user

    def __repr__(self):
        return f'<Payer "{self.name}">'

#Routes
@app.route('/',methods = ["POST","GET"])
def dashboard():
    if ("email" in session) and ("pswd" in session) and (session["pswd"] == User.query.filter_by(email=session["email"]).first().pswd) :
        if request.method == "POST":
            if request.form['submit'] == 'quick_expense' and request.form['amount']:
                description = request.form['description']
                category = request.form['category']
                date = request.form['date']
                #payer = request.form['payer']
                amount = request.form['amount']
            else:
                flash("Enter amount")
                return redirect(url_for('dashboard'))

            if session["email"]:
                usr_id = User.query.filter_by(email=session['email']).first().id
                expense = Expense(description=description,category=category,date=date,amount=amount,user_id=usr_id)
                db.session.add(expense)
                db.session.commit() 
                flash("Expense amount "+str(expense.amount)+"₹ added successfully")

            return redirect(url_for('dashboard'))  
        else:
            flash("Logged In Successfull")
            #Get view
            totalExpense = 0            
            monthlyExTotal = 0  
            monthlyExpenses = [0,0,0,0,0,0,0,0,0,0,0,0]            
            weeklyExpenses = [0,0,0,0]
            weeklyExTotal = 0
            for expense in User.query.filter_by(email=session['email']).first().expense:
                if expense.date[:4] == str(todays_date.year):             
                    totalExpense += expense.amount #total year expense 
                    for month in range(12):
                        if  int(expense.date[5:7])  == month+1:
                            monthlyExpenses[month] += expense.amount #monthly expense list
                if expense.date[:4] == str(todays_date.year) and expense.date[5:7] == str(todays_date.month):
                    monthlyExTotal += expense.amount #total monthly expense
                    if int(expense.date[-2:])<8:
                        if todays_date.day < 8 : weeklyExTotal += expense.amount
                        weeklyExpenses[0] += expense.amount
                    elif int(expense.date[-2:])<16:
                        if todays_date.day < 16 : weeklyExTotal += expense.amount
                        weeklyExpenses[1] += expense.amount
                    elif int(expense.date[-2:])<24:
                        if todays_date.day < 24 : weeklyExTotal += expense.amount
                        weeklyExpenses[2] += expense.amount
                    elif int(expense.date[-2:])<32:
                        if todays_date.day < 32 : weeklyExTotal += expense.amount
                        weeklyExpenses[3] += expense.amount

            totalIncome = 0
            monthlyInTotal = 0 
            monthlyIncomes = [0,0,0,0,0,0,0,0,0,0,0,0]
            weeklyIncomes = [0,0,0,0]
            weeklyInTotal = 0
            for income in User.query.filter_by(email=session['email']).first().income:
                if expense.date[:4] == str(todays_date.year):
                    totalIncome += income.amount #total year income
                    for month in range(12):
                        if  int(income.date[5:7])  == month+1:
                            monthlyIncomes[month] += income.amount #monthly expense list
                if income.date[:4] == str(todays_date.year) and income.date[5:7] == str(todays_date.month):
                    monthlyInTotal += income.amount #total monthly expense
                    if int(income.date[-2:])<8:
                        if todays_date.day < 8 : weeklyInTotal += income.amount
                        weeklyIncomes[0] += income.amount
                    elif int(expense.date[-2:])<16:
                        if todays_date.day < 16 : weeklyInTotal += income.amount
                        weeklyIncomes[1] += income.amount
                    elif int(expense.date[-2:])<24:
                        if todays_date.day < 24 : weeklyInTotal += income.amount
                        weeklyIncomes[2] += income.amount
                    elif int(expense.date[-2:])<32:
                        if todays_date.day < 32 : weeklyInTotal += income.amount
                        weeklyIncomes[3] += income.amount

            data ={
                "balance": totalIncome-totalExpense,
                "yearlyStats": totalExpense,
                "monthlyStats": monthlyExTotal,
                "weeklyStats": weeklyExTotal,
                "monthlyEx": monthlyExpenses,
                "weeklyEx": weeklyExpenses,
                "monthlyIn": monthlyIncomes,
                "weeklyIn": weeklyIncomes,
                "recent": User.query.filter_by(email=session["email"]).first().expense[:6]
            }
            return render_template('dashboard.html',data = data)
    else:
        return redirect(url_for('login'))

@app.route('/login',methods = ["POST","GET"])
def login():
    if request.method =="POST":
        email = request.form['email']
        pswd = request.form['pswd']
        
        if ((User.query.filter_by(email=email).first().email == email) and (User.query.filter_by(email=email).first().pswd == pswd)):
            session["email"] = User.query.filter_by(email=email).first().email
            session["pswd"] = User.query.filter_by(email=email).first().pswd
            session["fname"] = User.query.filter_by(email=email).first().fname
            
            if request.form.get('check') == "remember":
                session.permanent = True
            else:
                session.permanent = False
        else:
            flash("Incorrect Credentials")
        
        return redirect(url_for('dashboard'))
    else:
        if ("email" in session) and ("pswd" in session):
            flash("Already Logged In")
            return redirect(url_for('dashboard'))
        return render_template('login.html')

@app.route('/signup',methods = ["POST","GET"])
def signup():
    if request.method =="POST":
        if (request.form['fname'] and request.form['email'] and request.form['pswd']):
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            pswd = request.form['pswd']
        else:
            flash("Enter All Details")
            return redirect(url_for('signup')) 

        if not User.query.filter_by(email=email).first():
            #print(fname+" "+lname+"\n"+email)  
            usr = User(email=email,fname=fname,lname=lname,pswd=pswd)
            db.session.add(usr)
            db.session.commit() 
            flash(User.query.filter_by(email=email).first().email+" added successfully")
            return redirect(url_for('login'))  
        else:
            flash("User already Exist") 
            return redirect(url_for('signup'))      
    else:
        return render_template('signup.html')

@app.route('/resetpassword',methods = ["POST","GET"])
def reset():
    if request.method =="POST":
        if (request.form['email'] and request.form['npswd']):
            email = request.form['email']
            pswd = request.form['npswd']
        else:
            flash("Enter All Details")
            return redirect(url_for('reset')) 
        if User.query.filter_by(email=email).first():
            User.query.filter_by(email=email).first().pswd = pswd
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash("User Not Exist") 
            return redirect(url_for('reset'))
    else:
        return render_template('resetpassword.html')

@app.route('/changepassword',methods = ["POST","GET"])
def changePwd():
    if request.method =="POST":
        if (request.form['opswd'] and request.form['npswd']):
            email = request.form['email']
            opswd = request.form['opswd']
            npswd = request.form['npswd']
        else:
            flash("Enter All Details")
            return redirect(url_for('changePwd')) 
        if User.query.filter_by(email=email).first():
            if User.query.filter_by(email=email).first().pswd == opswd :
                User.query.filter_by(email=email).first().pswd = npswd
                session["pswd"] = User.query.filter_by(email=email).first().pswd
                db.session.commit()
                flash("Password Changed successfully")
            else:
                flash("Incorrect password")
                return redirect(url_for('changePwd'))
            return redirect(url_for('dashboard'))
        else:
            flash("Enter All Details")
            return redirect(url_for('changePswd')) 

    else:
        return render_template('changePassword.html')

@app.route('/logout')
def logout():
    session.pop("email",None)
    session.pop("pswd",None)
    flash("logged Out Successfull")
    return redirect(url_for('login'))

@app.route('/manage/income',methods = ["POST","GET"])
def income():
    if request.method =="POST":
            #Quick Income
            if request.form["submit"] == "quick_income":
                if request.form['amount']:
                    description = request.form['description']
                    category = request.form['category']
                    date = request.form['date']
                    #payer = request.form['payer']
                    amount = request.form['amount']

                    if session["email"]:
                        usr_id = User.query.filter_by(email=session['email']).first().id
                        income = Income(description=description,category=category,date=date,amount=amount,user_id=usr_id)
                        db.session.add(income)
                        db.session.commit() 
                        flash("Income amount "+str(income.amount)+"₹ added successfully")
                    else:
                        flash("Income not added")
                else:
                    flash("Enter amount")
                    return redirect(url_for('income'))

            #edit Income
            elif request.form['submit'] == "edit_income":
                if request.form['Eamount']:
                    description = request.form['Edescription']
                    category = request.form['Ecategory']
                    date = request.form['Edate']
                    #payer = request.form['payer']
                    amount = request.form['Eamount']
                    income_id = request.form['Eid']
                    print(amount)

                    if session["email"]:
                        usr_id = User.query.filter_by(email=session['email']).first().id
                        Income.query.filter_by(id= income_id).first().descrption = description
                        Income.query.filter_by(id= income_id).first().category = category
                        Income.query.filter_by(id= income_id).first().date = date
                        Income.query.filter_by(id= income_id).first().amount = amount
                        db.session.commit() 
                        flash("Income amount "+str(Income.query.filter_by(id= income_id).first().amount)+"₹ added successfully")
                    else:
                        flash("Income not added")
                else:
                    flash("Enter amount")
                    return redirect(url_for('income'))      
                
            #delete Income
            elif request.form['submit'] == "delete_income":
                if request.form['incomeId']:
                    incomeId = request.form['incomeId']
                    income = Income.query.filter_by(id= incomeId).first()
                    db.session.delete(income)
                    db.session.commit()
            
            return redirect(url_for('income'))
    else:
        incomes = User.query.filter_by(email=session['email']).first().income
        return render_template('income.html', data = incomes)

@app.route('/manage/expense',methods = ["POST","GET"])
def expense():
    if request.method =="POST":
        #Quick Expense
        if request.form["submit"] == "quick_expense":
            if request.form['amount']:
                description = request.form['description']
                category = request.form['category']
                date = request.form['date']
                #payer = request.form['payer']
                amount = request.form['amount']

                if session["email"]:
                    usr_id = User.query.filter_by(email=session['email']).first().id
                    expense = Expense(description=description,category=category,date=date,amount=amount,user_id=usr_id)
                    db.session.add(expense)
                    db.session.commit() 
                    flash("Expense amount "+str(expense.amount)+"₹ added successfully")
                else:
                    flash("Expense not added")
            else:
                flash("Enter amount")
                return redirect(url_for('expense'))

        #edit Expense
        elif request.form['submit'] == "edit_expense":
            if request.form['Eamount']:
                description = request.form['Edescription']
                category = request.form['Ecategory']
                date = request.form['Edate']
                #payer = request.form['payer']
                amount = request.form['Eamount']
                expense_id = request.form['Eid']
                print(amount)

                if session["email"]:
                    usr_id = User.query.filter_by(email=session['email']).first().id
                    Expense.query.filter_by(id=expense_id).first().descrption = description
                    Expense.query.filter_by(id=expense_id).first().category = category
                    Expense.query.filter_by(id=expense_id).first().date = date
                    Expense.query.filter_by(id=expense_id).first().amount = amount
                    db.session.commit() 
                    flash("Expense amount "+str(Expense.query.filter_by(id=expense_id).first().amount)+"₹ added successfully")
                else:
                    flash("Expense not added")
            else:
                flash("Enter amount")
                return redirect(url_for('expense'))      
            
        #delete Expense
        elif request.form['submit'] == "delete_expense":
            print("Hello")
            if request.form['expenseId']:
                expenseId = request.form['expenseId']
                expense = Expense.query.filter_by(id=expenseId).first()
                print(expense)
                db.session.delete(expense)
                db.session.commit()
        
        return redirect(url_for('expense'))
    else:
        expenses = User.query.filter_by(email=session['email']).first().expense
        return render_template('expenses.html', data = expenses)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)