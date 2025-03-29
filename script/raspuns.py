import pandas as pd
import os
import spacy
from spacy import util

# Verifică și încarcă modelul linguistic
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("Vă rugăm să instalați modelul român pentru spaCy:")
    print("python -m spacy download ro_core_news_lg")
    exit()

def load_battle_rules():
    if os.path.exists("battle_rules.csv"):
        df = pd.read_csv("battle_rules.csv", header=None, names=['winner', 'loser'])
        df['loser_lower'] = df['loser'].str.lower()
        return df
    return pd.DataFrame(columns=['winner', 'loser', 'loser_lower'])

def load_prices():
    if os.path.exists("cuvinte.csv"):
        df = pd.read_csv("cuvinte.csv", header=None, names=['word', 'price'])
        df['word_lower'] = df['word'].str.lower()
        return df
    return pd.DataFrame(columns=['word', 'price', 'word_lower'])

def get_similar_words(target, allowed_words):
    target_doc = nlp(target.lower())
    similarities = []
    
    for word in allowed_words:
        word_doc = nlp(word.lower())
        similarity = target_doc.similarity(word_doc)
        similarities.append((word, similarity))
    
    return sorted(similarities, key=lambda x: x[1], reverse=True)

def find_all_winners(target, battles, prices):
    target_lower = target.lower()
    
    # Caută în regulile directe
    direct_winners = battles[battles['loser_lower'] == target_lower]['winner'].tolist()
    
    # Dacă nu găsește, caută similare
    if not direct_winners:
        allowed_words = prices['word'].tolist()
        similar_words = get_similar_words(target, allowed_words)
        
        for word, _ in similar_words:
            similar_lower = word.lower()
            winners = battles[battles['loser_lower'] == similar_lower]['winner'].tolist()
            if winners:
                direct_winners = winners
                break
    
    # Verifică prețurile
    valid_winners = prices[prices['word'].isin(direct_winners)]
    return valid_winners.sort_values(by='price')

def main():
    battles = load_battle_rules()
    prices = load_prices()
    
    if prices.empty:
        print("Fișierul cuvinte.csv nu a fost găsit sau este gol")
        return
    
    while True:
        target = input("\nIntrodu cuvântul țintă (sau 'exit' pentru a închide): ").strip()
        if target.lower() == 'exit':
            break
            
        results = find_all_winners(target, battles, prices)
        
        if not results.empty:
            print("\nOpțiuni disponibile ordonate după preț:")
            for idx, row in results.iterrows():
                print(f"{row['word']} - {row['price']} RON")
            
            print(f"\nCea mai bună opțiune: {results.iloc[0]['word']} ({results.iloc[0]['price']} RON)")
        else:
            print(f"\nNu există înregistrări pentru cuvinte care să bată '{target}'")

if __name__ == "__main__":
    main()