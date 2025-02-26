import datetime

def exibirMenu():
    print("\n========== BANCO PYTHON ==========")
    print("[1] Depósito")
    print("[2] Saque")
    print("[3] Extrato")
    print("[4] Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def depositar(saldo, extrato):
    valor = float(input("Informe o valor do depósito: R$ "))
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: +R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        return saldo, extrato, True
    else:
        print("Valor inválido para depósito.")
        return saldo, extrato, False

def sacar(saldo, extrato, limiteSaque, numeroSaques, limiteSaquesDia):
    valor = float(input("Informe o valor do saque: R$ "))
    sucesso = False
    # Verificações de saque
    if valor <= 0:
        print("Valor inválido para saque.")
    elif valor > saldo:
        print("Saldo insuficiente.")
    elif valor > limiteSaque:
        print(f"O valor do saque excede o limite de R$ {limiteSaque:.2f}.")
    elif numeroSaques >= limiteSaquesDia:
        print(f"Você atingiu o número máximo de {limiteSaquesDia} saques diários.")
    else:
        saldo -= valor
        extrato.append(f"Saque: -R$ {valor:.2f}")
        numeroSaques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        sucesso = True
    
    return saldo, extrato, numeroSaques, sucesso

def exibirExtrato(saldo, extrato):
    print("\n========== EXTRATO ==========")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for operacao in extrato:
            print(operacao)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=============================\n")

def main():
    saldo = 0.0
    limiteSaque = 500.0
    extrato = []
    numeroSaques = 0
    limiteSaquesDia = 3
    transacoesDia = 0
    limiteTransacoesDia = 10
    
    while True:
        opcao = exibirMenu()
        
        if opcao == "1":
            if transacoesDia < limiteTransacoesDia:
                saldo, extrato, sucesso = depositar(saldo, extrato)
                if sucesso:
                    transacoesDia += 1
            else:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                extrato.append(f"Transação não permitida: Limite diário excedido em {now}")
                print("Limite diário de transações excedido. Não é possível realizar a operação.")
        
        elif opcao == "2":
            if transacoesDia < limiteTransacoesDia:
                saldo, extrato, numeroSaques, sucesso = sacar(saldo, extrato, limiteSaque, numeroSaques, limiteSaquesDia)
                if sucesso:
                    transacoesDia += 1
            else:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                extrato.append(f"Transação não permitida: Limite diário excedido em {now}")
                print("Limite diário de transações excedido. Não é possível realizar a operação.")
        
        elif opcao == "3":
            exibirExtrato(saldo, extrato)
        
        elif opcao == "4":
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
