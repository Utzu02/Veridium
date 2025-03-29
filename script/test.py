import numpy as np
import spacy
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

class MLWordBattleAI:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.player_words = {
            # Lista completă cu 60+ cuvinte și costurile lor
            "Feather": 1, "Coal": 1, "Pebble": 1, "Leaf": 2, "Paper": 2,
            "Rock": 2, "Water": 3, "Twig": 3, "Sword": 4, "Shield": 4,
            "Gun": 5, "Flame": 5, "Rope": 5, "Disease": 6, "Cure": 6,
            "Bacteria": 6, "Shadow": 7, "Light": 7, "Virus": 7, "Sound": 8,
            "Time": 8, "Fate": 8, "Earthquake": 9, "Storm": 9, "Vaccine": 9,
            "Logic": 10, "Gravity": 10, "Robots": 10, "Stone": 11, "Echo": 11,
            "Thunder": 12, "Karma": 12, "Wind": 13, "Ice": 13, "Sandstorm": 13,
            "Laser": 14, "Magma": 14, "Peace": 14, "Explosion": 15, "War": 15,
            "Enlightenment": 15, "Nuclear Bomb": 16, "Volcano": 16, "Whale": 17,
            "Earth": 17, "Moon": 17, "Star": 18, "Tsunami": 18, "Supernova": 19,
            "Antimatter": 19, "Plague": 20, "Rebirth": 20, "Tectonic Shift": 21,
            "Gamma-Ray Burst": 22, "Human Spirit": 23, "Apocalyptic Meteor": 24,
            "Earth's Core": 25, "Neutron Star": 26, "Supermassive Black Hole": 35,
            "Entropy": 45
        }

        self._prepare_training_data()
        self._build_model()

    def _prepare_training_data(self):
        training_examples = {
            # === Natural Elements ===
            "dust": "Water", "avalanche": "Flame", "drought": "Storm", "mudslide": "Earthquake",
            "sunlight": "Shadow", "blizzard": "Flame", "cyclone": "Earth", "heatwave": "Ice",

            # === Creatures ===
            "werewolf": "Light", "manticore": "Sword", "kraken": "Whale", "basilisk": "Light",
            "golem": "Logic", "griffin": "Gun", "ghost": "Light", "minotaur": "Sword",
            "plague doctor": "Vaccine", "swarm": "Sound",

            # === Technology ===
            "android": "Virus", "AI": "Logic", "mech": "Gravity", "supercomputer": "Entropy",
            "stealth jet": "Thunder", "autoturret": "Shadow", "hologram": "Light",
            "nanobots": "Flame",  # <- schimbat din "Heat" în ceva existent
            "satellite": "Laser",

            # === Abstract Concepts ===
            "nightmare": "Human Spirit", "ignorance": "Enlightenment", "madness": "Logic",
            "tyranny": "Rebirth", "futility": "Fate", "paradox": "Time", "illusion": "Light",
            "destruction": "Peace", "doom": "Enlightenment", "revenge": "Karma",

            # === Cosmic Phenomena ===
            "nebula storm": "Gravity", "cosmic radiation": "Shield", "dark matter": "Logic",
            "void": "Entropy", "stellar collapse": "Supernova", "galactic war": "Enlightenment",
            "black comet": "Earth's Core", "universal tear": "Supermassive Black Hole",
        }

        # 🔥 Păstrează doar exemplele ale căror valori (countere) există în player_words
        valid_training_examples = {
            k: v for k, v in training_examples.items() if v in self.player_words
        }

        self.X_train = np.array([self.nlp(word).vector for word in valid_training_examples.keys()])
        self.y_train = list(valid_training_examples.values())

        self.le = LabelEncoder()
        self.le.fit(list(self.player_words.keys()))

    def _build_model(self):
        self.model = Sequential([
            Dense(128, activation='relu', input_shape=(self.X_train.shape[1],)),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dense(len(self.player_words), activation='softmax')
        ])

        self.model.compile(
            loss='sparse_categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

        y_encoded = self.le.transform(self.y_train)
        self.model.fit(self.X_train, y_encoded, epochs=50, batch_size=16)

    def predict_counter(self, user_word: str) -> tuple[str, int]:
        vector = np.array([self.nlp(user_word).vector])
        predictions = self.model.predict(vector, verbose=0)[0]
        top_indices = np.argsort(predictions)[-3:][::-1]
        top_counters = self.le.inverse_transform(top_indices)

        for counter in top_counters:
            if counter in self.player_words:
                return counter, self.player_words[counter]

        return min(self.player_words.items(), key=lambda x: x[1])

    def explain_prediction(self, user_word: str, counter: str) -> str:
        similarity = self.nlp(user_word).similarity(self.nlp(counter))
        return f"AI a ales '{counter}' (similaritate: {similarity:.2f}) bazat pe modelul antrenat"

if __name__ == "__main__":
    ai = MLWordBattleAI()

    while True:
        user_word = input("\nEnter system word (type 'exit' to quit): ").strip()
        if user_word.lower() == 'exit':
            break

        counter, cost = ai.predict_counter(user_word)
        explanation = ai.explain_prediction(user_word, counter)

        print(f"\nSystem word: {user_word}")
        print(f"Counter chosen: {counter} (${cost})")
        print(f"Explanation: {explanation}")
