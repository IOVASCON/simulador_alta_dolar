# 📂 Projeto: Simulador de Alta do Dólar

![Logo do Projeto](images/logo.webp)

## 🖍️ Descrição

Este projeto é um simulador econômico desenvolvido em Python que analisa o impacto de diferentes estratégias cambiais na alta do dólar. Ele combina cálculos matemáticos, projeções financeiras e relatórios detalhados para auxiliar na tomada de decisões econômicas.

## 🎯 Objetivo do Projeto

O objetivo principal deste projeto é fornecer uma ferramenta que permita simular e avaliar o impacto de estratégias cambiais no mercado financeiro, auxiliando gestores em situações de crise ou planejamento financeiro.

## 🚀 Funcionalidades

- **Simulação Cambial:** Projeções baseadas em históricos e parâmetros definidos pelo usuário.
- **Interface Gráfica Intuitiva:** Captura e validação de entradas do usuário.
- **Relatórios Profissionais:** Geração de PDFs e gráficos PNG detalhados.
- **Comparativo entre Estratégias:** Análise de diferentes abordagens cambiais.

## 📂 Estrutura do Projeto

Abaixo está uma visualização da estrutura do projeto:

├── data
├── docs
├── images
├── src
├── tests
├── desktop.ini
├── gerar_relatorio.py
├── main.py
├── README.md
├── relatorio_simulacao.pdf
├── requirements.txt

## 🏆 Benefícios do Simulador

- **Precisão:** Elimina erros manuais em cálculos financeiros.
- **Eficiência:** Automatiza análises complexas, economizando tempo.
- **Clareza:** Gera relatórios detalhados que auxiliam na tomada de decisões.

## 🔄 Relacionamento Entre os Módulos

graph TD
    A[main.py] -->|chama| B[interface_grafica.py]
    A -->|utiliza| C[simulacao.py]
    A -->|gera| D[gerar_relatorio.py]
    D -->|produz| E[Relatório PDF]
    D -->|exporta| F[Gráficos PNG]

## 🔧 Como Executar

1. Clone o repositório:

   git clone <https://github.com/iovascon/simulador_alta_dolar.git>

2. Navegue até o diretório do projeto:

   cd simulador_alta_dolar

3. Configure o ambiente virtual (se necessário):

   python3 -m venv venv
   source venv/Scripts/activate

4. Instale as dependências:

   pip install -r requirements.txt

5. Execute o programa principal:

   python main.py

## 💻 Ambiente Virtual

Ambiente virtual configurado: **Sim** (usando requirements.txt)

## 📦 Bibliotecas Utilizadas

As bibliotecas utilizadas no projeto incluem:

- **matplotlib**: Visualizações e gráficos
- **pandas**: Manipulação de dados
- **reportlab**: Criação de relatórios PDF
- **scikit-learn**: Algoritmos de aprendizado de máquina
- **numpy**: Cálculos matemáticos
- **tabulate**: Geração de tabelas

## 🚀 Tecnologias Utilizadas

As principais tecnologias incluem:

- [Python](https://www.python.org/)
- [Matplotlib](https://matplotlib.org/)
- [ReportLab](https://www.reportlab.com/)

## 📅 Conteúdo do Relatório

- **Parâmetros utilizados na simulação.**
- **Evolução diária do dólar e reservas.**
- **Comparativo entre estratégias.**
- **Parecer técnico detalhado.**

## 🚩 Tarefas

- [X] Implementar validações adicionais.
- [x] Criar interface para usuários.
- [ ] Melhorar documentação.

## 🔹 Histórico de Lançamento

- **0.2.0**
  - MUDANÇA: Remover função antiga.
  - ADICIONAR: Implementar init().
- **0.1.1**
  - CORREÇÃO: Resolver travamento ao executar foo().
- **0.1.0**
  - MUDANÇA: Refatorar foo() para bar().
- **0.0.1**
  - Inicializar o projeto.

## 🙏 Contribuições

Feedbacks e sugestões são sempre bem-vindos! Sinta-se à vontade para abrir [**issues**](https://github.com/IOVASCON/projeto/issues) ou enviar [**pull requests**](https://github.com/IOVASCON/projeto/pulls).

## 👥 Autor

- [@iovascon](https://github.com/IOVASCON)

## 🔖 Licença

Este projeto está sob a licença [MIT](https://opensource.org/licenses/MIT).
