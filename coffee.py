# MySQL Connectivity
import mysql.connector as sqltor
from config import MYSQL_CONFIG  # Import the configuration
mycon = sqltor.connect(**MYSQL_CONFIG)
csr = mycon.cursor()

# ------------Functions-------------------------

# Returns a list of coworker ids excluding person


def getRest(id):       # List of tuples[(name,id,price)]
    csr.execute(
        "select name,cid,price from coworkers where cid!='{}'".format(id))
    rest = csr.fetchall()
    return rest


def getAllCoworkers():  # List of tuples[(name,id,price)]
    csr.execute("SELECT name, cid, price,count FROM coworkers")
    names = csr.fetchall()
    return names

# Returns total bill amount
def generateBill():
    csr.execute("select sum(price) from coworkers")
    total = csr.fetchone()
    return total[0]

# Calculates cumulative debts of each person and updates the cloumn in the coworker table


def updateDebts():
    for i in getAllCoworkers():
        # Fetch amountOwed
        q1 = "SELECT COALESCE(SUM(amount), 0) FROM payment WHERE payee = %s"
        csr.execute(q1, (i[1],))
        amountOwed = csr.fetchone()[0]

        # Fetch amountPaid
        q2 = "SELECT COALESCE(SUM(amount), 0) FROM payment WHERE payer = %s"
        csr.execute(q2, (i[1],))
        amountPaid = csr.fetchone()[0]

        # Calculate debt
        debt = amountOwed - amountPaid
        # Update in coworkers table
        q3 = "UPDATE coworkers SET debt = %s WHERE cid = %s"
        csr.execute(q3, (debt, i[1]))
        mycon.commit()

# Returns the id of the person with the most cumulative debt


def calculateMaxDebt():
    updateDebts()
    csr.execute("SELECT MAX(debt) AS max_debt, (SELECT cid FROM coworkers WHERE debt = (SELECT MAX(debt) FROM coworkers) LIMIT 1) AS max_cid,(SELECT name FROM coworkers WHERE cid = (SELECT cid FROM coworkers WHERE debt = (SELECT MAX(debt) FROM coworkers) LIMIT 1) LIMIT 1) AS max_name FROM coworkers")
    result = csr.fetchone()
    max_debt, max_cid, max_name = result[0], result[1], result[2]
    return max_debt, max_cid, max_name

# Executes the payment and records the transaction


def newTransaction():
    # Checking for first transaction
    csr.execute("select * from coworkers where debt!=0")
    check = csr.fetchall()
    if (not check):
        # Random person goes first
        id=getAllCoworkers()[0][1]
        generatePayments(id, getRest(getAllCoworkers()[0][1]))
        csr.execute("select count from coworkers where cid='{}'").format(id)
        count=csr.fetchall()
        print(count)
        c=count[0][0]+ 1
        csr.execute("UPDATE coworkers SET count = '{}' WHERE cid = '{}'").format(c, id)        

    # Person with the most cumulative debt pays
    else:
        d, nextPayerId,nextPayerName = calculateMaxDebt()
        csr.execute("select count from coworkers where cid='{}'".format(nextPayerId))
        count=csr.fetchall()
        print(count)
        c=count[0][0]+ 1
        csr.execute("UPDATE coworkers SET count = '{}' WHERE cid = '{}'".format(c, nextPayerId))        
        print("next payer:", nextPayerId, " ",nextPayerName )
        print('debt:', d)
        generatePayments(nextPayerId, getRest(nextPayerId))
        print('transaction complete !')
        # print("inside coffee: ")
        # csr.execute("SELECT name, drink_preference, price, debt,count FROM coworkers")
        # coworker_values = csr.fetchall()
        # print('values',coworker_values)


def generatePayments(payer_id, restOfCoworkers):
    # Total price of drinks
    total = generateBill()

    transaction_query = "INSERT INTO transactions(tdate, amount, payer) VALUES (CURDATE(), %s, %s)"
    csr.execute(transaction_query, (total, payer_id))
    tid = csr.lastrowid  # transaction id

    for coworker in restOfCoworkers:
        # get drink price
        cost = coworker[2]
        q2 = "insert into payment(payer,payee,amount,tid) values('{}','{}','{}','{}')".format(
            payer_id, coworker[1], cost, tid)
        csr.execute(q2)

    mycon.commit()
    updateDebts()

