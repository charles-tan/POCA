'''
import statsmodels.api as sm
import statsmodels.formula.api as smf
data = sm.datasets.get_rdataset("dietox", "geepack").data
print(data)
md = smf.mixedlm("Weight ~ Time", data, groups=data["Pig"])
mdf = md.fit()
print(mdf.summary())
'''

import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

# drop race primary (date), candidate (name irrelevant)
# drop_cols = ['won_primary', 'primary_status', 'general_status', 'primary_pctg', 'candidate', 'primary_runoff_status']
drop_cols = ['primary_status', 'general_status', 'primary_runoff_status']

# # check if there are any null values
# print(x_dem.isnull().values.any())
# print(y_dem.isnull().values.any())
# print(x_rep.isnull().values.any())
# print(y_rep.isnull().values.any())


# encode data
encode_dem_cols = ['candidate', 'won_primary', 'state', 'district', 'office_type', 'race_type', 'race', 'veteran', 'race_primary',
    'lgbtq', 'elected_official', 'self_funder', 'stem', 'obama_alum', 'dem_party_support', 'emily_endorsed',
    'guns_sense_candidate', 'biden_endorsed', 'warren_endorsed', 'sanders_endorsed', 'our_revolution_endorsed',
    'justice_dems_endorsed', 'pccc_endorsed', 'indivisible_endorsed', 'wfp_endorsed', 'votevets_endorsed', 'no_labels_support']

encode_rep_cols = ['candidate', 'won_primary', 'state', 'district', 'office_type', 'race_type', 'race_primary_election_date',
    'rep_party_support', 'trump_endorsed', 'bannon_endorsed', 'great_america_endorsed', 'nra_endorsed',
    'right_to_life_endorsed', 'susan_b_anthony_endorsed', 'club_for_growth_endorsed', 'koch_support', 'house_freedom_support',
    'tea_party_endorsed', 'main_street_endorsed','chamber_endorsed', 'no_labels_support']


dem_df = pd.read_csv('data/dem_candidates.csv', encoding="ISO-8859-1").dropna(subset=['primary_pctg'])
rep_df = pd.read_csv('data/rep_candidates.csv', encoding="ISO-8859-1").dropna(subset=['primary_pctg'])

label_encoder = LabelEncoder()

def label_encode_data(df, encode_cols):
    for col in encode_cols:
        df[col] = label_encoder.fit_transform(df[col].values.astype(str))

    return df

dem_df_enc = label_encode_data(dem_df, encode_dem_cols)
rep_df_enc = label_encode_data(rep_df, encode_rep_cols)

dem_df_enc.to_csv('data/encoded_dem_data.csv', index=False)
rep_df_enc.to_csv('data/encoded_rep_data.csv', index=False)

x_dem = dem_df_enc.drop(drop_cols, axis=1)
dem_df_enc = dem_df_enc.drop(drop_cols, axis=1)
# y_dem = dem_df_enc[['primary_pctg', 'won_primary']]
y_dem = dem_df_enc[['primary_pctg']]
y_dem_primary_pctg = dem_df_enc['primary_pctg']
y_dem_won_primary = dem_df_enc['won_primary']

x_rep = rep_df_enc.drop(drop_cols, axis=1)
y_rep = rep_df_enc[['primary_pctg', 'won_primary']]
y_rep_primary_pctg = rep_df_enc['primary_pctg']
y_rep_won_primary = rep_df_enc['won_primary']
# print(y_dem.squeeze(axis=1).shape)
# print(y_dem.shape, x_dem.shape)
# np.column_stack([y_dem,y_dem[:,-1]])
# print(y_dem.shape, x_dem.shape)

print(len(dem_df_enc["won_primary"]))
print(dem_df_enc[['won_primary', 'veteran', 'state', 'candidate']])
# print(len(dem_df_enc.veteran))
# print(len(dem_df_enc.candidate))

# print(dem_df_enc)
model = smf.MixedLM("won_primary ~ veteran", dem_df_enc[['won_primary', 'veteran', 'state', 'candidate']], groups=dem_df_enc["candidate"]).fit()
# model = sm.OLS(dem_df_enc["won_primary"], dem_df_enc["veteran"]).fit()
# print(model.predict())

'''

def run_lin_reg(x, y, y_won_primary, y_primary_pctg):
    # x = x.dropna()
    reg = LinearRegression().fit(x, y)
    print("SCORE - both: ", reg.score(x, y))

    reg = LinearRegression().fit(x, y_won_primary)
    print("SCORE - won_primary : ", reg.score(x, y_won_primary))

    reg = LinearRegression().fit(x, y_primary_pctg)
    print("SCORE - primary_pctg: ", reg.score(x, y_primary_pctg))
    print("\n")

print("DEMOCRATIC: ")
run_lin_reg(x_dem, y_dem, y_dem_won_primary, y_dem_primary_pctg)
print("REPUBLICAN: ")
run_lin_reg(x_rep, y_rep, y_rep_won_primary, y_rep_primary_pctg)
'''
