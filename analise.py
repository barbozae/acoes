import streamlit as st
import yfinance as yf
import time as time
import pandas as pd
import datetime as datetime
import streamlit_shadcn_ui as ui
import altair as alt

import requests
import zipfile
from io import BytesIO


st.set_page_config(
    page_title="Investimentos",
    page_icon="💲",
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Report a Bug': "mailto:edsonbarboza2006@hotmail.com",
        'About': 'Aplicativo desenvolvido por Edson Barboza com objetivo de realizar acompanhamento de ações.'
    })

@st.cache_data(ttl=3600)
def get_acoes():
    # acoes = ['^bvsp', 'cyre3.sa', 'bpac11.sa', 'bbas3.sa', 'eqtl3.sa', 'recv3.sa', 'prio3.sa' 'sanb11.sa', 'b3sa3.sa', 'elet3.sa', \
    #          'itub4.sa', 'alup11.sa', 'cmig4.sa', 'cple6.sa', 'petr4.sa', 'tims3.sa', 'vale3.sa', 'vivt3.sa', 'viva3.sa', 'gmat3.sa', \
                # 'igti11.sa', 'suzb3.sa']
    # tickers = yf.Tickers(acoes, period='2y')

    tickers = yf.Tickers('^bvsp \
                        cxse3.sa petr4.sa dirr3.sa eqtl3.sa sanb11.sa \
                        itub4.sa alup11.sa bbas3.sa cmig4.sa cple6.sa cyre3.sa viva3.sa\
                        prio3.sa wege3.sa vale3.sa gmat3.sa igti11.sa, suzb3.sa')

    ibovespa = tickers.tickers['^BVSP'].history(period='2y')

    caixa = tickers.tickers['CXSE3.SA'].history(period="2y")
    petrobras = tickers.tickers['PETR4.SA'].history(period="2y")
    direcional = tickers.tickers['DIRR3.SA'].history(period="2y")
    equatorial = tickers.tickers['EQTL3.SA'].history(period="2y")
    santander = tickers.tickers['SANB11.SA'].history(period="2y")

    itau = tickers.tickers['ITUB4.SA'].history(period="2y")
    alupar = tickers.tickers['ALUP11.SA'].history(period="2y")
    brasil_on = tickers.tickers['BBAS3.SA'].history(period="2y")
    cemig = tickers.tickers['CMIG4.SA'].history(period="2y")
    copel = tickers.tickers['CPLE6.SA'].history(period="2y")
    cyrela = tickers.tickers['CYRE3.SA'].history(period='2y')
    vivara = tickers.tickers['VIVA3.SA'].history(period="2y")

    petrorio = tickers.tickers['PRIO3.SA'].history(period="2y")
    wege = tickers.tickers['WEGE3.SA'].history(period="2y")
    vale = tickers.tickers['VALE3.SA'].history(period="2y")
    grupo_matheus = tickers.tickers['GMAT3.SA'].history(period="2y")
    iguatemi = tickers.tickers['IGTI11.SA'].history(period="2y")
    suzano = tickers.tickers['SUZB3.SA'].history(period="2y")

    # Adicionar uma coluna para identificar cada ação
    ibovespa['Symbol'] = '^BVSP.SA'

    caixa['Symbol'] = 'CXSE3.SA'
    petrobras['Symbol'] = 'PETR4.SA'
    direcional['Symbol'] = 'DIRR3.SA'
    equatorial['Symbol'] = 'EQTL3.SA'
    santander['Symbol'] = 'SANB11.SA'

    itau['Symbol'] = 'ITUB4.SA'
    alupar['Symbol'] = 'ALUP11.SA'
    brasil_on['Symbol'] = 'BBAS3.SA'
    cemig['Symbol'] = 'CMIG4.SA'
    copel['Symbol'] = 'CPLE6.SA'
    cyrela['Symbol'] = 'CYRE3.SA'
    vivara['Symbol'] = 'VIVA3.SA'

    petrorio['Symbol'] = 'PRIO3.SA'
    wege['Symbol'] = 'WEGE3.SA'
    vale['Symbol'] = 'VALE3.SA'
    grupo_matheus['Symbol'] = 'GMAT3.SA'
    iguatemi['Symbol'] = 'IGTI11.SA'
    suzano['Symbol'] = 'SUZB3.SA'

    # Concatenar todos os DataFrames
    dfs = [ibovespa, 
           caixa, petrobras, direcional, equatorial, santander,
           itau, alupar, brasil_on, cemig, copel, cyrela, vivara,
           petrorio, wege, vale, grupo_matheus, iguatemi, suzano
           ]
    df = pd.concat(dfs)
    df = df.drop('Stock Splits', axis=1)

    df['Variação'] = df['Close'] - df['Open']

    # df['Rendimento'] = (df['Close'] / df['Open']) - 1
    # df_concat['Variação'] = df_concat['Close'].pct_change() * 100

    # Resetar o índice para uma melhor organização
    df.reset_index(inplace=True)
    return df

