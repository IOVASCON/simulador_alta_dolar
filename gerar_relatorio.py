from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Dicionário com as descrições detalhadas de cada estratégia
DESCRICOES_ESTRATEGIAS = {
    'agressiva': [
        "• Intervenção intensiva com alto gasto de reservas",
        "• Controle cambial imediato",
        "• Redução média de reservas: 15-20% em 14 dias",
        "• Recomendação: Uso em crises agudas"
    ],
    'inatividade': [
        "• Nenhuma intervenção governamental",
        "• Valorização livre do dólar",
        "• Reservas mantidas integralmente",
        "• Recomendação: Contextos estáveis"
    ],
    'moderada': [
        "• Redução gradual de intervenções",
        "• Equilíbrio entre controle e reservas",
        "• Redução média de reservas: 8-12% em 14 dias",
        "• Recomendação: Cenário padrão recomendado"
    ],
    'padrão': [
        "• Política cambial convencional",
        "• Manutenção de taxas fixas",
        "• Redução linear de reservas",
        "• Recomendação: Situações previsíveis"
    ]
}

def formatar_moeda(valor):
    return locale.currency(valor, grouping=True, symbol=False)

def traduzir_estrategia(estrategia):
    traducao = {
        'agressiva': 'Intervenção intensiva com alto gasto de reservas para controle imediato',
        'moderada': 'Ações graduais buscando equilíbrio entre reservas e controle cambial',
        'inatividade': 'Nenhuma intervenção governamental no mercado cambial',
        'padrão': 'Manutenção da política cambial vigente sem alterações'
    }
    return traducao.get(estrategia, 'Estratégia não especificada')

def salvar_estrategia_png(df, estrategia):
    plt.figure(figsize=(10, 4))
    ax = plt.gca()
    ax.axis('off')
    
    # Criar a tabela
    tabela = plt.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='center'
    )
    
    # Definir o tamanho da fonte para todas as células
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)  # Define o tamanho da fonte globalmente
    
    # Ajustar as propriedades de cada célula individualmente, se necessário
    for key, cell in tabela.get_celld().items():
        cell.set_fontsize(10)  # Define o tamanho da fonte para cada célula
    
    # Salvar a figura
    plt.savefig(f'estrategia_{estrategia}.png', bbox_inches='tight', dpi=300)
    plt.close()

