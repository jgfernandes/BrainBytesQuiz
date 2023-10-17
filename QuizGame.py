from DatabaseManager import DatabaseManager
from QuizManager import QuizManager
from QuestionManager import QuestionManager

class QuizGame:
    def __init__(self, db_manager, quiz_manager, question_manager):
        self.db_manager = db_manager
        self.quiz_manager = quiz_manager
        self.question_manager = question_manager

    def list_quizzes(self):
        quizzes = self.db_manager.list_quizzes()
        if quizzes:
            print("\n--- Quizzes Disponíveis ---")
            for quiz in quizzes:
                print(f"ID: {quiz.doc_id}, Nome: {quiz['nome']}, Descrição: {quiz['descricao']}, Quantidade de Perguntas: {quiz['quantidade_de_perguntas']}")
        else:
            print("Nenhum quiz encontrado.")

    def play_quiz(self, quiz_id):
        if not self.db_manager.quizzes_table.contains(doc_id=quiz_id):
            print("Quiz não encontrado.")
            return

        quiz_data = self.db_manager.quizzes_table.get(doc_id=quiz_id)
        print(f"Jogando o Quiz: {quiz_data['nome']}")
        questions = quiz_data.get('perguntas', [])  # Obtenha a lista de perguntas associadas a este quiz

        if not questions:
            print("Este quiz não tem perguntas associadas.")
            return

        score = 0
        for question_id in questions:
            if not self.db_manager.questions_table.contains(doc_id=question_id):
                print(f"Pergunta ID {question_id} não encontrada.")
                continue

            question_data = self.db_manager.questions_table.get(doc_id=question_id)
            print("\nPergunta:")
            print(f"Título: {question_data['title']}")
            print(f"Texto: {question_data['text']}")
            options = question_data['options']
            for i, option in enumerate(options):
                print(f"{chr(65 + i)}. {option}")

            user_answer = input("Escolha a letra correspondente à resposta correta: ").strip().upper()

            if user_answer.isalpha() and user_answer in [chr(65 + i) for i in range(len(options))]:
                user_answer_index = ord(user_answer) - ord('A') + 1
                correct_answers = question_data['correct_answer']
                if user_answer_index in correct_answers:
                    print("Resposta correta!")
                    score += 1
                else:
                    print("Resposta incorreta.")
            else:
                print("Opção inválida. Você perdeu esta pergunta.")

        print(f"Você respondeu corretamente a {score} de {len(questions)} perguntas.")


    def manage_questions(self):
        self.question_manager.run()

    def manage_quizzes(self):
        self.quiz_manager.run()

    def run(self):
        while True:
            print("\n--- Menu do Jogo Quiz ---")
            print("1. Listar Quizzes Disponíveis")
            print("2. Jogar um Quiz")
            print("3. Gerenciar Perguntas")
            print("4. Gerenciar Quizzes")
            print("5. Sair")
            choice = input("Escolha uma opção: ")

            if choice == '1':
                self.list_quizzes()
            elif choice == '2':
                quiz_id = int(input("Digite o ID do quiz que deseja jogar: "))
                self.play_quiz(quiz_id)
            elif choice == '3':
                self.manage_questions()
            elif choice == '4':
                self.manage_quizzes()
            elif choice == '5':
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    db_manager = DatabaseManager()
    quiz_manager = QuizManager(db_manager)
    question_manager = QuestionManager(db_manager)  # Passa o mesmo db_manager para QuestionManager
    game = QuizGame(db_manager, quiz_manager, question_manager)
    game.run()

