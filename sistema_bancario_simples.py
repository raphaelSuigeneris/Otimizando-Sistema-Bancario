import textwrap

def menu():
    menu = """\n
    \tDigite a ação que você deseja realizar

[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[c]\tCriar conta
[u]\tCriar usuário
[l]\tListar contas
[q]\tSair
=> """
    return input(textwrap.dedent(menu))

def sacar(*, extrato, limite_saques):
    try:
        valor_saque = float(input("Digite o valor a ser sacado: "))
        if extrato["numero_saques"] >= limite_saques:
            print("Você já executou o limite diário de saques, tente novamente amanhã.")
        elif valor_saque > extrato["saldo"]:
            print("Saldo insuficiente!")
        elif valor_saque < 0 or valor_saque > extrato["limite"]:
            print("O valor informado está fora dos limites!")
        else:
            extrato["saldo"] -= valor_saque
            extrato["numero_saques"] += 1
            extrato["operacao"].append([f"Saque realizado: R${valor_saque:.2f}"])
            print (f"Você sacou R${valor_saque:.2f}.")
    except:
        print("O valor informado é inválido!")

def depositar(extrato, /):
    try:
        valor_deposito = float(input("Digite o valor para depósito: "))
        if valor_deposito > 0:
            extrato["saldo"] += valor_deposito
            extrato["operacao"].append([f"Depósito realizado: R${valor_deposito:.2f}"])
            print (f"Você depositou R${valor_deposito:.2f}")
        else:
            print("O valor informado é inválido!")
    except:
        print("O valor informado é inválido!")

def exibir_extrato(saldo, /, *, operacao):
        print("\n============== EXTRATO ==============")
        for i in range (len(operacao)):
            print(operacao[i][0])
        print(f"\nSeu saldo atual é de R${saldo:.2f}")
        print("=====================================")
    
def criar_usuario(usuarios):
    usuario = {"nome": "", "data": "", "cpf": "", "endereco": "", "contas": []}

    usuario["nome"] = input("Digite seu nome: ")
    usuario["data"] = input("Digite sua data de nascimento (dd/mm/aaaa): ")
    usuario["cpf"] = int(input("Digite seu CPF (apenas números): "))
    usuario["endereco"] = input("Digite seu endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    if filtro(usuario["cpf"], usuarios):
        print("Esse CPF já existe")
    else:
        print("Usuario criado com sucesso!")
    usuarios.append(usuario)
    return usuarios

def criar_conta(contas_existentes, usuarios):
    nova_conta = {"agencia": "0001", "numero": 0}

    nova_conta["numero"] = len(contas_existentes) + 1
    vinculo = int(input("Digite seu CPF (apenas números): "))

    if filtro(vinculo, usuarios):
        contas_existentes.append(nova_conta)
        for i in range(len(usuarios)):
            if usuarios[i]["cpf"] == vinculo:
                usuarios[i]["contas"].append(nova_conta)
        print("Conta criada com sucesso!")
    else:
        print("CPF não encontrado!")

def listar_contas(usuarios):
    for i in usuarios:
        for j in i["contas"]:
            linha = f"""\
                Titular:\t{i['nome']}
                Agência:\t{j['agencia']}
                C/C:\t\t{j['numero']}
            """
            print("="*100)
            print(textwrap.dedent(linha))

def filtro(valor_procurado, valores):
    valor_existe = False
    for i in valores:
        if valor_procurado in list(i.values()):
            valor_existe = True
    return valor_existe

def main():
    LIMITE_SAQUES = 3
    lista_de_usuarios = list()
    lista_de_contas = list()
    extrato = {"operacao": [], "saldo": 0, "numero_saques": 0, "limite": 500}

    while True:
        opcao = menu()
        if opcao == "d":
            depositar(extrato)

        elif opcao == "s":
            sacar(extrato = extrato, limite_saques = LIMITE_SAQUES)

        elif opcao == "e":
            exibir_extrato(extrato["saldo"], operacao = extrato["operacao"])

        elif opcao == "c":
            criar_conta(lista_de_contas, lista_de_usuarios)

        elif opcao == "u":
            lista_de_usuarios = criar_usuario(lista_de_usuarios)

        elif opcao == "l":
            listar_contas(lista_de_usuarios)

        elif opcao == "q":
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()