def criar_relatorio(resultados, nome_arquivo, cidade="Ponta Grossa", estado="PR", dados_entrada=None):
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    
    elementos = []
    estilos = getSampleStyleSheet()
    
    # Estilos personalizados
    estilos.add(ParagraphStyle(
        name='Cabecalho',
        fontSize=10,
        textColor=colors.grey,
        alignment=2
    ))

    estilos.add(ParagraphStyle(
        name='DetalhesEstrategia',
        fontSize=10,
        leading=13,
        spaceBefore=6,
        spaceAfter=6,
        bulletIndent=10,
        bulletFontName='Helvetica-Bold'
    ))
    
    estilos.add(ParagraphStyle(
        name='Saudacao',
        fontSize=12,
        spaceAfter=15
    ))
    
    estilos.add(ParagraphStyle(
        name='Corpo',
        fontSize=12,
        leading=14,
        spaceAfter=12
    ))
    
    estilos.add(ParagraphStyle(
        name='Conclusao',
        fontSize=12,
        leading=14,
        backColor=colors.lightgrey,
        borderPadding=10,
        spaceBefore=20,
        spaceAfter=20
    ))

    # Cabeçalho com local e data
    data = datetime.now().strftime("%d de %B de %Y")
    elementos.append(Paragraph(f"{cidade}/{estado}, {data}", estilos['Cabecalho']))
    elementos.append(Spacer(1, 1*cm))

    # Endereçamento
    enderecamento = Table([
        ["DE: Analista Financeiro Chefe", "PARA: Administrador Financeiro"],
        ["Departamento de Análise Econômica", "Diretoria Executiva"],
        ["Banco Central do Brasil", "Comitê de Política Monetária"]
    ], colWidths=[8*cm, 8*cm])
    
    enderecamento.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    
    elementos.append(enderecamento)
    elementos.append(Spacer(1, 1.5*cm))

    # Saudação
    elementos.append(Paragraph("Prezado Sr. Administrador,", estilos['Saudacao']))

    # Introdução
    intro = """
    <para>
    Conforme solicitado, apresento o relatório completo da simulação cambial realizada 
    para avaliar o impacto de diferentes estratégias de intervenção no mercado financeiro. 
    O estudo contempla projeções para os próximos dias e análise detalhada das reservas cambiais.
    </para>
    """
    
    elementos.append(Paragraph(intro, estilos['Corpo']))
    elementos.append(Spacer(1, 1*cm))

    # Estilo para descrições
    estilos.add(ParagraphStyle(
        name='Descricao',
        fontSize=9,
        leading=11,
        alignment=4,  # Justificado
        spaceBefore=6,
        spaceAfter=6
    ))
    
    # Seção de Parâmetros
    elementos.append(Paragraph("<b>PARÂMETROS DA SIMULAÇÃO</b>", estilos['Heading2']))
    elementos.append(Spacer(1, 0.5*cm))

    if dados_entrada:
        # Tabela de Entradas
        # Modificar as descrições para usar Paragraph
        entradas = [
            ['Parâmetro', 'Valor', 'Descrição'],
            [
                'Valores Históricos do Dólar', 
                '\n'.join([f'R$ {valor:.2f}'.replace('.', ',') for valor in dados_entrada['dollar_values']]), 
                Paragraph('Cotações diárias do dólar dos últimos dias utilizadas como base para a projeção', estilos['Descricao'])
            ],
            [
                'Reservas Iniciais', 
                f"US$ {dados_entrada['initial_reserves']:,.2f} bilhões".replace('.', ','), 
                Paragraph('Quantidade inicial de reservas cambiais disponíveis para intervenção no mercado', estilos['Descricao'])
            ],
            [
                'Taxa de Queima Diária', 
                f"US$ {dados_entrada['burn_rate']:,.2f} bilhões/dia".replace('.', ','), 
                Paragraph('Volume médio de reservas utilizado diariamente para conter a valorização do dólar', estilos['Descricao'])
            ],
            [
                'Dias para Previsão', 
                str(dados_entrada['days_to_predict']), 
                Paragraph('Período futuro analisado pela simulação em dias corridos', estilos['Descricao'])
            ],
            [
                'Sentimento de Mercado', 
                f"{dados_entrada['market_sentiment']:.2f}".replace('.', ','), 
                Paragraph('Índice que influencia a eficácia das intervenções:<br/>'
                        '-1 = Pessimismo extremo<br/>'
                        '0 = Neutralidade<br/>'
                        '+1 = Otimismo elevado', estilos['Descricao'])
            ],
            [
                'Estratégia Adotada', 
                dados_entrada['strategy'].capitalize(), 
                Paragraph(traduzir_estrategia(dados_entrada['strategy']), estilos['Descricao'])
            ]
        ]

        tabela_entradas = Table(entradas, colWidths=[4*cm, 4*cm, 8*cm])
        tabela_entradas.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4F81BD')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (2,1), (2,-1), 8),  # Espaço à esquerda na coluna descrição
            ('RIGHTPADDING', (2,1), (2,-1), 8), # Espaço à direita na coluna descrição
        ]))
        
        elementos.append(tabela_entradas)
        elementos.append(Spacer(1, 1*cm))

    # Resultados por Estratégia
    for estrategia, (df, _) in resultados.items():
        # Título da estratégia
        elementos.append(Paragraph(f"<b>Estratégia: {estrategia.capitalize()}</b>", estilos['Heading2']))
        
        # Tabela de resultados
        dados_tabela = [['Dia', 'Valor do Dólar (R$)', 'Reservas (Bilhões USD)']]
        for _, linha in df.iterrows():
            dados_tabela.append([
                str(int(linha['Day'])),
                formatar_moeda(linha['Dollar Value (R$)']),
                locale.format_string('%.2f', linha['Reserves (Billion USD)'], grouping=True)
            ])
        
        tabela = Table(dados_tabela, colWidths=[2*cm, 4*cm, 4*cm])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4F81BD')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTSIZE', (0,0), (-1,-1), 10)
        ]))
        
        elementos.append(tabela)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Descrição detalhada da estratégia
        descricao = DESCRICOES_ESTRATEGIAS.get(estrategia, [])
        for item in descricao:
            elementos.append(Paragraph(item, estilos['DetalhesEstrategia']))
        
        elementos.append(Spacer(1, 1*cm))
        salvar_estrategia_png(df[['Day', 'Dollar Value (R$)', 'Reserves (Billion USD)']], estrategia)

    # Conclusão
    conclusao = """
    <para>
    <b>PARECER FINAL:</b><br/><br/>
    A análise comparativa demonstra que a estratégia <b>agressiva</b> apresentou maior eficácia 
    no controle cambial imediato, porém com elevado consumo de reservas. A estratégia <b>moderada</b> 
    mostrou melhor equilíbrio entre controle da moeda e preservação de recursos. Recomenda-se 
    monitoramento diário do sentimento de mercado para ajustes dinâmicos na política cambial.
    </para>
    """
    
    elementos.append(Paragraph(conclusao, estilos['Conclusao']))

    # Assinatura
    elementos.append(Spacer(1, 2*cm))
    elementos.append(Paragraph("Atenciosamente,", estilos['BodyText']))
    elementos.append(Paragraph("<b>João da Silva</b>", estilos['BodyText']))
    elementos.append(Paragraph("Analista Financeiro Sênior", estilos['BodyText']))

    doc.build(elementos)