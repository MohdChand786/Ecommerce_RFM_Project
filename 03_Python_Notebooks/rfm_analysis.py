import pandas as pd

df_rfm = pd.read_csv('../01_Raw_Data/rfm_data.csv')

print(df_rfm.describe())


# 1. Recency Score
df_rfm['R_Score'] = pd.qcut(df_rfm['recency'], q=5, labels=[5, 4, 3, 2, 1])

# 2. Monetary Score
df_rfm['M_Score'] = pd.qcut(df_rfm['monetary'], q=5, labels=[1, 2, 3, 4, 5])

# 3. Frequence Score
def score_frequency(f):
    if f==1 : return 1
    elif f==2 : return 2
    elif f==3 : return 3
    elif f==4 : return 4
    else: return 5

df_rfm['F_Score'] = df_rfm['frequency'].apply(score_frequency)


# 4. Combine into a master segment string
df_rfm['RFM_Segment'] = df_rfm['R_Score'].astype(str) + df_rfm['F_Score'].astype(str) + df_rfm['M_Score'].astype(str)


champions = df_rfm[df_rfm['RFM_Segment'] == '555']
print(f"Number of Champions (555): {len(champions)}")

df_rfm.to_csv('../01_Raw_Data/rfm_scored.csv', index=False)
print("Scored dataset saved as rfm_scored.csv!")