# Expense-management
Manage your expense

To use expense-management app
$ git clone https://github.com/iamneha/Expense-management
$ cd Expense-management

Create virtualenv and activate it

$ pip install -f requirement.txt

Create database with name Expense_db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:neha@localhost:5432/Expense_db'

$ ipython

In [1]: from app import db

In [2]: db.create_all()

In [3]: exit

$ python app.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Open browser and add your expense
