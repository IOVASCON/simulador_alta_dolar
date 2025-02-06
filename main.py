import pandas as pd
import matplotlib.pyplot as plt
from src import simulacao, interface_grafica
import gerar_relatorio

def executar_simulacao(**dados):
    """Controla o fluxo principal da simulação para todas as estratégias"""
    resultados = {}
    
    try:
        validar_dados_entrada(dados)
        
        # Simular todas as estratégias
        for estrategia in ['moderada', 'agressiva', 'inatividade', 'padrão']:
            df, mensagem = processar_estrategia(estrategia, dados)
            resultados[estrategia] = (df, mensagem)
            
        # Capturar dados de entrada para o relatório
        dados_entrada_relatorio = {
            'dollar_values': dados['dollar_values'],
            'initial_reserves': dados['initial_reserves'],
            'burn_rate': dados['burn_rate'],
            'days_to_predict': dados['days_to_predict'],
            'market_sentiment': dados['market_sentiment'],
            'strategy': dados.get('strategy', 'padrão')
        }
        
        gerar_saidas(resultados, dados_entrada_relatorio)  # Passa os dados
        
    except Exception as e:
        interface_grafica.mostrar_erro_direto(f"Falha na simulação: {str(e)}")

def validar_dados_entrada(dados):
    """Valida os dados de entrada antes da execução"""
    if len(dados['dollar_values']) < 2:
        raise ValueError("É necessário pelo menos 2 valores históricos do dólar")
    if dados['days_to_predict'] <= 0:
        raise ValueError("O número de dias para previsão deve ser positivo")

def processar_estrategia(estrategia, dados):
    """Processa uma estratégia individual desde previsão até geração de resultados"""
    # Previsão de valores futuros
    valores_previstos = simulacao.prever_dolar(
        dados['dollar_values'],
        dados['days_to_predict']
    )
    
    # Ajuste de valores com estratégia e sentimento
    valores_ajustados = simulacao.ajustar_dolar(
        valores_previstos,
        estrategia,
        dados['market_sentiment']
    )
    
    # Combinação de dados históricos + previstos
    tendencia_completa = dados['dollar_values'] + valores_ajustados
    
    # Simulação das reservas
    reservas = simulacao.simular_reservas(
        dados['initial_reserves'],
        dados['burn_rate'],
        dados['days_to_predict'],
        estrategia,
        dados['market_sentiment']
    )
    
    # Ajuste crítico para igualar tamanho dos arrays
    reservas = equalizar_tamanho_arrays(reservas, len(tendencia_completa))
    
    return criar_dataset(tendencia_completa, reservas, estrategia, dados['market_sentiment'])

def equalizar_tamanho_arrays(reservas, tamanho_alvo):
    """Garante sincronia entre dados do dólar e reservas"""
    if not reservas:
        return [0] * tamanho_alvo
    
    ultimo_valor = reservas[-1]
    while len(reservas) < tamanho_alvo:
        reservas.append(ultimo_valor)
    return reservas[:tamanho_alvo]

def criar_dataset(tendencia, reservas, estrategia, sentimento):
    """Cria estrutura de dados final para análise com colunas padronizadas"""
    status_sentimento = (
        'positivo' if sentimento > 0 else
        'negativo' if sentimento < 0 else 
        'neutro'
    )
    
    mensagem = (
        f"Estratégia: {estrategia.capitalize()}\n"
        f"Sentimento: {status_sentimento}\n"
        f"Variação Dólar: {tendencia[0]:.2f} → {tendencia[-1]:.2f}"
    )
    
    # Dataframe com nomes de colunas padronizados em inglês
    return pd.DataFrame({
        'Day': range(len(tendencia)),
        'Dollar Value (R$)': [round(v, 2) for v in tendencia],
        'Reserves (Billion USD)': [round(r, 2) for r in reservas]
    }), mensagem

def gerar_saidas(resultados, dados_entrada):
    """Coordena a geração de todos os outputs do sistema"""
    gerar_relatorios(resultados, dados_entrada)
    plotar_graficos(resultados)

def gerar_relatorios(resultados, dados_entrada):
    """Gerencia a criação de documentos PDF"""
    gerar_relatorio.criar_relatorio(
        resultados, 
        'relatorio_simulacao.pdf',
        dados_entrada=dados_entrada  # Passa os dados capturados
    )

def plotar_graficos(resultados):
    """Produz visualizações gráficas da simulação com colunas corretas"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Gráfico de Reservas
    for estrategia, (df, _) in resultados.items():
        ax1.plot(df['Day'], df['Reserves (Billion USD)'], 
                marker='o', linewidth=1.5, label=estrategia.capitalize())
    
    ax1.set_title('Evolução das Reservas Cambiais', fontsize=14, pad=15)
    ax1.set_ylabel('Bilhões USD', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()
    
    # Gráfico do Dólar
    for estrategia, (df, _) in resultados.items():
        ax2.plot(df['Day'], df['Dollar Value (R$)'], 
                linestyle='--', marker='s', linewidth=1.5, label=estrategia.capitalize())
    
    ax2.set_title('Variação do Valor do Dólar', fontsize=14, pad=15)
    ax2.set_xlabel('Dias', fontsize=12)
    ax2.set_ylabel('Valor (R$)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig('analise_completa.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    app = interface_grafica.criar_interface(executar_simulacao)
    app.mainloop()