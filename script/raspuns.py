import csv
import spacy
from collections import defaultdict
from nltk.corpus import wordnet

# Încărcăm modelul de NLP pentru embeddings (modelul mic de engleză, local)
nlp = spacy.load("en_core_web_md")  # Folosim modelul mic pentru limba engleză

# Încărcăm datele din fișierele CSV
def load_data():
    words = {}
    with open('cuvinte.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words[row['nume'].lower()] = int(row['cost'])  # Transformăm cuvintele în lowercase

    battle_rules = defaultdict(list)
    with open('battle_rules.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            battle_rules[row['loser'].lower()].append(row['winner'].lower())  # Transformăm cuvintele în lowercase
    
    return words, battle_rules

# Funcție pentru a găsi sinonimele unui cuvânt folosind WordNet
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())  # Transformăm sinonimele în lowercase
    return synonyms

# Funcție pentru a calcula similaritățile între cuvinte
def find_similar_losers(input_word, battle_rules, threshold=0.5):
    input_word = input_word.lower()  # Transformăm cuvântul de intrare în lowercase
    # Extragem toți "loser"-ii din reguli
    all_losers = list(battle_rules.keys())
    
    # Calculăm similaritatea dintre input_word și fiecare "loser"
    input_doc = nlp(input_word)
    similarities = []
    for loser in all_losers:
        loser_doc = nlp(loser)
        sim = input_doc.similarity(loser_doc)
        if sim >= threshold:
            similarities.append((loser, sim))
    
    # Sortăm descrescător după similaritate
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [loser for loser, sim in similarities]

# Funcție pentru a găsi cel mai ieftin "winner" posibil
def find_cheapest_winner(input_word, words, battle_rules):
    input_word = input_word.lower()  # Transformăm cuvântul de intrare în lowercase
    # Caz 1: Cuvântul este direct în reguli
    if input_word in battle_rules:
        possible_winners = battle_rules[input_word]
    else:
        # Caz 2: Căutăm sinonime și similarități cu alți "loser"-i
        similar_losers = find_similar_losers(input_word, battle_rules)
        possible_winners = []
        
        # Adăugăm sinonimele cuvintelor la lista de posibili câștigători
        synonyms = get_synonyms(input_word)
        possible_winners.extend(synonyms)
        
        # Extindem cuvintele similare care pot fi câștigătoare
        for loser in similar_losers:
            possible_winners.extend(battle_rules.get(loser, []))
    
    # Filtrăm cuvinte valide și găsim cel mai ieftin
    valid_winners = [(word, cost) for word, cost in words.items() if word in possible_winners]
    
    # Dacă nu există câștigători, adăugăm o garanție ca cel puțin un câștigător să fie valid
    if not valid_winners:
        return list(words.keys())[0]  # Alegem primul câștigător disponibil, pentru a evita lipsa unui câștigător valid
    
    return min(valid_winners, key=lambda x: x[1])[0]

# Exemplu de utilizare
words, battle_rules = load_data()
input_word = input("Introdu cuvântul de învins: ")

# Căutăm cel mai ieftin câștigător
cheapest_winner = find_cheapest_winner(input_word, words, battle_rules)

if cheapest_winner:
    print(f"Cel mai ieftin câștigător pentru '{input_word}' este '{cheapest_winner}' (cost: {words[cheapest_winner]}).")