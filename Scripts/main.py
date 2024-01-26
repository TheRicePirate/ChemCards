import os
import sys
import molecule_generator
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QDialog, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from set_creator import SetCreator
from flashcardui import Ui_MainWindow  # Replace 'MainWindow_ui' with the actual name of your generated UI file
from gameplay import GameplayLoop


class CustomMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.has_started_game = False
        self.created_new_question = False
        self.has_clicked_submit = False
        # Set up the UI from the generated file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.setupUi(self)
        self.setStyleSheet("background-color: blue;")
        self.autoFillBackground()
        # Set fixed height
        self.setFixedHeight(500)  # Change the value to your desired fixed height
        self.ui.goToSetupButton.clicked.connect(self.go_to_setup)
        self.ui.returnToMainButton.clicked.connect(self.go_to_main)
        self.ui.loadSetButton.clicked.connect(self.browse_files)
        self.ui.showAnswerButton.clicked.connect(self.show_answer_clicked)
        self.ui.generateMoleculeButton.clicked.connect(self.generate_molecule_clicked)
        self.ui.createNewQuestionButton.clicked.connect(self.save_question_clicked)
        self.ui.submitAnswerButton.setEnabled = False


    def keyPressEvent(self, event):
        # Event key for the enter key
        if (event.key() == 16777220) and (gameManager.completed_deck == False) and (self.has_started_game == True):
            self.submit_answer_clicked()


    def submit_answer_clicked(self):
        if (self.has_clicked_submit == False) and (self.has_started_game == True) and (gameManager.completed_deck == False):
            if (gameManager.completed_deck == False):
                user_answer = self.ui.userAnswerField.text()
                if (user_answer == gameManager.current_card_answer) and (gameManager.showed_answer == False):
                    gameManager.correct_answers += 1
                    self.ui.correctOrIncorrectText.setStyleSheet('background-color: green;')
                    self.ui.correctOrIncorrectText.setText("Correct!")
                else:
                    self.ui.correctOrIncorrectText.setStyleSheet('background-color: red;')
                    self.ui.correctOrIncorrectText.setText("Incorrect")

            self.ui.submitAnswerButton.setText("Next")
            self.has_clicked_submit = True

        else:
            self.ui.correctOrIncorrectText.setStyleSheet(None)
            self.ui.submitAnswerButton.setText("Submit")
            self.has_clicked_submit = False
            self.ui.correctOrIncorrectText.setText("")
            gameManager.current_card_iteration += 1
            gameManager.showed_answer = False

            if (gameManager.current_card_iteration == gameManager.deck_size_total):
                self.ui.correctOrIncorrectText.setText(f"You scored: {gameManager.correct_answers}/{gameManager.deck_size_total} or {int((gameManager.correct_answers / gameManager.deck_size_total) * 100)}%")
                self.ui.submitAnswerButton.setDisabled(True)
                gameManager.completed_deck = True
            else:
                self.next_question_ui()

            self.ui.userAnswerField.setText("")

    def reset_game_ui(self):
        self.ui.correctOrIncorrectText.setStyleSheet(None)
        self.ui.correctOrIncorrectText.clear()
        self.ui.submitAnswerButton.text = "Submit"
        self.ui.questionText.clear()
        self.ui.userAnswerField.clear()
        self.ui.gamePlayMolecule.clear()

    def show_answer_clicked(self):
        if (self.has_started_game):
            gameManager.showed_answer = True
            self.ui.userAnswerField.setText(gameManager.current_card_answer)

    def reset_clicked(self):
        self.restart_app()

    def next_question_ui(self):
        gameManager.get_card()
        self.ui.questionText.setText(f"{gameManager.current_card_question_text}")

        smile_string = gameManager.current_card_image
        image_path = molecule_generator.generate_2d_diagram(smile_string)
        if image_path != False:
            pixmap = QPixmap(image_path)
            self.ui.gamePlayMolecule.setPixmap(pixmap)

        self.created_new_question = True

    def go_to_setup(self):
        if (self.has_started_game):
            self.restart_app()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName()
        setcreator.create_json_file(filename)
        self.ui.stackedWidget.setCurrentIndex(1)

    def go_to_main(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        if (self.created_new_question == False):
            setcreator.add_question(self.ui.userQuestionName.text(), self.ui.smilesField.text(), self.ui.userQuestionAnswer.text())
        setcreator.save_set()
        setcreator.data["cards"] = []
        self.ui.userQuestionName.clear()
        self.ui.smilesField.clear()
        self.ui.userQuestionAnswer.clear()
        self.ui.moleculeImage.clear()

    def browse_files(self):
        if (self.has_started_game == True):
            self.restart_app()
        else:
            self.ui.submitAnswerButton.clicked.connect(self.submit_answer_clicked)
            selected_file, _ = QFileDialog.getOpenFileName(self, 'Open file', 'User Card Sets', 'JSON (*.json)')
            if selected_file:
                self.has_started_game = True
                file_name = os.path.basename(selected_file)
                print("Selected file name:", file_name)
                gameManager.flashCardFilePath = selected_file
                gameManager.read_flashcard()
                self.next_question_ui()
                self.ui.submitAnswerButton.setEnabled = True

            else:
                print("No file selected")
                gameManager.flashCardFilePath = None


    def restart_app(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)

    def generate_molecule_clicked(self):
        smile_string = self.ui.smilesField.text()
        image_path = molecule_generator.generate_2d_diagram(smile_string)
        if image_path != False:
            pixmap = QPixmap(image_path)
            self.ui.moleculeImage.setPixmap(pixmap)

        else:
            print("invalid string")


    def save_question_clicked(self):
        setcreator.add_question(self.ui.userQuestionName.text(), self.ui.smilesField.text(), self.ui.userQuestionAnswer.text())
        self.ui.userQuestionName.clear()
        self.ui.smilesField.clear()
        self.ui.userQuestionAnswer.clear()
        self.ui.moleculeImage.clear()
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = CustomMainWindow()
    MainWindow.show()
    gameManager = GameplayLoop()
    setcreator = SetCreator()
    sys.exit(app.exec())