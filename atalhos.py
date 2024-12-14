import os

def ativar():
    os.system(r'.venv\Scripts\activate.ps1')

def commit(mensagem):
    os.system(f'git commit -m "{mensagem}"')

if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1. Ativar ambiente")
    print("2. Commit no Git")
    escolha = input("Digite o número da opção: ")

    if escolha == "1":
        ativar()
    elif escolha == "2":
        msg = input("Digite a mensagem do commit: ")
        commit(msg)
    else:
        print("Opção inválida.")
