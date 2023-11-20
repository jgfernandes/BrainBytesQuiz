# 3 QuizManager.py

from DatabaseManager import DatabaseManager

class QuizManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_quiz(self):
        existing_question_ids = []  # Armazena IDs de perguntas já incluídas em quizzes
        nome = input("Nome do Quiz: ")
        descricao = input("Descrição: ")
        while True:
            try:
                num_perguntas = int(input("Quantidade de Perguntas: "))
                break  # Se a conversão for bem-sucedida, saia do loop
            except ValueError:
                print("Erro: Por favor, digite apenas números.")

        perguntas = []
        for _ in range(num_perguntas):
            pergunta_id = int(input("ID da Pergunta: "))
            perguntas.append(pergunta_id)

        quiz_data = {
            'nome': nome,
            'descricao': descricao,
            'quantidade_de_perguntas': num_perguntas,
            'perguntas': perguntas
        }

        self.db_manager.add_quiz(quiz_data)
        print("Quiz criado com sucesso!")
    
        novo_quiz_id = "a"
        return novo_quiz_id

    def view_quiz(self, quiz_id):
        if not self.db_manager.quizzes_table.contains(doc_id=quiz_id):
            print("Quiz não encontrado.")
            return

        quiz_data = self.db_manager.quizzes_table.get(doc_id=quiz_id)
        print(f"Visualizando o Quiz: {quiz_data['nome']}")
        questions = quiz_data.get('perguntas', [])

        if not questions:
            print("Este quiz não tem perguntas associadas.")
        else:
            print("--- Perguntas ---")
            for question_id in questions:
                question_data = self.db_manager.questions_table.get(doc_id=question_id)
                if question_data:
                    print(f"Pergunta ID: {question_id}")
                    print(f"Título: {question_data.get('title', 'N/A')}")
                    print(f"Texto: {question_data.get('text', 'N/A')}")
                    options = question_data.get('options', [])
                    for i, option in enumerate(options):
                        print(f"{chr(65 + i)}. {option}")
                else:
                    print(f"Pergunta ID {question_id} não encontrada.")
    


    def list_quizzes(self):
        quizzes = self.db_manager.list_quizzes()
        if quizzes:
            print("\n--- Quizzes Disponíveis ---")
            for quiz in quizzes:
                print(f"ID: {quiz.doc_id}, Nome: {quiz['nome']}, Descrição: {quiz['descricao']}, Quantidade de Perguntas: {quiz['quantidade_de_perguntas']}")
                if 'perguntas' in quiz:
                    print(f"Perguntas: {', '.join(map(str, quiz['perguntas']))}")
        else:
            print("Nenhum quiz encontrado.")

    def edit_quiz(self, quiz_id):
        if not self.db_manager.quizzes_table.contains(doc_id=quiz_id):
            print("Quiz não encontrado.")
            return

        quiz_data = self.db_manager.quizzes_table.get(doc_id=quiz_id)
        print(f"Editando o Quiz: {quiz_data['nome']}")
        
        nome = input(f"Novo nome ({quiz_data['nome']}): ")
        descricao = input(f"Nova descrição ({quiz_data['descricao']}): ")
        num_perguntas = int(input(f"Nova quantidade de perguntas ({quiz_data['quantidade_de_perguntas']}): "))

        perguntas = []
        for _ in range(num_perguntas):
            pergunta_id = int(input("ID da Pergunta: "))
            perguntas.append(pergunta_id)

        updated_data = {
            'nome': nome or quiz_data['nome'],
            'descricao': descricao or quiz_data['descricao'],
            'quantidade_de_perguntas': num_perguntas,
            'perguntas': perguntas
        }

        self.db_manager.edit_quiz(quiz_id, updated_data)
        print(f"Quiz ID {quiz_id} editado com sucesso!")

    def delete_quiz(self, quiz_id):
        if not self.db_manager.quizzes_table.contains(doc_id=quiz_id):
            print("Quiz não encontrado.")
            return

        confirm = input(f"Tem certeza que deseja excluir o Quiz ID {quiz_id}? (Sim/Não): ").strip().lower()
        if confirm in ['sim', 's']:
            self.db_manager.delete_quiz(quiz_id)
            print(f"Quiz ID {quiz_id} excluído com sucesso!")

    def run(self):
        while True:
            print("\n--- Menu Quiz ---")
            print("1. Criar Quiz")
            print("2. Listar Quizzes")
            print("3. Visualizar Quiz")
            print("4. Editar Quiz")
            print("5. Excluir Quiz")
            print("6. Sair")
            choice = input("Escolha uma opção: ")

            if choice == '1':
                self.create_quiz()
            elif choice == '2':
                self.list_quizzes()
            elif choice == '3':
                quiz_id = int(input("Digite o ID do quiz que deseja visualizar: "))
                self.view_quiz(quiz_id)
            elif choice == '4':
                quiz_id = int(input("Digite o ID do quiz que deseja editar: "))
                self.edit_quiz(quiz_id)
            elif choice == '5':
                quiz_id = int(input("Digite o ID do quiz que deseja excluir: "))
                self.delete_quiz(quiz_id)
            elif choice == '6':
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")



if __name__ == "__main__":
    db_manager = DatabaseManager()
    manager = QuizManager(db_manager)
    manager.run()
