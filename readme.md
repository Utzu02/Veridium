Pentru solutie se va rula index.py

# Instrucțiuni pentru utilizarea scriptului de AI pentru joc

Acest ghid te va ajuta să instalezi și să configurezi tot ce este necesar pentru a utiliza scriptul de AI creat pentru jocul tău text-based.

## 1. Instalează bibliotecile necesare

Deschide un terminal sau o fereastră de command prompt și rulează următoarele comenzi pentru a instala bibliotecile necesare:

#### Instalează `spacy`:
```bash
pip install spacy
```

#### Instalează `nltk`:
```bash
pip install nltk
```

#### Instalează modelul de limbaj pentru spaCy:
Pentru a folosi spaCy cu limbajul englez, instalează modelul de limbaj „en_core_web_md” (sau „en_core_web_sm” dacă vrei un model mai mic). Rulează această comandă pentru a-l descărca local:
```bash
python -m spacy download en_core_web_md
```

#### Instalează `wordnet` din `nltk`:
Pentru a folosi funcția de sinonime, trebuie să descarci datele necesare din WordNet, inclusiv corpusul de sinonime. Rulează următoarele comenzi:
```python
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
```

Aceste comenzi vor descărca seturile de date necesare pentru a lucra cu sinonimele din WordNet.

## 2. Pregătește fișierele CSV

Asigură-te că fișierele CSV pe care le folosești (`cuvinte.csv` și `battle_rules.csv`) sunt corect structurate.

### Exemplu de `cuvinte.csv`:
```csv
nume,cost
cuvant1,10
cuvant2,15
cuvant3,5
```

### Exemplu de `battle_rules.csv`:
```csv
loser,winner
cuvant1,cuvant2
cuvant2,cuvant3
```

Asigură-te că fișierele sunt în același director cu scriptul tău Python sau indică calea corectă către ele în cod.

## 3. Rulează scriptul

După ce ai instalat toate dependențele și ai configurat fișierele CSV, poți rula scriptul. Salvează-l într-un fișier `.py`, de exemplu `game_ai.py`.

Pentru a rula scriptul, deschide terminalul/command prompt și rulează următoarea comandă:
```bash
python game_ai.py
```

## 4. Introducerea unui cuvânt pentru a căuta câștigătorul

După ce rulezi scriptul, va apărea promptul:
```
Introdu cuvântul de învins:
```

Introdu cuvântul pentru care vrei să găsești câștigătorul, iar scriptul îți va returna cel mai ieftin câștigător disponibil.

---

După acești pași, ar trebui să poți utiliza scriptul complet și să îți găsești cel mai ieftin câștigător pentru jocul tău!