import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

def criar_interface(callback):
    root = tk.Tk()
    root.title("Simulador Econômico - Entrada de Dados")
    root.geometry("700x550")
    
    # Variáveis de controle
    status_var = tk.StringVar()
    
    # Estilos personalizados
    estilo_exemplo = ttk.Style()
    estilo_exemplo.configure("Exemplo.TLabel", foreground="#666666", font=('Arial', 8))
    estilo_exemplo.configure("Status.TLabel", foreground="#007BFF", font=('Arial', 9, 'bold'))
    
    campos = {}
    container = ttk.Frame(root, padding=20)
    container.pack(expand=True, fill='both')

    def atualizar_valor_sentimento(valor):
        valor_formatado = f"{float(valor):.2f}"
        lbl_valor_sentimento.config(text=valor_formatado)
        root.update_idletasks()

    def nova_simulacao():
        # Resetar todos os campos e estados
        for field in ['dollar_values', 'initial_reserves', 'burn_rate', 'days_to_predict']:
            campos[field].delete(0, tk.END)
        
        campos['market_sentiment'].set(0.0)
        campos['strategy'].set('padrão')
        lbl_valor_sentimento.config(text="0.00")
        status_var.set("")
        btn_executar.config(state="normal")
        btn_nova.config(state="disabled")
        btn_imprimir.config(state="disabled")

    def imprimir_relatorio():
        try:
            filepath = os.path.abspath('relatorio_simulacao.pdf')
            if os.name == 'nt':  # Windows
                os.startfile(filepath)
            else:  # Mac/Linux
                subprocess.run(['open', filepath], check=True)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o relatório: {str(e)}")

    # Componentes da interface
    labels = [
        ("Valores históricos do dólar (separados por vírgula):", 'dollar_values',
         "Ex: 5.00,5.05,5.10,5.15 (valores em reais)"),
        
        ("Reservas iniciais (bilhões USD):", 'initial_reserves',
         "Ex: 200.00 (valor numérico sem símbolos)"),
        
        ("Taxa de queima diária (bilhões USD):", 'burn_rate',
         "Ex: 2.0 (valor numérico com até 1 casa decimal)"),
        
        ("Dias para previsão:", 'days_to_predict',
         "Ex: 10 (número inteiro de dias)"),
        
        ("Sentimento de mercado (-1 a 1):", 'market_sentiment',
         "Ex: -0.5 (valores entre -1 (pessimista) e 1 (otimista))")
    ]

    for i, (texto, nome, exemplo) in enumerate(labels):
        ttk.Label(container, text=texto).grid(row=i*2, column=0, padx=10, pady=5, sticky='w')
        
        if nome == 'market_sentiment':
            frame_sentimento = ttk.Frame(container)
            frame_sentimento.grid(row=i*2, column=1, sticky='ew')
            
            scale = ttk.Scale(
                frame_sentimento, 
                from_=-1, 
                to=1, 
                orient='horizontal',
                command=lambda v: atualizar_valor_sentimento(v)
            )
            scale.pack(side='left', expand=True, fill='x')
            
            lbl_valor_sentimento = ttk.Label(frame_sentimento, text="0.00", width=5)
            lbl_valor_sentimento.pack(side='left', padx=10)
            campos[nome] = scale
        else:
            entrada = ttk.Entry(container)
            entrada.grid(row=i*2, column=1, padx=10, pady=5, sticky='ew')
            campos[nome] = entrada
        
        ttk.Label(container, text=exemplo, style="Exemplo.TLabel").grid(
            row=i*2+1, column=1, padx=10, sticky='w')

    # Combobox para estratégias
    ttk.Label(container, text="Estratégia:").grid(row=10, column=0, sticky='w')
    estrategias = ttk.Combobox(container, values=['moderada', 'agressiva', 'inatividade', 'padrão'])
    estrategias.grid(row=10, column=1, padx=10, pady=5, sticky='ew')
    estrategias.set('padrão')
    campos['strategy'] = estrategias
    ttk.Label(container, text="Ex: moderada (opções: moderada, agressiva, inatividade, padrão)", 
             style="Exemplo.TLabel").grid(row=11, column=1, padx=10, sticky='w')

    # Botões
    botoes_frame = ttk.Frame(container)
    botoes_frame.grid(row=12, column=0, columnspan=2, pady=15)
    
    btn_executar = ttk.Button(
        botoes_frame, 
        text="Executar Simulação", 
        command=lambda: validar_entradas(campos, callback, status_var, btn_executar, btn_nova, btn_imprimir)
    )
    btn_executar.pack(side='left', padx=5)
    
    btn_nova = ttk.Button(
        botoes_frame, 
        text="Nova Simulação", 
        command=nova_simulacao,
        state="disabled"
    )
    btn_nova.pack(side='left', padx=5)
    
    btn_imprimir = ttk.Button(
        botoes_frame, 
        text="Imprimir Relatório", 
        command=imprimir_relatorio,
        state="disabled"
    )
    btn_imprimir.pack(side='left', padx=5)

    # Status
    lbl_status = ttk.Label(container, textvariable=status_var, style="Status.TLabel")
    lbl_status.grid(row=13, column=0, columnspan=2, pady=10)

    container.columnconfigure(1, weight=1)
    
    return root

def validar_entradas(campos, callback, status_var, btn_executar, btn_nova, btn_imprimir):
    try:
        dollar_values = [
            float(valor.strip().replace(',', '.')) 
            for valor in campos['dollar_values'].get().split(',')
        ]
        
        dados = {
            'dollar_values': dollar_values,
            'initial_reserves': float(campos['initial_reserves'].get().replace(',', '.')),
            'burn_rate': float(campos['burn_rate'].get().replace(',', '.')),
            'days_to_predict': int(campos['days_to_predict'].get()),
            'market_sentiment': float(campos['market_sentiment'].get()),
            'strategy': campos['strategy'].get().lower()
        }
        
        callback(**dados)
        
        # Atualizar interface após sucesso
        btn_executar.config(state="disabled")
        btn_nova.config(state="normal")
        btn_imprimir.config(state="normal")
        status_var.set("Simulação concluída! Relatório PDF e gráficos gerados na pasta raiz.")
        
    except ValueError as e:
        messagebox.showerror("Erro", f"Dados inválidos: {str(e)}")
        btn_executar.config(state="normal")

def mostrar_erro_direto(mensagem):
    messagebox.showerror("Erro Crítico", mensagem)