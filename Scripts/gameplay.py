import json
import random

class GameplayLoop():


    flashCardFilePath = None
    selected_cards = set()

    showed_answer = False
    deck_size_total = None
    current_card_iteration = 0
    completed_deck = False
    current_card_question_text = None
    current_card_image = None
    current_card_answer = None
    correct_answers = 0

    def __init__(self):
        pass

    def reset_values(self):
        flashCardFilePath = None
        selected_cards = set()

        showed_answer = False
        deck_size_total = None
        current_card_iteration = 0
        completed_deck = False
        current_card_question_text = None
        current_card_image = None
        current_card_answer = None
        correct_answers = 0
        pass


    def read_flashcard(self):
        with open(self.flashCardFilePath, 'r') as json_file:
            data = json.load(json_file)
        
        self.loaded_flashcards = data.get("cards", [])
        self.deck_size_total = len(self.loaded_flashcards)

    def get_unique_card(self):
        while True:
            selected_card = random.choice(self.loaded_flashcards)
            selected_card_tuple = tuple(selected_card)
            if selected_card_tuple not in self.selected_cards:
                self.selected_cards.add(selected_card_tuple)
                return selected_card

            
    def get_card(self):
        retrieved_card = self.get_unique_card()
        self.current_card_question_text, self.current_card_image, self.current_card_answer = retrieved_card
