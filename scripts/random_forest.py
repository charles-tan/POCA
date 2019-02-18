import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression

dem_df = pd.read_csv('../data/dem_num_endorsements.csv', encoding="ISO-8859-1").dropna(subset=['primary_pctg'])
rep_df = pd.read_csv('../data/rep_num_endorsements.csv', encoding="ISO-8859-1").dropna(subset=['primary_pctg'])

# drop race primary (date), candidate (name irrelevant)
drop_cols = ['won_primary', 'primary_status', 'general_status', 'primary_pctg', 'candidate', 'primary_runoff_status', 
'num_non_endorsements', 'num_endorsements']
def run_random_forest(df):
    msk = np.random.rand(len(df)) < 0.8
    train = df[msk]
    test = df[~msk]

    train_x = train.drop(drop_cols, axis=1)
    train_y = train[['primary_pctg', 'won_primary']]
    train_y_primary_pctg = train['primary_pctg']
    train_y_won_primary = train['won_primary']


    test_x = test.drop(drop_cols, axis=1) 
    test_y = test[['primary_pctg', 'won_primary']]
    test_y_primary_pctg = test['primary_pctg']
    test_y_won_primary = test['won_primary']

    regr = RandomForestRegressor(max_depth=2, random_state=0, n_estimators=100)
    regr.fit(train_x, train_y)

    regr.score(test_x, test_y)
    feature_importances = pd.DataFrame(regr.feature_importances_, index = train_x.columns, columns=['importance']).sort_values('importance',ascending=False)
    print(feature_importances)

print("REPUBLICAN: ")
run_random_forest(rep_df)

# drop_cols.append('partisan_lean')
print("DEMOCRATIC: ")
run_random_forest(dem_df)
print("\n")