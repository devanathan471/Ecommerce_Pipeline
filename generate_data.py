import pandas as pd
customers={"name":["Alex","Arun","Ben","Bala","Cavin"],"reg_date":["5.10.2026","6.10.2026","6.10.2026","7.10.2026","5.10.2026"]}
cus_df=pd.DataFrame(customers)
cus_df.to_csv("customers.csv", index=False)
products={"name":["AK47","Uzi","Desert Eagle"], "price":["$1200","$750","$320"]}
prd_df=pd.DataFrame(products)
prd_df.to_csv("products.csv", index=False)
orders={"ord_id":["1001","1002","1003","1004","1005"],
        "cus_id":["1","5","2","4","3"],
        "prd_id":["1","2","3","2","1"],
        "qty":["1","4","3","5","2"],
        "date":["8.10.2026","12.10.2026","15.10.2026","13.10.2026","17.10.2026"]}
ord_df=pd.DataFrame(orders)
ord_df.to_csv("orders.csv", index=False)