import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# 1. Put your actual password here (with special characters safely encoded)
safe_password = quote_plus('chand@463')

# 2. Connect to MySQL
engine = create_engine(f'mysql+pymysql://root:{safe_password}@localhost:3306/ecommerce_db')

# 3. Read the CSV files
print("Reading CSVs...")
df_customers = pd.read_csv('01_Raw_Data/customers.csv')
df_orders = pd.read_csv('01_Raw_Data/orders.csv')
df_items = pd.read_csv('01_Raw_Data/order_items.csv')

# 4. Safely drop tables in reverse order of dependencies using direct execution
print("Clearing old tables...")
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS order_items;"))
    conn.execute(text("DROP TABLE IF EXISTS orders;"))
    conn.execute(text("DROP TABLE IF EXISTS customers;"))

# 5. Load tables into MySQL in the correct order (Parents first, then children)
print("Loading customers...")
df_customers.to_sql('customers', con=engine, if_exists='replace', index=False)

print("Loading orders...")
df_orders.to_sql('orders', con=engine, if_exists='replace', index=False)

print("Loading order items...")
df_items.to_sql('order_items', con=engine, if_exists='replace', index=False)

print("Success! All data loaded into MySQL.")