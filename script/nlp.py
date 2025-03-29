import os
import numpy as np
import pandas as pd
import random
import requests
from dotenv import load_dotenv
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense
from tensorflow.keras.optimizers import Adam

load_dotenv()

# Common English words list for random targets
ENGLISH_WORDS = [
    # Natură & Elemente
    'fire', 'water', 'earth', 'air', 'metal', 'wood', 'stone', 'ice', 'storm',
    'light', 'dark', 'shadow', 'sun', 'moon', 'star', 'sky', 'wind', 'rain',
    'snow', 'fog', 'cloud', 'river', 'lake', 'ocean', 'wave', 'island', 'desert',
    'mountain', 'valley', 'forest', 'tree', 'root', 'leaf', 'flower', 'fruit',
    'seed', 'thorn', 'ash', 'dust', 'ember', 'flame', 'quicksand', 'crystal',

    # Corp & Materie
    'body', 'mind', 'spirit', 'soul', 'heart', 'bone', 'blood', 'skin', 'vein',
    'nerve', 'flesh', 'eye', 'hand', 'tongue', 'voice', 'breath', 'pulse', 'scar',
    'tear', 'wound', 'shell', 'core', 'frame', 'shape', 'form', 'mirror',

    # Emoții & Stări
    'fear', 'hope', 'joy', 'anger', 'love', 'hate', 'grief', 'desire', 'dream',
    'nightmare', 'peace', 'rage', 'envy', 'pride', 'shame', 'guilt', 'bliss',
    'doubt', 'faith', 'regret', 'madness', 'lust', 'calm',

    # Timp & Spațiu
    'time', 'year', 'day', 'night', 'dawn', 'dusk', 'twilight', 'eternity',
    'moment', 'hour', 'past', 'future', 'present', 'void', 'infinity', 'cycle',
    'season', 'clock', 'path', 'road', 'gate', 'portal', 'threshold', 'realm',
    'dimension', 'edge', 'horizon',

    # Abstracte & Filosofice
    'truth', 'lie', 'logic', 'chaos', 'order', 'freedom', 'control', 'destiny',
    'fate', 'will', 'choice', 'chance', 'karma', 'balance', 'duality', 'origin',
    'purpose', 'meaning', 'illusion', 'reality', 'wisdom', 'knowledge',
    'ignorance', 'belief', 'vision', 'insight', 'instinct', 'memory',

    # Simboluri & Artefacte
    'crown', 'sword', 'dagger', 'shield', 'armor', 'arrow', 'bow', 'coin', 'ring',
    'scroll', 'book', 'page', 'script', 'sigil', 'mark', 'seal', 'chain', 'lock',
    'key', 'mirror', 'mask', 'cloak', 'gem', 'crystal', 'stone', 'altar', 'staff',
    'orb', 'torch', 'blade', 'fang', 'claw', 'horn',

    # Forțe & Acțiuni
    'force', 'power', 'energy', 'gravity', 'magnetism', 'spark', 'beam', 'blast',
    'shock', 'wave', 'eruption', 'quake', 'surge', 'charge', 'whisper', 'echo',
    'call', 'chant', 'ritual', 'curse', 'blessing', 'summon', 'banishment',

    # Entități & Arhetipuri
    'beast', 'hunter', 'prey', 'king', 'queen', 'child', 'man', 'woman', 'warrior',
    'mage', 'seer', 'prophet', 'ghost', 'angel', 'demon', 'titan', 'giant',
    'serpent', 'phoenix', 'dragon', 'spirit', 'avatar', 'reaper', 'oracle',

    # Tehnologie & Sci-Fi
    'machine', 'code', 'signal', 'data', 'program', 'algorithm', 'circuit', 'core',
    'grid', 'chip', 'node', 'network', 'system', 'matrix', 'virus', 'drone',
    'robot', 'android', 'sensor', 'scanner', 'module', 'device', 'battery',
    'engine', 'quantum', 'portal', 'field', 'hologram', 'interface',

    # Diverse / Poetic
    'glow', 'sparkle', 'shine', 'shade', 'silence', 'song', 'music', 'tone',
    'noise', 'chant', 'spell', 'illusion', 'dream', 'phantom', 'echo', 'pulse',
    'thread', 'web', 'nest', 'egg', 'wing', 'tail', 'scale', 'trail', 'sign',
    'omen', 'symbol'
]


