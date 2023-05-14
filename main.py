import pandas as pd

def load_hands(csv_name):
    df = pd.read_csv(csv_name)

    for ind in df.index:
        if(df.loc[ind]['Won Round'] in ['NO','No','no']):
            df.loc[ind]['Won Round'] = False
        elif (df.loc[ind]['Won Round'] in ['yes','YES','Yes']):
            df.loc[ind]['Won Round'] = True
        df['Player'].fillna('Unknown',inplace=True)
    df.dropna(inplace=True)
    df['Cards'] = df['Cards'].str.split(", ")
    return df

if __name__ == '__main__':
    df = load_hands('poker_hands.csv')
    print('** Question 1 **\n',df)
    print('\n** Question 2 **')
    filter_winners_df = df[df['Won Round'] == True]
    winning_rounds = filter_winners_df.groupby('Player').agg('count')
    winner = winning_rounds['Won Round'].idxmax()
    print('A. Most Winning Player:', winner)

    high_card_df = df[df['Hand'] == 'high card']
    cards = high_card_df['Value Cards'].value_counts()
    most_freq_card = cards.idxmax()
    print('\nB. Most frequently high card is:',most_freq_card)

    grouped = df.groupby('Hand')
    avg_hand = grouped['Won Round'].mean().sort_values(ascending=False)
    print('\nC. Success rates by hand:\n',avg_hand)

    df[['Card1', 'Card2']] = df['Value Cards'].str.split(',', expand=True)
    filtered_df = df[(df['Card1'] == 'A') | (df['Card2']=='A')]
    res = filtered_df.groupby('Player').agg('count')
    print('\n** Question 3 - Bonus **\n A. Number of Aces for each Player:\n',res['Cards'])

    df_flush = df[df['Hand'] == 'flush']
    mean = round(len(df_flush)/len(df),2)
    print(f'\nB. The dealers are fair, flush was given {mean} times this tournament ')
