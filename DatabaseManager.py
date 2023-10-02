from tinydb import TinyDB

class DatabaseManager:
    def __init__(self, db_file='quiz_db.json'):
        self.db = TinyDB(db_file)
        self.questions_table = self.db.table('questions_db')
        self.quizzes_table = self.db.table('quizzes')

    # Funções relacionadas a perguntas
    def add_question(self, question_data):
        self.questions_table.insert(question_data)

    def list_questions(self):
        return self.questions_table.all()

    def edit_question(self, question_id, new_data):
        self.questions_table.update(new_data, doc_ids=[question_id])

    def delete_question(self, question_id):
        self.questions_table.remove(doc_ids=[question_id])

    # Funções relacionadas a quizzes
    def add_quiz(self, quiz_data):
        self.quizzes_table.insert(quiz_data)

    def list_quizzes(self):
        return self.quizzes_table.all()

    def edit_quiz(self, quiz_id, new_data):
        self.quizzes_table.update(new_data, doc_ids=[quiz_id])

    def delete_quiz(self, quiz_id):
        self.quizzes_table.remove(doc_ids=[quiz_id])
