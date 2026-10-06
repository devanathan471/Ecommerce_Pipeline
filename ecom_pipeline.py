import psycopg
import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()
DB_config={"host":os.getenv("DB_HOST"),"user":os.getenv("DB_USER"),"password":os.getenv("DB_PASSWORD"),"dbname":os.getenv("ECOM_DB_NAME"),"port":os.getenv("DB_PORT")}
def db_setup():
 with psycopg.connect(**DB_config) as conn:
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS customers CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS products CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS orders CASCADE;")
        cursor.execute("CREATE TABLE IF NOT EXISTS customers(cus_id SERIAL PRIMARY KEY,name TEXT NOT NULL, reg_date TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS products(prd_id SERIAL PRIMARY KEY,item_name TEXT UNIQUE NOT NULL,price TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS orders(ord_id SERIAL PRIMARY KEY,qty TEXT, date TEXT,cs_id INTEGER,pd_id INTEGER, FOREIGN KEY(cs_id) REFERENCES customers(cus_id), FOREIGN KEY(pd_id) REFERENCES products(prd_id))")
        conn.commit()
def load_csv():
    with psycopg.connect(**DB_config) as conn:
      with conn.cursor() as cursor:
        cus_df=pd.read_csv("customers.csv")
        prd_df=pd.read_csv("products.csv")
        ord_df=pd.read_csv("orders.csv")
        for index , rows in cus_df.iterrows():
         cursor.execute("INSERT INTO customers(name,reg_date) VALUES(%s,%s)",(rows['name'],rows['reg_date'],))
        for index,rows in prd_df.iterrows():
           cursor.execute("INSERT INTO products(item_name,price) VALUES(%s,%s) ON CONFLICT (item_name) DO NOTHING",(rows["name"],rows["price"],))
        for index,rows in ord_df.iterrows():
           cursor.execute("INSERT INTO orders(cs_id,pd_id,qty,date) VALUES(%s,%s,%s,%s)",(rows["cus_id"],rows["prd_id"],rows["qty"],rows["date"],))
        cursor.execute("SELECT * FROM customers")
        c_rows=cursor.fetchall()
        print("CUSTOMER TABLE")
        for row in c_rows:
           print(row)
        cursor.execute("SELECT * FROM products")
        p_rows=cursor.fetchall()
        print("PRODUCT TABLE")
        for row in p_rows:
           print(row)
        cursor.execute("SELECT * FROM orders")
        o_rows=cursor.fetchall()
        print("ORDERS TABLE")
        for row in o_rows:
           print(row)
def run_analytics():
   with psycopg.connect(**DB_config) as conn:
      with conn.cursor() as cursor:
       # cursor.execute("SELECT c.name, SUM(o.qty::INTEGER * REPLACE(p.price,'$','')::NUMERIC)AS total_spent FROM customers c JOIN orders o ON c.cus_id=o.cs_id JOIN products p ON p.prd_id=o.pd_id GROUP BY c.name ORDER BY total_spent DESC; ")
        #c = cursor.fetchall()
        #print("TOTAL REVENUE PER CUSTOMER\n")
        #print(c)
        cursor.execute("SELECT p.item_name, SUM(o.qty::INTEGER) AS total_qty FROM products p JOIN orders o ON o.pd_id=p.prd_id GROUP BY p.item_name ORDER BY total_qty DESC;")
        d = cursor.fetchall()
        #print("TOTAL SELLING PRODUCTS BY QUANTITY")
        #print(d)
        #cursor.execute("SELECT p.item_name, SUM(o.qty::INTEGER)AS total_qty FROM products p JOIN orders o ON o.pd_id=p.prd_id WHERE o.date >'15.10.2026' GROUP BY p.item_name ORDER BY total_qty DESC;")
        #e=cursor.fetchall()
        #print(e)
        #cursor.execute("SELECT p.item_name, SUM(o.qty::INTEGER) AS total_qty FROM products p JOIN orders o ON o.pd_id=p.prd_id JOIN customers c ON c.cus_id=o.cs_id WHERE o.date>'11.10.2026' AND o.qty::INTEGER>1 GROUP BY p.item_name ORDER BY total_qty DESC;")
        #e=cursor.fetchall()
        #print(e)
        df=pd.DataFrame(d,columns=["Product name","Total_sold"])
        #print(df)
        plt.bar(df["Product name"],df["Total_sold"])
        plt.title("Sale detail")
        plt.xlabel("Product name")
        plt.ylabel("Total_sold")
        plt.show()
if __name__ =="__main__":
   db_setup()
   load_csv()
   run_analytics()