import streamlit as st
import yfinance as yf
import time as time
import pandas as pd
import datetime as datetime
import streamlit_shadcn_ui as ui
import altair as alt

#TODO Inserir todas as seleções em dividendos
st.set_page_config(
    page_title="Investimentos",
    page_icon="💲",
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Report a Bug': "mailto:edsonbarboza2006@hotmail.com",
        'About': 'Aplicativo desenvolvido por Edson Barboza com objetivo de realizar acompanhamento de ações.'
    })

@st.cache_data(ttl=300)
def get_acoes():
    tickers = yf.Tickers('^bvsp cyre3.sa bpac11.sa bbas3.sa sbsp3.sa recv3.sa brcr11.sa prio3.sa sanb11.sa b3sa3.sa elet3.sa \
                         itub4.sa alup11.sa cmig4.sa cple6.sa petr4.sa tims3.sa vale3.sa vivt3.sa viva3.sa gmat3.sa igti11.sa, suzb3.sa')

    ibovespa = tickers.tickers['^BVSP'].history(period='2y')
    cyrela = tickers.tickers['CYRE3.SA'].history(period='2y')
    banco_BTGP = tickers.tickers['BPAC11.SA'].history(period="2y")
    brasil_on = tickers.tickers['BBAS3.SA'].history(period="2y")
    sabesp = tickers.tickers['SBSP3.SA'].history(period="2y")
    petro = tickers.tickers['RECV3.SA'].history(period="2y")
    petrorio = tickers.tickers['PRIO3.SA'].history(period="2y")
    santander = tickers.tickers['SANB11.SA'].history(period="2y")
    b3 = tickers.tickers['B3SA3.SA'].history(period="2y")
    eletrobras = tickers.tickers['ELET3.SA'].history(period="2y")
    itau = tickers.tickers['ITUB4.SA'].history(period="2y")
    alupar = tickers.tickers['ALUP11.SA'].history(period="2y")
    cemig = tickers.tickers['CMIG4.SA'].history(period="2y")
    copel = tickers.tickers['CPLE6.SA'].history(period="2y")
    petrobras = tickers.tickers['PETR4.SA'].history(period="2y")
    tim = tickers.tickers['TIMS3.SA'].history(period="2y")
    vale = tickers.tickers['VALE3.SA'].history(period="2y")
    vivo = tickers.tickers['VIVT3.SA'].history(period="2y")
    vivara = tickers.tickers['VIVA3.SA'].history(period="2y")
    grupo_matheus = tickers.tickers['GMAT3.SA'].history(period="2y")
    iguatemi = tickers.tickers['IGTI11.SA'].history(period="2y")
    suzano = tickers.tickers['SUZB3.SA'].history(period="2y")

    # Adicionar uma coluna para identificar cada ação
    ibovespa['Symbol'] = '^BVSP.SA'
    cyrela['Symbol'] = 'CYRE3.SA'
    banco_BTGP['Symbol'] = 'BPAC11.SA'
    brasil_on['Symbol'] = 'BBAS3.SA'
    sabesp['Symbol'] = 'SBSP3.SA'
    petro['Symbol'] = 'RECV3.SA'
    petrorio['Symbol'] = 'PRIO3.SA'
    santander['Symbol'] = 'SANB11.SA'
    b3['Symbol'] = 'B3SA3.SA'
    eletrobras['Symbol'] = 'ELET3.SA'
    itau['Symbol'] = 'ITUB4.SA'
    alupar['Symbol'] = 'ALUP11.SA'
    cemig['Symbol'] = 'CMIG4.SA'
    copel['Symbol'] = 'CPLE6.SA'
    petrobras['Symbol'] = 'PETR4.SA'
    tim['Symbol'] = 'TIMS3.SA'
    vale['Symbol'] = 'VALE3.SA'
    vivo['Symbol'] = 'VIVT3.SA'
    vivara['Symbol'] = 'VIVA3.SA'
    grupo_matheus['Symbol'] = 'GMAT3.SA'
    iguatemi['Symbol'] = 'IGTI11.SA'
    suzano['Symbol'] = 'SUZB3.SA'

    # Concatenar todos os DataFrames
    dfs = [ibovespa, cyrela, banco_BTGP, brasil_on, sabesp, petro, petrorio, santander, b3, 
           eletrobras, itau, alupar, cemig, copel, petrobras, tim, vale, vivo, vivara, grupo_matheus, iguatemi, suzano]
    df = pd.concat(dfs)
    df = df.drop('Stock Splits', axis=1)

    df['Variação'] = df['Close'] - df['Open']

    # df['Rendimento'] = (df['Close'] / df['Open']) - 1
    # df_concat['Variação'] = df_concat['Close'].pct_change() * 100

    # Resetar o índice para uma melhor organização
    df.reset_index(inplace=True)
    return df

