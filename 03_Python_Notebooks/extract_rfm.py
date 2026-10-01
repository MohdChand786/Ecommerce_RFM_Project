import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

safe_password = quote_plus('chand@463')
engine= create_engine(f'mysql+pymysql://root:{safe_password}@localhost:3306/ecommerce_db')


query = """
SELECT c.customer_unique_id, DATEDIFF('2018-10-17', MAX(STR_TO_DATE(LEFT(o.order_purchase_timestamp, 10), '%%d-%%m-%%Y'))) AS recency, COUNT(DISTINCT o.order_id) AS frequency, SUM(oi.price + oi.freight_value) AS monetary FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY customer_unique_id
ORDER BY monetary DESC;
"""

print("Extracting data from MySQL... (This may take 10-20 seconds)")
df_full = pd.read_sql(query, con=engine)



df_full.to_csv('../01_Raw_Data/rfm_data.csv', index=False)

print(f"Success! Extracted {len(df_full)} rows to rfm_data.csv")