import json



class SetCreator():

    card_set_file_path = None
    data = {
        "cards": []
    }

    def __init__(self):
        pass

    def create_json_file(self, file_path):
        self.card_set_file_path = file_path + '.json'
        with open(file_path + ".json", 'w') as json_file:
            json.dump({}, json_file, indent=2)     

    def add_question(self, question_name, image_path, answer):
        new_question = (question_name, image_path, answer)
        self.data["cards"].append(new_question)

    def save_set(self):
        with open(self.card_set_file_path, 'w') as json_file:
            json.dump(self.data, json_file, indent=2)

