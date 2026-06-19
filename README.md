# algoritmo-e-programa-o2
import os

# Lista que vai armazenar as tarefas
tarefas = []

def mostrar_menu():
    print("\n=== GERENCIADOR DE TAREFAS ===")
    print("1. Adicionar Tarefa")
    print("2. Listar Tarefas")
    print("3. Remover Tarefa")
    print("4. Sair")
    print("==============================")

def adicionar_tarefa():
    tarefa = input("Digite o nome da tarefa: ")
    if tarefa.strip():
        tarefas.append(tarefa)
        print(f"Tarefa '{tarefa}' adicionada com sucesso!")
    else:
        print("A tarefa não pode estar vazia.")

def listar_tarefas():
    if not tarefas:
        print("Sua lista de tarefas está vazia.")
    else:
        print("\n--- Suas Tarefas ---")
        for index, tarefa in enumerate(tarefas, start=1):
            print(f"{index}. {tarefa}")

def remover_tarefa():
    listar_tarefas()
    if tarefas:
        try:
            indice = int(input("\nDigite o número da tarefa que deseja remover: "))
            if 1 <= indice <= len(tarefas):
                removida = tarefas.pop(indice - 1)
                print(f"Tarefa '{removida}' removida!")
            else:
                print("Número inválido.")
        except ValueError:
            print("Por favor, digite um número válido.")

# Loop principal do programa
while True:
    mostrar_menu()
    opcao = input("Escolha uma opção (1-4): ")

    if opcao == "1":
        adicionar_tarefa()
    elif opcao == "2":
        listar_tarefas()
    elif opcao == "3":
        remover_tarefa()
    elif opcao == "4":
        print("Saindo do programa. Até mais!")
        break
    else:
        print("Opção inválida! Tente novamente.")
