import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def prever_dolar(dollar_values, days_to_predict):
    """Preve valores futuros do dólar usando regressão linear."""
    X = np.arange(len(dollar_values)).reshape(-1, 1)
    y = np.array(dollar_values)
    modelo = LinearRegression().fit(X, y)
    futuro_X = np.arange(len(dollar_values), len(dollar_values) + days_to_predict).reshape(-1, 1)
    return modelo.predict(futuro_X)

def simular_reservas(initial_reserves, burn_rate, days_to_predict, strategy, market_sentiment):
    """Simula a queima de reservas cambiais com estratégias variadas."""
    reservas = [initial_reserves]
    for dia in range(days_to_predict):
        if strategy == 'moderada':
            queima = max(burn_rate - 0.1 * dia, 0)
        elif strategy == 'agressiva':
            queima = burn_rate * 1.5
        elif strategy == 'inatividade':
            queima = 0
        else:
            queima = burn_rate
        queima *= (1 - market_sentiment * 0.1)
        reservas.append(max(reservas[-1] - queima, 0))
    return reservas

def ajustar_dolar(predicted_dollar, strategy, market_sentiment):
    """Ajusta valores do dólar baseado em estratégia e sentimento."""
    ajustado = []
    for dia, valor in enumerate(predicted_dollar):
        if strategy == 'moderada':
            novo = valor * (1 + 0.001 * dia)
        elif strategy == 'agressiva':
            novo = valor * (1 - 0.002 * dia)
        elif strategy == 'inatividade':
            novo = valor * (1 + 0.003 * dia)
        else:
            novo = valor
        ajustado.append(novo * (1 + market_sentiment * 0.01))
    return ajustado