@st.cache_data(ttl=43200)
def get_fundos():
    ano = "2024"
    # Criar uma lista para armazenar os DataFrames de cada mês
    dados_completos = []
    # Loop para iterar sobre todos os meses do ano
    for mes in range(1, 13):
        # Formatar o mês com dois dígitos (ex: '01', '02', ...)
        mes_formatado = f"{mes:02d}"
        # Criar a URL para o mês correspondente
        url = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes_formatado}.zip'

        print(f"Baixando dados do mês: {mes_formatado}/{ano}")

        # Fazer o download do arquivo ZIP
        download = requests.get(url)
        # Verificar se o download foi bem-sucedido
        if download.status_code == 200:
            # Abrir o arquivo ZIP a partir do conteúdo baixado
            arquivo_zip = zipfile.ZipFile(BytesIO(download.content))
            
            # Ler o arquivo CSV dentro do ZIP
            dados_fundos = pd.read_csv(arquivo_zip.open(arquivo_zip.namelist()[0]), sep=";", encoding='ISO-8859-1', low_memory=False)

            # Renomear coluna se necessário pois a partir de outubro/24 a coluna CNPJ_FUNDO foi alterada
            if 'CNPJ_FUNDO_CLASSE' in dados_fundos.columns:
                dados_fundos.rename(columns={'CNPJ_FUNDO_CLASSE': 'CNPJ_FUNDO'}, inplace=True)

            # Filtrar os dados com base no CNPJ após garantir o nome correto da coluna
            dados_fundos = dados_fundos[dados_fundos['CNPJ_FUNDO'].str.contains(
                "20.147.389/0001-00|34.172.497/0001-47|47.612.737/0001-29|36.249.317/0001-03", 
                na=False
            )]
            # Adicionar os dados do mês ao DataFrame completo
            dados_completos.append(dados_fundos)
        else:
            print(f"Erro ao baixar dados para {mes_formatado}/{ano}")

    # Concatenar todos os DataFrames em um único DataFrame
    df_fundos = pd.concat(dados_completos, ignore_index=True)
    dados_fundos = dados_fundos.drop(['RESG_DIA', 'CAPTC_DIA'], axis=1)
    return df_fundos

@st.cache_data(ttl=86400)
def get_name_fundos():
    df_name_fundos = pd.read_csv('https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv', 
                             sep = ";", encoding = 'ISO-8859-1')
    df_name_fundos = df_name_fundos[['CNPJ_FUNDO', 'DENOM_SOCIAL']]
    df_name_fundos = df_name_fundos.drop_duplicates()
    return df_name_fundos

@st.cache_data(ttl=86400)
def get_cdi():
    # site para consultar o codigo para tipo de consulta
    # https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
    #taxa selic 12, cdi 4398

    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados?formato=json&dataInicial=01/01/2023&dataFinal=31/12/2024"
    response = requests.get(url)
    dados = response.json()
    # Converter para DataFrame
    df_cdi = pd.DataFrame(dados)
    # Converter a coluna 'data' para o tipo datetime
    df_cdi['data'] = pd.to_datetime(df_cdi['data'], format='%d/%m/%Y')
    # Converter a coluna 'valor' para o tipo float
    df_cdi['valor'] = df_cdi['valor'].astype(float)
    # Calculando a variação percentual dia a dia
    df_cdi = df_cdi.rename(columns={'valor': 'Close', 'data': 'Date'})
    df_cdi['Symbol'] = df_cdi['Symbol'] = 'CDI'
    return df_cdi


