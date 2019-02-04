import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

full_df = pd.read_csv('data/dem_candidates.csv', encoding="ISO-8859-1") # drop dates

# TODO: encode



x = full_df.drop(['won_primary', 'primary_pctg'], axis=1)
y = full_df[['won_primary', 'primary_pctg']]
print(type(y.won_primary.values))
y['won_primary'] = label_encoder.fit_transform(y.won_primary.values.astype(str))

print(y)


# reg = LinearRegression().fit(x, y)
# print(reg.score(x, y))