# 1 QuizGame.py

from DatabaseManager import DatabaseManager
from QuizManager import QuizManager
from QuestionManager import QuestionManager

class QuizGame:
    def __init__(self, db_manager, quiz_manager, question_manager):
        self.db_manager = db_manager
        self.quiz_manager = quiz_manager
        self.question_manager = question_manager
        self.player_name = None  # Adicionamos um atributo para armazenar o nome do jogador

    def list_quizzes(self):
        """
        Lista todos os quizzes disponíveis no banco de dados.
        """
        quizzes = self.db_manager.list_quizzes()
        if quizzes:
            print("\n--- Quizzes Disponíveis ---")
            for quiz in quizzes:
                print(f"ID: {quiz.doc_id}, Nome: {quiz['nome']}, Descrição: {quiz['descricao']}, Quantidade de Perguntas: {quiz['quantidade_de_perguntas']}")
        else:
            print("Nenhum quiz encontrado.")

    def play_quiz(self, quiz_id):
        """
        Inicia o jogo para um quiz específico.
        """
        if not self.db_manager.quizzes_table.contains(doc_id=quiz_id):
            print("Quiz não encontrado.")
            return

        quiz_data = self.db_manager.quizzes_table.get(doc_id=quiz_id)
        print(f"Jogando o Quiz: {quiz_data['nome']}")

        if not self.player_name:
            self.player_name = input("Digite seu nome: ")

        questions = quiz_data.get('perguntas', [])

        if not questions:
            print("Este quiz não tem perguntas associadas.")
            return

        score = 0
        total_questions = len(questions)
        answers_summary = []  # Lista para armazenar respostas e feedbacks

        for question_id in questions:
            if not self.db_manager.questions_table.contains(doc_id=question_id):
                print(f"Pergunta ID {question_id} não encontrada.")
                continue

            question_data = self.db_manager.questions_table.get(doc_id=question_id)
            print("\nPergunta:")
            print(f"Título: {question_data['title']}")
            print(f"Texto: {question_data['text']}")
            options = question_data['options']
            correct_answers = question_data['correct_answer']

            for i, option in enumerate(options):
                print(f"{chr(65 + i)}. {option}")

            user_answer = input("Escolha a letra ou número correspondente à resposta correta: ").strip().upper()

            while user_answer not in ['A', 'B', 'C', 'D', 'E', '1', '2', '3', '4', '5']:
                print("Opção inválida. Por favor, escolha uma das letras ou números disponíveis.")
                user_answer = input("Escolha a letra ou número correspondente à resposta correta: ").strip().upper()

            if user_answer.isnumeric():
                user_answer_index = int(user_answer)
                user_answer = chr(64 + user_answer_index)

            user_answer_index = ord(user_answer) - ord('A') + 1
            is_correct = user_answer_index in correct_answers
            answers_summary.append({
                'Título da Questão': question_data['title'],
                'Resposta Correta': [chr(64 + ans) for ans in correct_answers],
                'Resposta Fornecida': user_answer,
            })

            if is_correct:
                score += 1

        print(f"\nResumo das Respostas:")
        for index, answer_summary in enumerate(answers_summary, 1):
            print(f"Pergunta {index}:")
            for key, value in answer_summary.items():
                print(f"{key}: {value}")
            print()

        print(f"\n{self.player_name}, você respondeu corretamente a {score} de {total_questions} perguntas.")

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
    question_manager = QuestionManager(db_manager)
    game = QuizGame(db_manager, quiz_manager, question_manager)
    game.run()
