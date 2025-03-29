import csv
import spacy
from collections import defaultdict
from nltk.corpus import wordnet

# Încărcăm modelul de NLP pentru embeddings
nlp = spacy.load("en_core_web_md")  # Modelul mic pentru limba engleză

# Încărcăm datele din fișierele CSV
def load_data():
    words = {}
    battle_rules = defaultdict(list)
    
    with open('cuvinte.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words[row['nume'].lower()] = {
                'id': row['id'],  # Stocăm și ID-ul cuvântului
                'cost': int(row['cost'])  # Costul cuvântului
            }
    
    with open('battle_rules.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            battle_rules[row['loser'].lower()].append(row['winner'].lower())  # Toate cuvintele în lowercase
    
    return words, battle_rules

# Cache pentru sinonime
synonym_cache = {}

# Funcție pentru a găsi sinonimele unui cuvânt folosind WordNet
def get_synonyms(word):
    if word in synonym_cache:
        return synonym_cache[word]  # Dacă avem deja sinonimele, le returnăm direct
    
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())  # Sinonimele sunt adăugate în lowercase
    
    synonym_cache[word] = synonyms  # Salvăm sinonimele în cache
    return synonyms

# Funcție pentru a calcula similaritățile între cuvinte (optimizată pentru a nu repeta calculul)
def find_similar_losers(input_word, battle_rules, threshold=0.5):
    input_word = input_word.lower()  # Cuvântul de intrare în lowercase
    input_doc = nlp(input_word)  # Procesăm cuvântul de intrare doar o dată
    similarities = []

    for loser in battle_rules:
        loser_doc = nlp(loser)  # Procesăm fiecare "loser" doar o dată
        sim = input_doc.similarity(loser_doc)
        if sim >= threshold:
            similarities.append((loser, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [loser for loser, _ in similarities]

# Funcție pentru a găsi cel mai ieftin "winner" posibil
def find_cheapest_winner(input_word, words, battle_rules):
    input_word = input_word.lower()  # Cuvântul de intrare în lowercase
    
    # Căutăm cuvinte similare "loser" din reguli
    similar_losers = find_similar_losers(input_word, battle_rules)
    possible_winners = set(get_synonyms(input_word))  # Sinonimele cuvântului de intrare

    # Extindem lista cu câștigători pe baza similitudinilor și regulilor de bătălie
    for loser in similar_losers:
        possible_winners.update(battle_rules.get(loser, []))
    
    # Filtrăm cuvintele valide și găsim cel mai ieftin
    valid_winners = [
        (word, cost['id'], cost['cost']) for word, cost in words.items() if word in possible_winners
    ]
    
    if not valid_winners:
        return words[next(iter(words))]['id']  # Dacă nu există câștigători, alegem primul ID disponibil
    
    return min(valid_winners, key=lambda x: x[2])[1]  # Returnăm ID-ul celui mai ieftin câștigător

# Exemplu de utilizare
words, battle_rules = load_data()
input_word = input("Introdu cuvântul de învins: ")

# Căutăm cel mai ieftin câștigător
cheapest_winner_id = find_cheapest_winner(input_word, words, battle_rules)

if cheapest_winner_id:
    print(f"Cel mai ieftin câștigător pentru '{input_word}' este cuvântul cu ID-ul '{cheapest_winner_id}'.")