class AdvancedWordBattleAI:
    def __init__(self):
        self.data = self.load_data()
        self.allowed_words = self.load_allowed_words()
        self.vocab, self.word_to_idx = self.preprocess_data()
        self.model = self.create_model()
        self.api_endpoint = "https://api.deepseek.com/v1/chat/completions"
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.cost_rank = {word: idx for idx, word in enumerate(self.allowed_words)}
        
    def load_data(self):
        if os.path.exists("battle_rules.csv"):
            return pd.read_csv("battle_rules.csv", header=None, names=['word1', 'word2'])
        return pd.DataFrame(columns=['word1', 'word2'])

    def load_allowed_words(self):
        return pd.read_csv("cuvinte.csv", header=None)[1].tolist()

    def preprocess_data(self):
        all_words = pd.concat([self.data['word1'], self.data['word2']]).tolist() + self.allowed_words + ENGLISH_WORDS
        return sorted(set(all_words)), {word: idx for idx, word in enumerate(sorted(set(all_words)))}

    def create_model(self):
        vocab_size = len(self.vocab)
        input_a = Input(shape=(1,))
        input_b = Input(shape=(1,))
        
        embedding = Embedding(vocab_size, 10)
        vec_a = Flatten()(embedding(input_a))
        vec_b = Flatten()(embedding(input_b))
        
        merged = Concatenate()([vec_a, vec_b])
        dense = Dense(32, activation='relu')(merged)
        output = Dense(1, activation='sigmoid')(dense)
        
        model = Model(inputs=[input_a, input_b], outputs=output)
        model.compile(optimizer=Adam(0.001), loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train_model(self):
        if not self.data.empty:
            X = [
                self.data['word1'].map(self.word_to_idx).values,
                self.data['word2'].map(self.word_to_idx).values
            ]
            self.model.fit(X, np.ones(len(self.data)), epochs=5, batch_size=64, verbose=0)

    def get_random_target(self):
        return random.choice(ENGLISH_WORDS)

    def get_suggestions(self, target_word):
        valid_candidates = [
            w for w in self.allowed_words 
            if w != target_word
            and (w, target_word) not in zip(self.data['word1'], self.data['word2'])
        ]
        
        if target_word not in self.word_to_idx:
            self.vocab.append(target_word)
            self.word_to_idx[target_word] = len(self.vocab) - 1
            self.model = self.create_model()
            self.train_model()

        if not valid_candidates:
            return []

        candidate_indices = [self.word_to_idx[w] for w in valid_candidates]
        target_idx = self.word_to_idx[target_word]
        
        predictions = self.model.predict(
            [np.array(candidate_indices), np.full(len(candidate_indices), target_idx)],
            verbose=0
        ).flatten()
        
        return sorted(zip(predictions, valid_candidates), key=lambda x: (-x[0], self.cost_rank[x[1]]))

    def query_api(self, suggestion, target):
        prompt = (
            f"Consider conceptual, abstract relationships. "
            f"Does '{suggestion}' logically counter or defeat '{target}'? "
            "Examples:\n"
            "- Water beats Fire\n"
            "- Shield beats Arrow\n"
            "- Time beats Aging\n"
            "Answer only 'da' or 'nu'."
        )
        
        try:
            response = requests.post(
                self.api_endpoint,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 2
                },
                timeout=15
            )
            return response.json()['choices'][0]['message']['content'].strip().lower()[:2]
        except Exception as e:
            print(f"API Error: {str(e)}")
            return 'nu'

    def process_target(self, target_word):
        print(f"\nTarget: {target_word}")
        suggestions = self.get_suggestions(target_word)
        
        for prob, candidate in suggestions:
            response = self.query_api(candidate, target_word)
            if response == 'da':
                self.add_rule(candidate, target_word)
                print(f"✅ Added: {candidate} beats {target_word}")
                return True
            print(f"❌ Rejected: {candidate} (confidence: {prob:.2f})")
        return False

    def add_rule(self, word1, word2):
        new_rule = pd.DataFrame([[word1, word2]], columns=['word1', 'word2'])
        new_rule.to_csv("battle_rules.csv", mode='a', header=False, index=False)
        self.data = pd.concat([self.data, new_rule], ignore_index=True)
        self.vocab, self.word_to_idx = self.preprocess_data()
        self.train_model()

    def run_requests(self, num_requests):
        for _ in range(num_requests):
            target = self.get_random_target()
            self.process_target(target)

if __name__ == "__main__":
    ai = AdvancedWordBattleAI()
    ai.train_model()
    
    try:
        num_requests = int(input("Enter number of random targets to process: "))
        ai.run_requests(num_requests)
    except ValueError:
        print("Invalid input")