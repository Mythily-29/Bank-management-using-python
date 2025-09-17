from functools import wraps
import random

id_generate=[1,2,3,4,5,6,7,8,9,0]

random_id=int(''.join(map(str,random.sample(id_generate,k=3))))

def check_email_exists(f): #check if the email already existing
    @wraps(f)
    def wrapper(*args,**kwargs):
        email=kwargs.get('email','')

        for user in Users.signed_user_details:
            if user['email']==email:
                print('Already email exists')
                return
        return f(*args,**kwargs)
        
    return wrapper

def check_login_details(f): #checking validation when the user is login in
    @wraps(f)

    def wrapper(*args,**kwargs):
        email=kwargs.get('email')
        password=kwargs.get('password')
        check_email=None

        for user in Users.signed_user_details:
            if email == user['email']:
                check_email=user
                break

        if not check_email:
            print('Cannot fetch the invalid details')
            return 

        if check_email['password']!=password:
            print('You have entered password wrongly')
            return 
        kwargs['sign_id'] = check_email['sign_id']
        return f(*args,**kwargs)
    return wrapper

class Users: #class to do sign up and login functions

    signed_user_details=[{'sign_id':123,'name':'anu','email':'anu@gmail.com','password':'1234',},
                         {'sign_id':456,'name':'nobi','email':'nobi@gmail.com','password':'1234',},
                         {'sign_id':111,'name':'kio','email':'kio@gmail.com','password':'1234',}]

    @staticmethod
    @check_email_exists
    def Signup(name,email,password):
        Users.signed_user_details.append({'sign_id':random_id,'name':name,'email':email,'password':password})
        print(f'{name} has been successfully registered !!')

    @staticmethod
    @check_login_details
    def Login(*args,**kwargs):
        email=kwargs.get('email')
        get_id=kwargs.get('sign_id')
        print(f'{email} has been successfully logined and your id {get_id} !!')
        while True:
            print('Welcome to DCKAP Bank \n 1. Check Balance \n 2. Deposit \n 3. Withdraw \n 4. Transfer Money \n 5. Transaction History \n 6. Logout')   
            try:
                user_login_input=int(input('Select any one of option from 1-6 :'))
                if user_login_input==1:
                    Accounts.user_account_details.append({'sign_id':get_id,'balance':0,'deposit':[],'withdraw':[],'transaction_history':[]})
                    Accounts.check_balance(get_id)
                elif user_login_input==2:
                    amount=int(input('Enter amount to add :'))
                    Accounts.Deposit(get_id,amount)
                elif user_login_input==3:
                    amount=int(input('Enter amount to withdraw :'))
                    Accounts.Withdraw(get_id,amount)
                elif user_login_input==4:
                    transfer_id=int(input('Enter id to transfer id :'))
                    transfer_amount=int(input('Enter money to transfer :'))
                    Accounts.Transfer_money(get_id,transfer_id,transfer_amount)
                elif user_login_input==5:
                    Accounts.Transaction_history(get_id)
                elif user_login_input==6:
                    print('Logoutted')
                    break
                else:print('Invalid option selected')

            except Exception as e:
                print('You selected invalid option',e)

def default_id_checking(id,acc): #getting details from the id
    for user in Accounts.user_account_details if acc else Users.signed_user_details:
        if user['sign_id'] == id:
            return user

class Accounts(): #Doing accounts related operations
    user_account_details=[{'sign_id':123,'balance':0,'deposit':[],'withdraw':[],'transaction_history':[]},
                          {'sign_id':456,'balance':0,'deposit':[],'withdraw':[],'transaction_history':[]},
                          {'sign_id':111,'balance':0,'deposit':[],'withdraw':[],'transaction_history':[]}]
    
    @staticmethod    
    def check_balance(id):
        get=default_id_checking(id,acc=True)
        print(f'Your balance amount is Rs.{get["balance"]}')

    @staticmethod
    def Deposit(id,amount):
        get=default_id_checking(id,acc=True)
        if amount > 0:
            get['balance'] += amount
            get['deposit'].append(f'Deposited Rs.{amount}')
            get['transaction_history'].append(f'Deposited Rs.{amount}')
            print(f'Deposited Rs.{amount}')
        else:
            print('Enter amount greater than 0')

    def Withdraw(id,amount):
        get=default_id_checking(id,acc=True)
        if amount > 0 and amount < get['balance']:
            get['balance'] -= amount
            get['withdraw'].append(f'Withdrawed Rs.{amount}')
            get['transaction_history'].append(f'Withdrawed Rs.{amount}')
            print(f'Withdrawed Rs.{amount}')
        else:
            print('Enter sufficient amount or dont enter negative balance')

    def Transfer_money(uid,tid,amount):
        get_one=default_id_checking(uid,acc=True)
        get_two=default_id_checking(tid,acc=True)
        if uid==tid:
            print('Same id cannot transfer money')
            return
        if get_two:
            if amount > 0 and amount < get_one['balance']:
                balance=get_two['balance']
                get_one['balance'] -= amount
                get_two['balance'] =balance+amount
                get_one['transaction_history'].append(f'Transfered Rs.{amount} to {get_two["sign_id"]}')
                get_two['transaction_history'].append(f'Credited Rs.{amount} from {get_one["sign_id"]}')
                print(f'Transfered Rs.{amount} to {get_two["sign_id"]}')
            else:
                print('Enter sufficient amount')
        else:
            print('Cannot fetch the invalid details id')

    def Transaction_history(id):
        get=default_id_checking(id,acc=True)
        for i in get['transaction_history']:
            print(i)

def login_user():
    email=input('Enter your email :')
    password=input('Enter your password :')
    Users.Login(email=email,password=password)

def signup_user():
    name=input('Enter your name :')
    email=input('Enter your email :')
    password=input('Enter your password :')
    Users.Signup(name=name,email=email,password=password)

user_obj={
    1: login_user,
    2: signup_user, 
}

while True: #Loop to repeatedly asking the input from the user
    print('===== Welcome to DCKAP Bank =====\n 1. Login \n 2. Signup \n 3. Exit')
    try:
        user_input=int(input('Enter a option from (1-3) :'))
        if user_input==3:
            print('Exitted')
            break
        action=user_obj.get(user_input,0)
        action()

    except Exception as e:
        print('Invalid option')
