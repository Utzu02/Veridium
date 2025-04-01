# 🔥 Words of Power - AI Battle System

[![Hackathon Challenge](https://img.shields.io/badge/🔰_Hackathon_Challenge-Click_Here-FF6B6B?style=for-the-badge)](https://soleadify.notion.site/Hackathon-Challenge-Words-of-Power-1a52a4d999ed8021bb92dde896a630a5)

**Sistem AI care determină cel mai eficient/ieftin cuvânt pentru a învinge un inamic dat**, folosind reguli custom și NLP pentru cuvinte necunoscute!

![Battle System Demo](https://via.placeholder.com/800x400.png?text=Run+main.py+to+see+magic!🪄)

## 🚀 Cum funcționează?
| Componentă              | Descriere                                                                 |
|-------------------------|---------------------------------------------------------------------------|
| 📜 **Reguli explicite**  | Folosește `battle_rules.csv` pentru match-uri directe                     |
| 🧠 **NLP Semantic**      | Găsește analogii între cuvinte cu spaCy                                   |
| 💸 **Fallback strategic**| Alege mereu cel mai ieftin cuvânt dacă nu există alte opțiuni             |

## 🛠️ Instalare
```bash
# 1. Instalare spaCy + model românesc
pip install spacy
python -m spacy download ro_core_news_md

# 2. Clonează repository-ul (opțional)
git clone https://github.com/username/words-of-power.git
cd words-of-power

# 📂 Rulează în folderul proiectului:
python raspuns.py (main.py este scriptul care ruleaza doar in timpul concursului)

# 🧪 Exemplu input:
# > Introdu cuvântul de învins: câine
# > Câștigător garantat: 'catel' (cost: 5)
