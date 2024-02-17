# MySQL Connectivity
import mysql.connector as sqltor
mycon = sqltor.connect(
    host='localhost',
    user='root',
    passwd='harikakondur',
    database='coffee')
csr = mycon.cursor()
# ------------Functions-------------------------

# Returns a list of coworker ids excluding person


def getRest(id):       # List of tuples[(name,id,price)]
    csr.execute(
        "select name,cid,price from coworkers where cid!='{}'".format(id))
    rest = csr.fetchall()
    return rest


def getAllCoworkers():  # List of tuples[(name,id,price)]
    csr.execute("SELECT name, cid, price FROM coworkers")
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

# Returns the id of the person with the most cumulative debt


def calculateMaxDebt():
    updateDebts()
    csr.execute("SELECT MAX(debt) AS max_debt, (SELECT cid FROM coworkers WHERE debt = (SELECT MAX(debt) FROM coworkers) LIMIT 1) AS max_cid FROM coworkers")
    result = csr.fetchone()
    return result[0], result[1]

# Executes the payment and records the transaction


def newTransaction():
    # Checking for first transaction
    csr.execute("select * from coworkers where debt!=0")
    check = csr.fetchall()
    if (not check):
        # Random person goes first
        generatePayments(getAllCoworkers()[0][1], getRest(
            getAllCoworkers()[0][1]))
    # Person with the most cumulative debt pays
    else:
        d, nextPayerId = calculateMaxDebt()
        name = [coworker[0] for coworker in getAllCoworkers() if coworker[1] == nextPayerId][0]
        print("next payer:", nextPayerId, " ", name)
        print('debt:', d)
        generatePayments(nextPayerId, getRest(nextPayerId))
        print('transaction complete !')


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


# newTransaction()
debt, id = calculateMaxDebt()
csr.execute("SELECT name FROM coworkers WHERE cid='{}'".format(id))
name = csr.fetchall()
print(name[0])
