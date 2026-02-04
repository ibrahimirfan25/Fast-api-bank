from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection

app = FastAPI()

class Login_Request(BaseModel):
    account_number: int
    pin: int
    
class Deposit_Request(BaseModel):
    account_number: int
    amount: int
    
class Withdraw_Request(BaseModel):
    account_number: int
    amount: int
    
class Transfer_Request(BaseModel):
    from_account: int
    to_account : int
    amount: int


@app.post("/login")
def Login(data: Login_Request):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT account_number, name, balance FROM accounts WHERE account_number = ? and pin = ?",
        (data.account_number, data.pin)
    )
    
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return{"Success": False, "message" : "Invalid account number or pin"}
    
    return{
        "success": True,
        "account_number": user[0],
        "name": user[1],
        "balance": user[2]
    }
    

@app.get("/balance/{account_number}")
def get_balance(account_number: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT balance FROM accounts WHERE account_number = ?",
        (account_number,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return{"success" : "False", "message" : "the account number you entered is incorrect"}
    
    return {
        "Success" : "True",
        "Account_number": account_number,
        "balance": row[0]
    }
    

@app.post("/deposit")
def Deposit(data: Deposit_Request):
    if data.amount <= 0:
        return {"Success": "False", "message" : "The amount you have entered is less than zero"}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT balance FROM accounts WHERE account_number = ?",
        (data.account_number,)
    )
    
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {"successs" : "False", "message" : "Account not found"}
    
    new_balance = row[0] + data.amount
    
    cursor.execute(
        "UPDATE accounts SET balance = ? WHERE account_number = ?",
        (new_balance, data.account_number)
    )
    
    conn.commit()
    conn.close()
    
    return{
        "Success" : "True",
        "Message" : "Deposit Successfully",
        "new_balance" : new_balance
    }
        

@app.post("/withdraw")
def withdraw(data: Withdraw_Request):
    if data.amount <= 0:
        return {"Success" : "False", "message" : "Invalid value"}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT balance FROM accounts WHERE account_number = ?",
        (data.account_number,)
    )
    
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {"success": False, "message": "Account not found"}
    
    current_balance = row[0]
    
    if data.amount > current_balance:
        conn.close()
        return {"SUCCESS" : "False", "message" : "The amount you have entered is incorrect or great"}
    
    new_balance = current_balance - data.amount
    
    cursor.execute(
        "UPDATE accounts SET balance = ? WHERE account_number = ?",
        (new_balance, data.account_number)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Withdraw successful",
        "new_balance": new_balance
    }
    
@app.post("/transfer")
def transfer(data: Transfer_Request):
    if data.amount <= 0:
        return {"success": False, "message": "Amount must be greater than zero"}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_number = ?",
        (data.from_account,)
    )
    sender = cursor.fetchone()

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_number = ?",
        (data.to_account,)
    )
    receiver = cursor.fetchone()

    if not sender or not receiver:
        conn.close()
        return {"success": False, "message": "Account not found"}

    sender_balance = sender[0]

    if data.amount > sender_balance:
        conn.close()
        return {"success": False, "message": "Insufficient balance"}

    new_sender_balance = sender_balance - data.amount
    new_receiver_balance = receiver[0] + data.amount

    cursor.execute(
        "UPDATE accounts SET balance = ? WHERE account_number = ?",
        (new_sender_balance, data.from_account)
    )

    cursor.execute(
        "UPDATE accounts SET balance = ? WHERE account_number = ?",
        (new_receiver_balance, data.to_account)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Transfer successful",
        "from_account_balance": new_sender_balance
    }