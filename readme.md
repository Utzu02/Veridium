Pentru solutie se va rula index.py

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