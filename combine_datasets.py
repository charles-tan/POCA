import pandas as pd

dem_df = pd.read_csv('data/encoded_dem_data.csv', encoding="ISO-8859-1").dropna(subset=['primary_pctg'])
rep_df = pd.read_csv('data/encoded_rep_data.csv', encoding="ISO-8859-1").dropna(subset=['primary_pctg'])

dem_endorsements = ['obama_alum','dem_party_support','emily_endorsed','guns_sense_candidate','biden_endorsed',
    'warren_endorsed','sanders_endorsed','our_revolution_endorsed','justice_dems_endorsed','pccc_endorsed', 
    'indivisible_endorsed','wfp_endorsed','votevets_endorsed','no_labels_support']

rep_endorsements = ['rep_party_support', 'trump_endorsed', 'bannon_endorsed', 'great_america_endorsed', 
    'nra_endorsed', 'right_to_life_endorsed', 'susan_b_anthony_endorsed', 'club_for_growth_endorsed',
    'koch_support', 'house_freedom_support', 'tea_party_endorsed', 'main_street_endorsed', 'chamber_endorsed', 'no_labels_support']

print("REPUBLICAN NULL: \n")
for col in rep_df.columns:
    print(col + " pctg null: ", rep_df[col].isna().sum() / len(rep_df[col]))

print("\nDEMOCRATIC NULL: \n")
for col in dem_df.columns:
    print(col + " pctg null: ", dem_df[col].isna().sum() / len(dem_df[col]))

def add_endorsements(df, endorsement_cols):
    num_e = 0
    num_non_e = 0
    num_e_col = []
    num_non_e_col = []
    for i, r in df.iterrows():
        num_e = 0
        num_non_e = 0
        for e in endorsement_cols:
            if r[e] == 1:
                num_e += 1
            elif r[e] == 0:
                num_non_e += 1

        num_e_col.append(num_e)
        num_non_e_col.append(num_non_e)

    df['num_endorsements'] = num_e_col
    df['num_non_endorsements'] = num_non_e_col

    return df

dem_df = add_endorsements(dem_df, dem_endorsements)
dem_df.to_csv('data/dem_num_endorsements.csv', index=False)

rep_df = add_endorsements(rep_df, rep_endorsements)
rep_df.to_csv('data/rep_num_endorsements.csv', index=False)
