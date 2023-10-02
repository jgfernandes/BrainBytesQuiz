# Importa a classe DatabaseManager do arquivo database_manager.py e a renomeia como 'db'
from DatabaseManager import DatabaseManager

# Define a classe QuestionManager
class QuestionManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    
    def update_questions_in_database(self):
        # Define os valores padrão para os campos ausentes
        default_question_data = {
            'title': None,
            'text': None,
            'options': "A",
            'correct_answer': None,
            'difficulty': None,
            'category': None,
            'multiple_answers': False,
            'question_image': None,
            'feedback_image': None,
            'feedback_text': None,
            'active': True
        }

        # Inicializa uma variável para rastrear se alguma modificação foi feita
        modifications_made = False

        # Itera por todas as perguntas no banco de dados
        for question in self.db_manager.questions_table.all():
            question_data = question.copy()

            # Verifica cada campo no question_data e preenche com o valor padrão se estiver faltando
            for field, default_value in default_question_data.items():
                if field not in question_data:
                    question_data[field] = default_value
                    modifications_made = True  # Uma modificação foi feita

            # Atualiza a pergunta no banco de dados com os campos preenchidos, se alguma modificação foi feita
            if modifications_made:
                self.db_manager.questions_table.update(question_data, doc_ids=[question.doc_id])
                print(f"Pergunta ID {question.doc_id} atualizada com sucesso!")
            else:
                pass

        # Se nenhuma modificação foi feita em nenhuma pergunta, informa ao usuário
        if not modifications_made:
            print("Nenhuma modificação necessária. Todas as perguntas já possuem todos os campos.")

    def list_active_questions(self):
        # Método para listar todas as perguntas ativas no banco de dados
        print("Lista de Perguntas Ativas:")
        
        # Itera por todas as perguntas no banco de dados
        for question in self.db_manager.questions_table.all():
            if question.get('active', False):  # Verifica se a pergunta está ativa
                print("-" * 80)  # Linha de traços antes de cada pergunta
                print(f"ID: {question.doc_id}")
                for key, value in question.items():
                    print(f"{key}: {value}")
                print("-" * 80)  # Linha de traços após cada pergunta


    def get_yes_no_input(self, prompt):
        # Função para obter entrada 'Sim' ou 'Não' do usuário

        # Opções válidas
        valid_options = ['1', '2', 'sim', 'não', 'sim\n', 'não\n', 's', 'n']

        while True:
            # Exibe as opções formatadas
            formatted_options = "\n1. Sim\n2. Não\n"
            user_input = input(prompt + formatted_options).strip().lower()

            if user_input in valid_options:
                return user_input in ['1', 'sim', 'sim\n', 's']
            else:
                print("Opção inválida. Escolha '1' para Sim, '2' para Não, 's' para Sim ou 'n' para Não.")

    def get_options(self):
        # Função para obter as opções da pergunta
        options = []
        max_options = 5  # Defina o número máximo de opções desejado

        while len(options) < max_options:  # Continue enquanto o número de opções for menor que o máximo
            option = input(f"Alternativa {chr(65 + len(options))} (Deixe em branco para encerrar): ").strip()

            if not option:
                if len(options) < 2:
                    print("É necessário pelo menos duas opções.")  # Informa ao usuário que são necessárias pelo menos duas opções
                else:
                    break
            else:
                options.append(option)  # Adiciona a opção à lista de opções

        return options  # Retorna a lista de opções

    def get_correct_answers(self, options, multiple_answers):
        # Função para obter as respostas corretas
        correct_answers = []
        valid_options = ['1', '2', 'sim', 'não', 'sim\n', 'não\n']

        while True:
            correct_answer = self.get_correct_answer(options)  # Chama a função get_correct_answer para obter uma resposta correta

            # Verifica se a resposta já foi escolhida anteriormente
            if correct_answer in correct_answers:
                print("Essa resposta já foi escolhida anteriormente.")
                continue  # Pula para a próxima iteração do loop sem adicionar a resposta duplicada

            correct_answers.append(correct_answer)  # Adiciona a resposta correta à lista de respostas corretas

            if not multiple_answers:
                break

            another_answer = input("Deseja adicionar outra resposta correta? (1 - Sim / 2 - Não): ").strip().lower()

            if another_answer not in valid_options:
                print("Opção inválida. Escolha '1' para Sim ou '2' para Não.")
            elif another_answer in ['2', 'não', 'não\n']:
                break

        return correct_answers  # Retorna a lista de respostas corretas

    def get_correct_answer(self, options):
        # Função para obter a resposta correta enumerando as opções de A a E
        while True:
            print("Escolha a resposta correta:")
            for i, option in enumerate(options):
                print(f"{chr(65 + i)}. {option.strip()}")  # Apresenta as opções ao usuário

            correct_answer = input("Digite a letra correspondente à resposta correta: ").strip().upper()  # Solicita ao usuário que digite a letra correspondente à resposta correta

            if correct_answer.isalpha() and correct_answer in [chr(65 + i) for i in range(len(options))]:
                return ord(correct_answer) - ord('A') + 1  # Retorna o índice da opção correta
            else:
                print("Resposta correta inválida. Escolha uma letra correspondente às opções.")  # Imprime uma mensagem de erro

    def get_difficulty(self):
        while True:
            print("Escolha a dificuldade:")
            print("1. Fácil")
            print("2. Médio")
            print("3. Difícil")

            difficulty = input("Digite o número correspondente à dificuldade desejada: ")

            if difficulty in ['1', '2', '3']:
                return int(difficulty)
            else:
                print("Opção inválida. Escolha uma dificuldade válida.")

    def add_question(self):
        # Método para adicionar uma nova pergunta
        title = input("Título da pergunta: ")
        text = input("Texto da pergunta: ")
        options = self.get_options()
        multiple_answers = self.get_yes_no_input("Permite múltiplas respostas? (Sim/Não): ")
        correct_answers = self.get_correct_answers(options, multiple_answers)
        difficulty = self.get_difficulty()
        category = input("Categoria: ")
        question_image = input("URL da imagem da pergunta (opcional): ")
        feedback_image = input("URL da imagem do feedback (opcional): ")
        feedback_text = input("Feedback por escrito (opcional): ")

        question_data = {
            'title': title,
            'text': text,
            'options': options,
            'correct_answer': correct_answers,
            'difficulty': difficulty,
            'category': category,
            'multiple_answers': multiple_answers,
            'question_image': question_image,
            'feedback_image': feedback_image,
            'feedback_text': feedback_text,
            'active': True  # Certifica-se de que a pergunta seja criada como ativa
        }

        # Acessa a tabela de perguntas através do db_manager e insere os dados da pergunta
        self.db_manager.questions_table.insert(question_data)
        print("Pergunta adicionada com sucesso!")

    def edit_question(self):
        # Método para editar uma pergunta existente
        question_id = input("Digite o ID da pergunta que deseja editar: ")

        if not question_id.isdigit():
            print("ID de pergunta inválido. Deve ser um número.")
            return

        question_id = int(question_id)

        if self.db_manager.questions_table.contains(doc_id=question_id):
            # Obtém a pergunta atual a partir do banco de dados
            current_question = self.db_manager.questions_table.get(doc_id=question_id)
            new_data = {}

            # Exibe os valores atuais da pergunta
            print("\nValores atuais:")
            print(f"Título: {current_question['title']}")
            print(f"Texto: {current_question['text']}")
            for i, option in enumerate(current_question['options']):
                print(f"Alternativa {chr(65 + i)}: {option}")
            print(f"Permite múltiplas respostas? {'Sim' if current_question['multiple_answers'] else 'Não'}")
            print(f"Dificuldade: {current_question['difficulty']}")
            print(f"Categoria: {current_question['category']}")

            # Início da edição dos dados da pergunta
            print("\nDeixe em branco para manter os valores atuais.")

            # Solicita a edição do título da pergunta
            new_data['title'] = input(f"Novo Título ({current_question['title']}): ") or current_question['title']

            # Solicita a edição do texto da pergunta
            new_data['text'] = input(f"Novo Texto ({current_question['text']}): ") or current_question['text']

            # Solicita novas opções de resposta uma por uma
            new_options = []

            for i in range(5):
                current_option = current_question['options'][i] if i < len(current_question['options']) else ""
                option = input(f"Nova Alternativa {chr(65 + i)} ({current_option}): ").strip()

                if not option and i >= 2:
                    # Se deixou em branco e já tem pelo menos duas respostas, encerra
                    break

                new_options.append(option)

            # Continua perguntando até incluir pelo menos duas respostas ou até chegar à alternativa E
            while len(new_options) < 2 and len(new_options) < 5:
                option = input(f"Nova Alternativa {chr(65 + len(new_options))} (Deixe em branco para encerrar): ").strip()

                if not option:
                    break

                new_options.append(option)

            new_data['options'] = new_options

            # Solicita se a pergunta permite múltiplas respostas
            multiple_answers = self.get_yes_no_input("Permite múltiplas respostas? (Sim/Não): ")

            # Verifica se o campo de resposta correta foi deixado em branco
            if not current_question.get('correct_answers') or not any(current_question['correct_answers']):
                correct_answers = self.get_correct_answers(new_data['options'])
            else:
                correct_answers = current_question['correct_answers']

            # Define a resposta correta
            new_data['correct_answers'] = correct_answers

            # Solicita a edição da dificuldade
            new_data['difficulty'] = self.get_difficulty() or current_question['difficulty']

            # Solicita a edição da categoria
            new_data['category'] = input(f"Nova Categoria ({current_question['category']}): ") or current_question['category']

            # Define se a pergunta permite múltiplas respostas
            new_data['multiple_answers'] = multiple_answers

            # Solicita a edição da URL da imagem da pergunta
            new_data['question_image'] = input(f"Nova URL da Imagem da Pergunta ({current_question['question_image']}): ") or current_question['question_image']

            # Solicita a edição da URL da imagem do feedback
            new_data['feedback_image'] = input(f"Nova URL da Imagem do Feedback ({current_question['feedback_image']}): ") or current_question['feedback_image']

            # Solicita a edição do texto do feedback
            new_data['feedback_text'] = input(f"Insira o novo texto do Feedback ({current_question['feedback_text']}): ") or current_question['feedback_text']

            # Atualiza a pergunta no banco de dados
            self.db_manager.questions_table.update(new_data, doc_ids=[question_id])
            print("Pergunta atualizada com sucesso!")
        else:
            print("ID de pergunta não encontrado no banco de dados.")

    def list_questions(self):
        # Método para listar todas as perguntas no banco de dados
        print("Lista de Perguntas:")
        for question in self.db_manager.questions_table.all():
            print("-" * 80)  # Linha de traços antes de cada pergunta
            print(f"ID: {question.doc_id}")
            for key, value in question.items():
                print(f"{key}: {value}")
            print("-" * 80)  # Linha de traços após cada pergunta

    def delete_question(self):
        # Método para excluir uma pergunta existente
        question_id = input("Digite o ID da pergunta que deseja excluir: ")

        if not question_id.isdigit():
            print("ID de pergunta inválido. Deve ser um número.")
            return

        question_id = int(question_id)

        if self.db_manager.questions_table.contains(doc_id=question_id):
            # Define o estado da pergunta como excluída (em vez de removê-la permanentemente)
            self.db_manager.questions_table.update({'active': False}, doc_ids=[question_id])
            print("Pergunta marcada como excluída.")
        else:
            print("ID de pergunta não encontrado no banco de dados.")




    def run(self):
        while True:
            print("\n--- Menu ---")
            print("1. Adicionar Pergunta")
            print("2. Listar Perguntas Ativas")
            print("3. Listar Todas as Perguntas")
            print("4. Editar Pergunta")
            print("5. Excluir Pergunta")
            print("6. Adequar Banco de Dados")
            print("7. Sair")
            choice = input("Escolha uma opção: ")

            if choice == '1':
                self.add_question()
            elif choice == '2':
                self.list_active_questions()
            elif choice == '3':
                self.list_questions()
            elif choice == '4':
                self.edit_question()
            elif choice == '5':
                self.delete_question()
            elif choice == '6':
                self.update_questions_in_database()
                print("Banco de Dados Adequado com Sucesso!")
            elif choice == '7':
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    db_manager = DatabaseManager()
    manager = QuestionManager(db_manager)
    manager.run()
