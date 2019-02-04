import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

full_df = pd.read_csv('data/dem_candidates.csv', encoding="ISO-8859-1").dropna(subset=['primary_pctg'])
print(full_df.primary_runoff_status.unique())


# drop race primary (date), candidate (name irrelevant)
drop_cols = ['won_primary', 'primary_status', 'general_status', 'primary_pctg', 'candidate', 'primary_runoff_status']

x = full_df.drop(drop_cols, axis=1) 
y = full_df[['primary_pctg', 'won_primary']]

print(x.isnull().values.any())
print(y.isnull().values.any())

encode_x_cols = ['state', 'district', 'office_type', 'race_type', 'race', 'veteran', 'race_primary',
    'lgbtq', 'elected_official', 'self_funder', 'stem', 'obama_alum', 'party_support', 'emily_endorsed',
    'guns_sense_candidate', 'biden_endorsed', 'warren_endorsed', 'sanders_endorsed', 'our_revolution_endorsed',
    'justice_dems_endorsed', 'pccc_endorsed', 'indivisible_endorsed', 'wfp_endorsed', 'votevets_endorsed', 'no_labels_support']

onehot_x_cols = []

# TODO: encode
for col in encode_x_cols:
    x[col] = label_encoder.fit_transform(x[col].values.astype(str))

y['won_primary'] = label_encoder.fit_transform(y['won_primary'].values.astype(str))
x.to_csv('data/encoded_dem_data.csv', encoding='utf-8', index=False)

y_won_primary = y['won_primary']
y_primary_pctg = y['primary_pctg']

# x = x.dropna()
reg = LinearRegression().fit(x, y)
print("SCORE - both: ", reg.score(x, y))

reg = LinearRegression().fit(x, y_won_primary)
print("SCORE - won_primary : ", reg.score(x, y_won_primary))

reg = LinearRegression().fit(x, y_primary_pctg)
print("SCORE - primary_pctg: ", reg.score(x, y_primary_pctg))