class Application:
    def __init__(self):
        self.df = get_acoes()
        self.display_data()
        self.card()
        self.navegacao()
        
    def navegacao(self):
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Análise diária', 'Crescimento', 'Variação %', 'Volume', 'Dividendo', 'Hora de vender'])
        with tab1:
            self.analise_diaria()
        with tab2:
            self.rendimento()
        with tab3:
            self.variacao()
        with tab4:
            self.volume()
        with tab5:
            self.dividendo()
        with tab6:
            self.vender()

    def display_data(self):
        df_acoes = get_acoes()
        df_acoes['Date'] = pd.to_datetime(df_acoes['Date']).dt.date
        df_fundos = get_fundos()
        df_name_fundos = get_name_fundos()
        df_cdi = get_cdi()
        # df_cdi['Rendimento'] = df_cdi['Close'].cumsum()

        base_fundos = pd.merge(df_fundos, df_name_fundos, how = "left", 
                            left_on = ["CNPJ_FUNDO"], right_on = ["CNPJ_FUNDO"])
        base_fundos = base_fundos[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'DT_COMPTC', 'VL_QUOTA', 'VL_PATRIM_LIQ', 'NR_COTST']]
        base_multimercado = base_fundos.rename(columns={'DENOM_SOCIAL': 'Symbol', 'DT_COMPTC': 'Date', 'VL_QUOTA': 'Close'})

        # Concatenar base_multimercado e df_cdi
        base_multimercado = pd.concat([base_multimercado, df_cdi], ignore_index=True)

        # base_multimercado = base_multimercado[base_multimercado['Symbol'].str.contains("ARMOR AXE FI|ABSOLUTE HIDRACDI", na = False)]
    
        # Substituir os valores na coluna 'nome_fundo'
        base_multimercado['Symbol'] = base_multimercado['Symbol'].replace('ARMOR AXE FI EM COTAS DE FUNDOS DE INVESTIMENTO MULTIMERCADO', 'ARMOR AXE')
        base_multimercado['Symbol'] = base_multimercado['Symbol'].replace('ABSOLUTE HIDRA CDI FIC DE FIF RENDA FIXA INVESTIMENTO EM INFRAESTRUTURA CRÉDITO PRIVADO - RL', 'ABSOLUTE HIDRA')
        base_multimercado['Symbol'] = base_multimercado['Symbol'].replace('ITAÚ AÇÕES BDR NÍVEL I FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS DE INVESTIMENTO', 'ITAÚ FUNDOS')
        base_multimercado['Symbol'] = base_multimercado['Symbol'].replace('ITAÚ INDEX US TECH FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS DE INVESTIMENTO EM AÇÕES', 'US TECH')

        # Concatenando os DataFrames verticalmente
        df = pd.concat([df_acoes, base_multimercado], ignore_index=True)

        st.title('👨🏻‍💼 Análise Carteira de Ações')
        
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        # Adiciona o slider para selecionar o intervalo de datas
        # dates = df['Date'].unique()

        # self.inicio_data, self.fim_data = st.select_slider(
        #                                         "Selecione o intervalo de datas",
        #                                         options=dates,
        #                                         value=(dates.min(), dates.max())
        #                                         )
        
        # datas que inicia o sistema
        tempo = time.time()
        tempo_local = time.localtime(tempo)

        col1, col2 = st.columns(2)
        with col1:
            self.inicio_data = st.date_input(
                'Data inicial', 
                datetime.date(tempo_local[0], tempo_local[1], 1), format='DD/MM/YYYY') 
        with col2:
            self.fim_data = st.date_input(
                    'Data final', 
                    datetime.date.today(), format='DD/MM/YYYY')

        # Filtro por Symbol
        selecao = st.radio('Seleção',
                                    ['Top5 + Minhas Ações', 'Acompanhando', 'Top5', 'Minhas Ações', 'MultiMercado', 'Exterior'], horizontal=True, index=2)
        
        # Obter os símbolos disponíveis no DataFrame
        simbolos = df['Symbol'].unique()

        top5_itau = ['CXSE3.SA', 'PETR4.SA', 'DIRR3.SA', 'EQTL3.SA', 'SANB11.SA']
        minha_acoes = ['ALUP11.SA', 'CMIG4.SA', 'CPLE6.SA', 'BBAS3.SA', 'CYRE3.SA', 'ITUB4.SA', 'VIVA3.SA']
        multimercado = ['ARMOR AXE', 'ABSOLUTE HIDRA']
        acompanhando = ['PRIO.SA', 'VALE3.SA', 'GMAT3.SA', 'IGTI11.SA', 'SUZB3.SA', 'WEGE3.SA']
        exterior = ['US TECH', 'ITAÚ FUNDOS']

        if selecao == 'Top5 + Minhas Ações':
            default_selecao = minha_acoes + top5_itau
        elif selecao == 'Acompanhando':
            default_selecao = acompanhando
        elif selecao == 'Minhas Ações':
            default_selecao = minha_acoes
        elif selecao == 'MultiMercado':
            default_selecao = multimercado
        elif selecao == 'Exterior':
            default_selecao = exterior
        else:
            default_selecao = top5_itau

        # Garantir que os valores de selecao estão nas opções disponíveis
        default_selecao = [item for item in default_selecao if item in simbolos]

        self.select_symbol = st.multiselect('Selecione as ações', 
                                       simbolos, 
                                       default=default_selecao,
                                       placeholder='Escolha uma opção')
        if self.select_symbol:
            df = df[df['Symbol'].isin(self.select_symbol)]

        # Filtra o DataFrame com base no intervalo de datas selecionado
        mask = (df['Date'] >= self.inicio_data) & (df['Date'] <= self.fim_data)
        self.filtered_df = df.loc[mask]
        # Verifique quantos símbolos únicos estão presentes no DataFrame filtrado
        self.unique_symbols = self.filtered_df['Symbol'].unique()

        if len(self.unique_symbols) > 1:
            # Se houver mais de um símbolo, use pivot_table para reestruturar o DataFrame
            self.pivot_df = self.filtered_df.pivot_table(index='Date', columns='Symbol', values='Close')
        else:
            # Se houver apenas um símbolo, mantenha o DataFrame como está
            self.pivot_df = self.filtered_df.set_index('Date')[['Close']]

        # Ordene o DataFrame pelo índice 'Date'
        self.pivot_df = self.pivot_df.sort_values(by='Date')

    def card(self):
        df = get_acoes()
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        mask = (df['Date'] >= self.inicio_data) & (df['Date'] <= self.fim_data)
        df = df.loc[mask]

        # Encontrar o valor máximo da coluna 'Close' para cada 'Symbol'
        max_close_symbol = df.groupby('Symbol')['Close'].last()

        # Encontrar o último valor da coluna 'Variação' para cada 'Symbol'
        last_variation_symbol = df.groupby('Symbol')['Variação'].last()

        # Encontrar o símbolo com a maior variação
        symbol_max_variation = last_variation_symbol.idxmax() if not last_variation_symbol.empty else "Nenhum destaque"

        # Supondo que você tenha um seletor de símbolos (self.select_symbol)
        if self.select_symbol:
            # Filtrar os dados conforme a seleção feita
            filtered_symbols = [symbol for symbol in self.select_symbol if symbol in max_close_symbol.index]

            # Criar o número correto de colunas
            # cols = st.columns(len(filtered_symbols) + 2)  # Adiciona mais duas colunas para os cartões fixos
            cols = st.columns(len(filtered_symbols) + 1)
            for i, symbol in enumerate(filtered_symbols):
                with cols[i]:
                    ui.metric_card(
                        title=symbol,
                        content=round(max_close_symbol[symbol], 2),
                        description=f"{round(last_variation_symbol[symbol], 2)}% Variação",
                        key=f"card{i+1}"
                    )

            # Adiciona o cartão fixo para "Fundo Imob"
            # with cols[len(filtered_symbols)]:
            #     ui.metric_card(
            #         title="ITUB4.SA",
            #         content=max_close_symbol['ITUB4.SA'].round(2),
            #         description=f"{last_variation_symbol['ITUB4.SA'].round(2)}% Variação",
            #         key="card77"
            #     )

            # Calcular o valor dinâmico do fechamento com base nos símbolos filtrados
            filtered_variations = last_variation_symbol[filtered_symbols]
            # a linha abaixo deixava ações da ITUB fixa
            # fechamento_value = last_variation_symbol[filtered_symbols].sum() + last_variation_symbol['ITUB4.SA'] if filtered_symbols else 0
            fechamento_value = last_variation_symbol[filtered_symbols].sum() if filtered_symbols else 0

            # Encontrar o símbolo com a maior variação entre os símbolos filtrados
            symbol_max_variation_filtered = filtered_variations.idxmax() if not filtered_variations.empty else "Nenhum destaque"

            # Adiciona o cartão dinâmico para "Fechamento"
            # with cols[len(filtered_symbols) + 1]:
            with cols[len(filtered_symbols)]:
                ui.metric_card(
                    title="Fechamento",
                    content=round(fechamento_value, 2),
                    description=f'Destaque {symbol_max_variation_filtered}',
                    key="card88"
                )

    def analise_diaria(self):
        self.table_geral = self.filtered_df.copy()

        # col1, col2 = st.columns([1, 0.5])
        # col1, col2, col3, col4 = st.columns([1.5, 1, 0.32, 0.38])
        col1, col2, col3 = st.columns([1.25, 0.7, 0.25])
        with col1:
            # Use st.line_chart para criar o gráfico de linhas
            st.line_chart(self.pivot_df)

        with col2:
            df_dia_agrupado = self.table_geral.groupby(['Date'])['Variação'].sum().reset_index()
            dias_positivos = (df_dia_agrupado['Variação'] >= 0).sum()
            dias_negativos = (df_dia_agrupado['Variação'] < 0).sum()
            st.markdown(f':blue[{dias_positivos}] dias no positivo e *:red[{dias_negativos}]* dias negativo')
            
            self.table_geral = self.table_geral.sort_values(by='Date', ascending=False)
            self.table_geral = self.table_geral.drop('Dividends', axis=1)

            # Calcular o rendimento para cada linha
            def calcular_rendimento_linha(linha, df):
                symbol = linha['Symbol']
                close_atual = linha['Close']
                data_atual = linha['Date']
                
                if symbol == 'CDI':
                    # rendimento = df[df['Symbol'] == 'CDI']['Close'].cumsum().iloc[-1]
                    # Filtrar o DataFrame para o CDI até a data atual
                    rendimento = df[(df['Symbol'] == 'CDI') & (df['Date'] <= data_atual)]['Close'].cumsum().iloc[-1]

                else:
                    # Filtrar o DataFrame para o mesmo símbolo e buscar a menor data
                    menor_data = df[df['Symbol'] == symbol]['Date'].min()
                    close_menor_data = df[(df['Symbol'] == symbol) & (df['Date'] == menor_data)]['Close'].values[0]
                    # Calcular o rendimento
                    rendimento = ((close_atual - close_menor_data) / close_menor_data * 100).round(2)
                return rendimento
            # Aplicar a função para cada linha
            self.table_geral['Rendimento'] = self.table_geral.apply(calcular_rendimento_linha, axis=1, df=self.table_geral)

            st.dataframe(self.table_geral, hide_index=True, column_order=['Date', 'Symbol', 'Open', 'Low', 'Close', 'Variação', 'Rendimento'])

        with col3:
            acumulado = self.table_geral['Variação'].sum().round(2)
            st.markdown(f'Variação {acumulado}')

            df_symbol_agrupado = self.table_geral.groupby(['Symbol'])['Variação'].sum()
            st.dataframe(df_symbol_agrupado, use_container_width=True)

        # with col4:
        #     ultima_data = self.table_geral['Date'].max()
        #     df_rendimento = self.table_geral[self.table_geral['Date'] == ultima_data]
        #     df_rendimento = df_rendimento.groupby(['Symbol'])['Rendimento'].sum()

        #     # a soma foi feita diferente devido df_rendimento ter se tornado uma Series do pandas
        #     rendimento_symbol = (df_rendimento[:].sum() / len(df_rendimento[0:])).round(2)
        #     st.markdown(f'Crescimento {rendimento_symbol}%')

        #     st.dataframe(df_rendimento)

    def variacao(self):
        if len(self.unique_symbols) > 1:
            # Se houver mais de um símbolo, use pivot_table para reestruturar o DataFrame
            pivot_df_variacao = self.filtered_df.pivot_table(index='Date', columns='Symbol', values='Variação')
        else:
            # Se houver apenas um símbolo, mantenha o DataFrame como está
            pivot_df_variacao = self.filtered_df.set_index('Date')[['Variação']]

        # Ordene o DataFrame pelo índice 'Date'
        pivot_df_variacao = pivot_df_variacao.sort_values(by='Date')
        
        # Calculate the rolling mean with a window of 30 days
        pivot_df_variacao['Média Móvel'] = pivot_df_variacao.mean(axis=1).rolling(window=30).mean()
        pivot_df_variacao['Linha 0'] = 0
        st.line_chart(pivot_df_variacao)

        st.write('Variação acumulada por Período')
        variacao_total = pivot_df_variacao.copy()
        variacao_total['Total'] = variacao_total.loc[:, :].sum(axis=1)
        st.line_chart(variacao_total['Total'], color='#FFBF00')

        st.write('Variação acumulada por Symbol')
        variação_symbol = pivot_df_variacao.drop(['Média Móvel', 'Linha 0'], axis=1)
        variação_symbol = variação_symbol.sum(axis=0)
        st.line_chart(variação_symbol, color='#39FF14')


        def grafico_com_altair():
            df = self.filtered_df.copy()

            df['Média 30d'] = pivot_df_variacao.mean(axis=0).rolling(window=30).mean()

            # Calculate the rolling mean
            df['Média 30d'] = df.groupby('Symbol')['Variação'].transform(lambda x: x.rolling(window=30).mean())

            # Create the chart
            chart = alt.Chart(df).mark_line().encode(
                x='Date:T',
                y='Variação:Q',
                color='Symbol:N',   
                tooltip=['Date:T', 'Variação:Q']
            ) + alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='red').encode(
                y='y:Q'
            )

            # Create the rolling mean line
            rolling_mean_line = alt.Chart(df).mark_line(size=1.3, opacity=0.9, color='orange').encode(
                x='Date:T',
                y='Média 30d:Q',
                tooltip=['Média 30:T']
            )

            # Combine all layers
            final_chart = chart + rolling_mean_line

            # Customize the legend position
            final_chart = final_chart.configure_legend(
                        orient='bottom',  # move the legend to the bottom
                        legendX=0,  # align the legend to the left
                        legendY=0,  # align the legend to the top (within the bottom area)
                        titleOrient='left',  # align the legend title to the left
                        title=None
                        )

            # Display the chart in Streamlit
            st.altair_chart(final_chart, use_container_width=True)

    def volume(self):
        if len(self.unique_symbols) > 1:
            # Se houver mais de um símbolo, use pivot_table para reestruturar o DataFrame
            pivot_df_volume = self.filtered_df.pivot_table(index='Date', columns='Symbol', values='Volume')
        else:
            # Se houver apenas um símbolo, mantenha o DataFrame como está
            pivot_df_volume = self.filtered_df.set_index('Date')[['Volume']]

        # Ordene o DataFrame pelo índice 'Date'
        pivot_df_volume = pivot_df_volume.sort_values(by='Date')

        st.line_chart(pivot_df_volume)        

    def dividendo(self):
        df = self.filtered_df
        df = df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Variação'], axis=1)
        df = df[df['Dividends'] > 0]
        
        cols = st.columns([1.75, 0.25])
        with cols[0]:
            st.bar_chart(data=df, x='Date', y='Dividends', color='Symbol', height=400, use_container_width=True)
        with cols[1]:
            df_dividendo_acum = df.groupby(['Symbol'])['Dividends'].sum()
            st.write('Dividendos Acumulado')
            ui.table(data=df_dividendo_acum.reset_index())        

        # Criar o gráfico de barras usando Altair
        # chart = alt.Chart(df).mark_bar(size=15).encode(
        #     x='Date:T',
        #     y='Dividends:Q',
        #     color='Symbol:N',
        #     tooltip=['Date', 'Symbol', 'Dividends'],
        # ).properties(
        #     width=800,
        #     height=400
        # ).interactive()

        # # Exibir o gráfico no Streamlit
        # st.altair_chart(chart, use_container_width=True)

    def rendimento(self):
        df = self.filtered_df.copy()
        col1, col2 = st.columns([1.7, 0.28])
        # col1, col2, col3 = st.columns([2.4, 0.33, 0.38])
        with col1:
            crescimento = self.table_geral.groupby(['Date'])['Rendimento'].mean()
            st.write('Rendimento diário do Período')
            st.line_chart(crescimento, color='#FFBF00')

            if len(self.unique_symbols) > 1:
            # Se houver mais de um símbolo, use pivot_table para reestruturar o DataFrame
                pivot_df_variacao = self.table_geral.pivot_table(index='Date', columns='Symbol', values='Rendimento')
            else:
                # Se houver apenas um símbolo, mantenha o DataFrame como está
                pivot_df_variacao = self.table_geral.set_index('Date')[['Rendimento']]

            # Ordene o DataFrame pelo índice 'Date'
            pivot_df_variacao = pivot_df_variacao.sort_values(by='Date')
            
            # Calculate the rolling mean with a window of 30 days
            pivot_df_variacao['Média Móvel'] = pivot_df_variacao.mean(axis=1).rolling(window=30).mean()
            pivot_df_variacao['Linha 0'] = 0
            st.write('Rendimento diário por Symbol')
            st.line_chart(pivot_df_variacao)

            st.write('Rendimento acumulada por Symbol')
            rendimento_symbol = pivot_df_variacao.drop(['Média Móvel', 'Linha 0'], axis=1)
            # rendimento_symbol = rendimento_symbol.mean(axis=0)
            rendimento_symbol = rendimento_symbol.iloc[-1]
            st.line_chart(rendimento_symbol, color='#39FF14')

            # Calcular o rendimento para cada linha
            def calcular_rendimento_linha(linha, df):
                symbol = linha['Symbol']
                close_atual = linha['Close']
                # Filtrar o DataFrame para o mesmo símbolo e buscar a menor data
                menor_data = df[df['Symbol'] == symbol]['Date'].min()
                close_menor_data = df[(df['Symbol'] == symbol) & (df['Date'] == menor_data)]['Close'].values[0]
                # Calcular o rendimento
                rendimento = ((close_atual - close_menor_data) / close_menor_data * 100).round(2)
                return rendimento
            
            # Aplicar a função para cada linha
            df['Rendimento'] = df.apply(calcular_rendimento_linha, axis=1, df=df)
            st.dataframe(pivot_df_variacao.drop(['Média Móvel', 'Linha 0'], axis=1))

        with col2:
            ultima_data = df['Date'].max()
            df_rendimento = df[df['Date'] == ultima_data]
            df_rendimento = df_rendimento.groupby(['Symbol'])['Rendimento'].sum()

            # a soma foi feita diferente devido df_rendimento ter se tornado uma Series do pandas
            rendimento_symbol = (df_rendimento[:].sum() / len(df_rendimento[0:])).round(2)
            st.markdown(f'Crescimento {rendimento_symbol}%')
            st.dataframe(df_rendimento, use_container_width=True)

    def vender(self):
        # esse copy esta me trazendo apenas as colunas selecionadas dispensando o drop
        df_vendas = self.table_geral[['Date', 'Symbol']].copy()
        df_vendas = self.table_geral[self.table_geral['Date'] == self.table_geral['Date'].max()]
        
        # gerando dicionario com valores de venda
        valor_venda = {
            'Symbol': ['ALUP11.SA', 'CMIG4.SA', 'CPLE6.SA', 'BBAS3.SA', 'CYRE3.SA', 'ITUB4.SA', 'VIVA3.SA'],
            'Valor Venda': [42.7, 14.75, 13.30, 31.00, 30.00, 0.00, 32.00],
            'Valor Compra': [31.57, 11.51, 10.67, 28.35, 22.25, 36.57, 27.07],
            'Data Compra': ['2024-08-26', '2024-08-26', '2024-08-26', '2024-08-26', '2024-08-27', '2024-08-23', '2024-08-26']
            }        
        df_valor_venda = pd.DataFrame(valor_venda)

        df_vendas = pd.merge(df_vendas, df_valor_venda, on='Symbol', how='inner')
        df_vendas['Rentabilidade'] = ((df_vendas['Close'] - df_vendas['Valor Compra']) / df_vendas['Valor Compra'] * 100).round(2)
        df_vendas = df_vendas.sort_values(by='Rendimento', ascending=False)
        st.dataframe(df_vendas, 
                            hide_index=True, 
                            column_config={'Rentabilidade': st.column_config.NumberColumn('Rentabilidade', format='%.2f %%')},
                            column_order=['Data Compra', 'Date', 'Symbol', 'Valor Compra', 'Close', 'Valor Venda', 'Rentabilidade'])
        

if __name__ == "__main__":
    Application()
