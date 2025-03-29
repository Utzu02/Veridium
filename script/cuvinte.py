import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

class SystematicWordBattler:
    def __init__(self):
        self.allowed_words = self.load_words()
        self.existing_rules = self.load_rules()
        
    def load_words(self):
        """Încarcă lista de cuvinte din fișierul cuvinte.csv"""
        df = pd.read_csv("cuvinte.csv", header=None)
        return df[1].tolist()  # Presupunem că cuvintele sunt în prima coloană

    def load_rules(self):
        """Încarcă regulile existente din battle_rules.csv"""
        if os.path.exists("battle_rules.csv"):
            df = pd.read_csv("battle_rules.csv", header=None, names=['word1', 'word2'])
            return set(zip(df['word1'], df['word2']))
        return set()

    def save_rule(self, winner, loser):
        """Salvează o nouă regulă în fișier"""
        with open("battle_rules.csv", "a") as f:
            f.write(f"{winner},{loser}\n")
        self.existing_rules.add((winner, loser))

    def ask_api(self, challenger, target):
        """Întreabă API-ul dacă challenger bate target"""
        prompt = (
            f"Decide dacă '{challenger}' învinge conceptual pe '{target}'. "
            f"Exemple corecte: Apă > Foc, Scut > Săgeată. "
            f"Răspunde doar cu 'da' sau 'nu'."
        )
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 2
                },
                timeout=10
            )
            return response.json()['choices'][0]['message']['content'].lower().startswith('da')
        except Exception as e:
            print(f"Eroare API: {e}")
            return False

    def process_all_combinations(self):
        """Procesează toate combinațiile posibile de cuvinte"""
        total = len(self.allowed_words)
        
        for idx, target in enumerate(self.allowed_words):
            print(f"\nProcesez cuvântul țintă ({idx+1}/{total}): {target}")
            
            for challenger in self.allowed_words:
                if challenger == target:
                    continue
                
                # Verifică dacă regula există deja
                if (challenger, target) in self.existing_rules:
                    continue
                
                # Întreabă API-ul
                if self.ask_api(challenger, target):
                    self.save_rule(challenger, target)
                    print(f"✅ {challenger} > {target}")
                else:
                    print(f"⏩ {challenger} nu bate {target}")

if __name__ == "__main__":
    battler = SystematicWordBattler()
    battler.process_all_combinations()
    print("\nProcesare completă! Toate combinațiile au fost verificate.")