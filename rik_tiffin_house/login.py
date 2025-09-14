import mysql.connector

# connect to MySQL
conn = mysql.connector.connect(
    host="localhost",      
    user="root",           
    password="Riksingha@615", 
    database="rik_tiffin"      
)

cursor = conn.cursor()

# take input
name = input("Enter your name: ")
number = int(input("Enter your mobile number: "))
address = input("Enter your address: ")

# insert into table (make sure you have a table called customers)
query = "INSERT INTO customers (name, number, address) VALUES (%s, %s, %s)"
values = (name, number, address)
cursor.execute(query, values)

# commit to save changes
conn.commit()
print("✅ Data inserted successfully!")

# fetch and display all rows
cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()
print("\nAll records:")
for row in rows:
    print(row)



# close connection
cursor.close()
conn.close()
