import mysql.connector
    
    mydb = mysql.connector.connect (
    host = "localhost",
    user = "g1sec",
    password = "lala",
    database="testing" 
    )
    cursorA = mydb.cursor(buffered=True)