class Application:
    def __init__(self):
        self.df = get_acoes()
        self.display_data()
        self.card()
        self.navegacao()
        
    def navegacao(self):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Análise diária', 'Crescimento', 'Variação %', 'Volume', 'Dividendo'])
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

    def display_data(self):
        df = get_acoes()
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
                                    ['Top5 + Pessoal', 'Acompanhando', 'Top5', 'Pessoal'], horizontal=True, index=2)
        
        # Obter os símbolos disponíveis no DataFrame
        simbolos = df['Symbol'].unique()

        if selecao == 'Top5 + Pessoal':
            default_selecao = ['ALUP11.SA', 'CMIG4.SA', 'CPLE6.SA', 'BBAS3.SA', 'PETR4.SA', 'TIMS3.SA', 'VALE3.SA', 'VIVT3.SA',
                               'SBSP3.SA', 'PRIO3.SA', 'SANB11.SA', 'B3SA3.SA', 'ELET3.SA']
        elif selecao == 'Acompanhando':
            # default_selecao = ['CYRE3.SA', 'BPAC11.SA', 'BBAS3.SA', 'SBSP3.SA', 'RECV3.SA'] # PRIMEIRAS AÇÕES COM O TOP5 DA ITAU
            default_selecao = ['PETR4.SA', 'VALE3.SA', 'GMAT3.SA', 'IGTI11.SA', 'SUZB3.SA']
        elif selecao == 'Pessoal':
            default_selecao = ['ALUP11.SA', 'CMIG4.SA', 'CPLE6.SA', 'BBAS3.SA', 'CYRE3.SA', 'VIVT3.SA', 'ITUB4.SA', 'VIVA3.SA']
        else:
            default_selecao = ['SBSP3.SA', 'PRIO3.SA', 'SANB11.SA', 'B3SA3.SA', 'ELET3.SA']

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

        # automatização 1

        # cols = st.columns(8)
        # with cols[0]:
        #     ui.metric_card(title="Ibovespa",
        #                 content=(max_close_symbol['^BVSP.SA']).round(2),
        #                 description=f"{last_variation_symbol['^BVSP.SA'].round(2)}% Variação",
        #                 key="card1")
        # with cols[1]:
        #     ui.metric_card(title="PetroRio",
        #                    content=(max_close_symbol['PRIO3.SA']).round(2),
        #                    description=f"{last_variation_symbol['PRIO3.SA'].round(2)}% Variação",
        #                    key="card2")
        # with cols[2]:
        #     ui.metric_card(title="Santander",
        #                    content=(max_close_symbol['SANB11.SA']).round(2),
        #                    description=f"{last_variation_symbol['SANB11.SA'].round(2)}% Variação",
        #                    key="card3")
        # with cols[3]:
        #     ui.metric_card(title="B3",
        #                    content=max_close_symbol['B3SA3.SA'].round(2),
        #                    description=f"{last_variation_symbol['B3SA3.SA'].round(2)}% Variação",
        #                    key="card4")
        # with cols[4]:
        #     ui.metric_card(title="Sabesp",
        #                    content=max_close_symbol['SBSP3.SA'].round(2),
        #                    description=f"{last_variation_symbol['SBSP3.SA'].round(2)}% Variação",
        #                    key="card5")
        # with cols[5]:
        #     ui.metric_card(title="Eletrobras",
        #                    content=max_close_symbol['ELET3.SA'].round(2),
        #                    description=f"{last_variation_symbol['ELET3.SA'].round(2)}% Variação",
        #                    key="card6")

        # # Drop o índice '^BVSP.SA', para somar a variação da carteira
        # if '^BVSP.SA' in last_variation_symbol.index:
        #     last_variation_symbol = last_variation_symbol.drop('^BVSP.SA')

        # # Encontrar o símbolo com a maior variação
        # symbol_max_variation = last_variation_symbol.idxmax()

        # # symbol_max_variation = last_variation_symbol.idxmax() if not last_variation_symbol.empty else "Nenhum destaque"

        # with cols[6]:
        #     ui.metric_card(title="Fundo Imob",
        #                    content=max_close_symbol['BRCR11.SA'].round(2),
        #                    description=f"{last_variation_symbol['BRCR11.SA'].round(2)}% Variação",
        #                    key="card7")
        # with cols[7]:
        #     ui.metric_card(title="Fechamento",
        #                 #    content=(max_close_symbol['RECV3.SA']).round(2),
        #                    content=last_variation_symbol.sum().round(2),
        #                    description=f'Destaque {symbol_max_variation}',
        #                    key="card8")

    def analise_diaria(self):
        self.table_geral = self.filtered_df.copy()

        # col1, col2 = st.columns([1, 0.5])
        # col1, col2, col3, col4 = st.columns([1.5, 1, 0.32, 0.38])
        col1, col2, col3 = st.columns([1.7, 0.9, 0.3])
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
            st.dataframe(df_symbol_agrupado)

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
        col1, col2 = st.columns([1.75, 0.25])
        # col1, col2, col3 = st.columns([2.4, 0.33, 0.38])
        with col1:
            crescimento = self.table_geral.groupby(['Date'])['Rendimento'].mean()
            st.line_chart(crescimento)
                    
        # with col2:
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
            # acumulado = df['Variação'].sum().round(2)
            # st.markdown(f'Variação {acumulado}')

            # df_symbol_agrupado = df.groupby(['Symbol'])['Variação'].sum()
            # st.dataframe(df_symbol_agrupado)

        with col2:
            ultima_data = df['Date'].max()
            df_rendimento = df[df['Date'] == ultima_data]
            df_rendimento = df_rendimento.groupby(['Symbol'])['Rendimento'].sum()

            # a soma foi feita diferente devido df_rendimento ter se tornado uma Series do pandas
            rendimento_symbol = (df_rendimento[:].sum() / len(df_rendimento[0:])).round(2)
            st.markdown(f'Crescimento {rendimento_symbol}%')

            st.dataframe(df_rendimento)


if __name__ == "__main__":
    Application()
