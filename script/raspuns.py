import pandas as pd
import os

def load_battle_rules():
    if os.path.exists("battle_rules.csv"):
        df = pd.read_csv("battle_rules.csv", header=None, names=['winner', 'loser'])
        df['winner_lower'] = df['winner'].str.lower()
        df['loser_lower'] = df['loser'].str.lower()
        return df
    return pd.DataFrame(columns=['winner', 'loser', 'winner_lower', 'loser_lower'])

def load_prices():
    if os.path.exists("cuvinte.csv"):
        df = pd.read_csv("cuvinte.csv", header=None, names=['word', 'price'])
        df['word_lower'] = df['word'].str.lower()
        return df
    return pd.DataFrame(columns=['word', 'price', 'word_lower'])

def find_cheapest_winner(target_word, battles, prices):
    target_lower = target_word.lower()
    
    # Găsim toate cuvintele câștigătoare (case insensitive)
    relevant_battles = battles[battles['loser_lower'] == target_lower]
    all_winners = relevant_battles['winner_lower'].unique()
    
    # Cuvinte valide din lista de prețuri
    valid_winners = prices[prices['word_lower'].isin(all_winners)]
    
    if not valid_winners.empty:
        # Sortare după preț și nume
        sorted_winners = valid_winners.sort_values(by=['price', 'word'])
        return sorted_winners
    return None

def main():
    battles = load_battle_rules()
    prices = load_prices()
    
    if prices.empty:
        print("Eroare: Fișierul cuvinte.csv nu există sau este gol")
        return
    
    while True:
        target = input("\nIntrodu cuvântul țintă (sau 'exit' pentru a închide): ").strip()
        if target.lower() == 'exit':
            break
            
        result = find_cheapest_winner(target, battles, prices)
        
        if result is not None:
            print("\nCuvinte câștigătoare disponibile:")
            for idx, row in result.iterrows():
                print(f" - {row['word']} (Preț: {row['price']})")
            
            cheapest = result.iloc[0]
            print(f"\nCel mai ieftin cuvânt care bate '{target}': {cheapest['word']} (Preț: {cheapest['price']})")
        else:
            print(f"\nNu există înregistrări pentru cuvinte care să bată '{target}'")

if __name__ == "__main__":
    main()