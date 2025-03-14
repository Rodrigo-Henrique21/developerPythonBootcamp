import tkinter as tk
from tkinter import messagebox
import datetime

class Conta:
    def __init__(self, saldo_inicial=0.0, limite_saque=500.0, limite_saques_dia=3, limite_transacoes_dia=10):
        self.saldo = saldo_inicial
        self.limite_saque = limite_saque
        self.limite_saques_dia = limite_saques_dia
        self.limite_transacoes_dia = limite_transacoes_dia

        self.numero_saques = 0
        self.transacoes_dia = 0
        self.extrato = []

    def depositar(self, valor: float) -> bool:
        """ Realiza depósito se o valor for positivo. Retorna True se bem-sucedido. """
        if valor <= 0:
            return False
        self.saldo += valor
        self.transacoes_dia += 1
        self.extrato.append(f"Depósito: +R$ {valor:.2f}")
        return True

    def sacar(self, valor: float) -> bool:
        """
        Realiza saque se o valor for válido, houver saldo suficiente,
        não exceder o limite de saque e não ultrapassar o número de saques diário.
        Retorna True se o saque foi bem-sucedido.
        """
        if valor <= 0:
            return False
        if self.saldo < valor:
            return False
        if valor > self.limite_saque:
            return False
        if self.numero_saques >= self.limite_saques_dia:
            return False

        self.saldo -= valor
        self.numero_saques += 1
        self.transacoes_dia += 1
        self.extrato.append(f"Saque: -R$ {valor:.2f}")
        return True

    def exibir_extrato(self) -> str:
        """ Retorna o extrato como uma string formatada, incluindo o saldo atual. """
        if not self.extrato:
            extrato_str = "Não foram realizadas movimentações."
        else:
            extrato_str = "\n".join(self.extrato)

        extrato_str += f"\n\nSaldo atual: R$ {self.saldo:.2f}"
        return extrato_str

    def transacao_permitida(self) -> bool:
        """ Verifica se ainda há transações diárias disponíveis. """
        if self.transacoes_dia < self.limite_transacoes_dia:
            return True

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.extrato.append(f"Transação não permitida: Limite diário excedido em {now}")
        return False


class BancoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banco Python - Orientado a Objetos")
        self.root.geometry("400x400")

        # Cria a conta do usuário
        self.conta = Conta()

        # Frame principal
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Rótulo e entrada para valor
        self.label_valor = tk.Label(frame, text="Valor (R$):")
        self.label_valor.grid(row=0, column=0, padx=5, pady=5)

        self.entry_valor = tk.Entry(frame)
        self.entry_valor.grid(row=0, column=1, padx=5, pady=5)

        # Botões de Depósito, Saque, Extrato e Sair
        self.btn_depositar = tk.Button(frame, text="Depósito", width=12, command=self.depositar)
        self.btn_depositar.grid(row=1, column=0, padx=5, pady=5)

        self.btn_sacar = tk.Button(frame, text="Saque", width=12, command=self.sacar)
        self.btn_sacar.grid(row=1, column=1, padx=5, pady=5)

        self.btn_extrato = tk.Button(frame, text="Extrato", width=12, command=self.exibir_extrato)
        self.btn_extrato.grid(row=2, column=0, padx=5, pady=5)

        self.btn_sair = tk.Button(frame, text="Sair", width=12, command=self.sair_sistema)
        self.btn_sair.grid(row=2, column=1, padx=5, pady=5)

        # Rótulo para exibição do saldo
        self.label_saldo = tk.Label(self.root, text=f"Saldo atual: R$ {self.conta.saldo:.2f}",
                                    font=("Arial", 12, "bold"))
        self.label_saldo.pack(pady=5)

        # Text Widget para exibir o extrato
        self.text_extrato = tk.Text(self.root, width=50, height=10, state='disabled')
        self.text_extrato.pack(pady=10)

    def depositar(self):
        """ Lida com a ação de depósito via GUI. """
        valor_str = self.entry_valor.get()
        if not valor_str:
            messagebox.showwarning("Atenção", "Digite um valor para depósito.")
            return

        try:
            valor = float(valor_str)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        if not self.conta.transacao_permitida():
            messagebox.showwarning("Atenção", "Limite diário de transações excedido.")
            self.atualizar_extrato()
            return

        resultado = self.conta.depositar(valor)
        if resultado:
            messagebox.showinfo("Sucesso", f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            self.atualizar_saldo()
            self.limpar_entrada_valor()
        else:
            messagebox.showerror("Erro", "Valor inválido para depósito.")

    def sacar(self):
        """ Lida com a ação de saque via GUI. """
        valor_str = self.entry_valor.get()
        if not valor_str:
            messagebox.showwarning("Atenção", "Digite um valor para saque.")
            return

        try:
            valor = float(valor_str)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        if not self.conta.transacao_permitida():
            messagebox.showwarning("Atenção", "Limite diário de transações excedido.")
            self.atualizar_extrato()
            return

        resultado = self.conta.sacar(valor)
        if resultado:
            messagebox.showinfo("Sucesso", f"Saque de R$ {valor:.2f} realizado com sucesso!")
            self.atualizar_saldo()
            self.limpar_entrada_valor()
        else:
            # Verifica qual foi a condição de falha
            if valor <= 0:
                messagebox.showerror("Erro", "Valor inválido para saque.")
            elif valor > self.conta.saldo:
                messagebox.showerror("Erro", "Saldo insuficiente.")
            elif valor > self.conta.limite_saque:
                messagebox.showerror("Erro", f"O valor do saque excede o limite de R$ {self.conta.limite_saque:.2f}.")
            elif self.conta.numero_saques >= self.conta.limite_saques_dia:
                messagebox.showerror("Erro", f"Número máximo de {self.conta.limite_saques_dia} saques diários atingido.")

    def exibir_extrato(self):
        """ Lida com a ação de exibir o extrato via GUI. """
        extrato_str = self.conta.exibir_extrato()
        self.atualizar_extrato(extrato_str)

    def atualizar_saldo(self):
        """ Atualiza a exibição do saldo na janela. """
        self.label_saldo.config(text=f"Saldo atual: R$ {self.conta.saldo:.2f}")

    def atualizar_extrato(self, texto=None):
        """ Atualiza o conteúdo do Text Widget de extrato. """
        if texto is None:
            # Se não for passado, pega o extrato atual da conta
            texto = self.conta.exibir_extrato()
        self.text_extrato.config(state='normal')
        self.text_extrato.delete('1.0', tk.END)
        self.text_extrato.insert(tk.END, texto)
        self.text_extrato.config(state='disabled')

    def limpar_entrada_valor(self):
        """ Limpa o conteúdo do campo de entrada. """
        self.entry_valor.delete(0, tk.END)

    def sair_sistema(self):
        """ Encerra o programa. """
        self.root.quit()


def main():
    root = tk.Tk()
    app = BancoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
