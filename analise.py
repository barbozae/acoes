import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit_shadcn_ui as ui
import altair as alt


st.set_page_config(
    page_title="Investimentos",
    page_icon="💲",
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Report a Bug': "mailto:edsonbarboza2006@hotmail.com",
        'About': 'Aplicativo desenvolvido por Edson Barboza com objetivo de realizar acompanhamento de ações.'
    })

@st.cache_data(ttl=180)
def get_acoes():
    tickers = yf.Tickers('^bvsp cyre3.sa bpac11.sa bbas3.sa sbsp3.sa recv3.sa')

    ibovespa = tickers.tickers['^BVSP'].history(period='2y')
    cyrela = tickers.tickers['CYRE3.SA'].history(period='2y')
    banco_BTGP = tickers.tickers['BPAC11.SA'].history(period="2y")
    brasil_on = tickers.tickers['BBAS3.SA'].history(period="2y")
    sabesp = tickers.tickers['SBSP3.SA'].history(period="2y")
    petro = tickers.tickers['RECV3.SA'].history(period="2y")

    # Adicionar uma coluna para identificar cada ação
    ibovespa['Symbol'] = '^BVSP.SA'
    cyrela['Symbol'] = 'CYRE3.SA'
    banco_BTGP['Symbol'] = 'BPAC11.SA'
    brasil_on['Symbol'] = 'BBAS3.SA'
    sabesp['Symbol'] = 'SBSP3.SA'
    petro['Symbol'] = 'RECV3.SA'

    # Concatenar todos os DataFrames
    dfs = [ibovespa, cyrela, banco_BTGP, brasil_on, sabesp, petro]
    df_concat = pd.concat(dfs)
    df_concat = df_concat.drop('Stock Splits', axis=1)

    df_concat['Variação'] = df_concat['Close'].pct_change() * 100

    # Resetar o índice para uma melhor organização
    df_concat.reset_index(inplace=True)
    return df_concat

class Application:
    def __init__(self):
        self.df = get_acoes()
        self.display_data()
        self.card()
        self.navegacao()
        
    def navegacao(self):
        tab1, tab2, tab3, tab4 = st.tabs(['Análise diária', 'Variação %', 'Volume', 'Dividendo'])
        with tab1:
            self.analise_diaria()
        with tab2:
            self.variacao()
        with tab3:
            self.volume()
        with tab4:
            self.dividendo()

    def display_data(self):
        df = get_acoes()
        st.title('👨🏻‍💼 Análise Carteira de Ações')

        df['Date'] = pd.to_datetime(df['Date']).dt.date
        # Adiciona o slider para selecionar o intervalo de datas
        dates = df['Date'].unique() #.dt.strftime('%d/%m/%Y').unique()

        self.inicio_data, self.fim_data = st.select_slider(
                                                "Selecione o intervalo de datas",
                                                options=dates,
                                                value=(dates.min(), dates.max())
                                                )
        # Filtro por Symbol
        self.select_symbol = st.multiselect('Selecione as ações', 
                                       df['Symbol'].unique(), 
                                       default=['CYRE3.SA', 'BPAC11.SA', 'BBAS3.SA', 'SBSP3.SA', 'RECV3.SA'],
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

        cols = st.columns(7)
        with cols[0]:
            ui.metric_card(title="Ibovespa",
                        content=(max_close_symbol['^BVSP.SA']).round(2),
                        description=f"{last_variation_symbol['^BVSP.SA'].round(2)}% Variação",
                        key="card1")
        with cols[1]:
            ui.metric_card(title="Cyrela",
                           content=(max_close_symbol['CYRE3.SA']).round(2),
                           description=f"{last_variation_symbol['CYRE3.SA'].round(2)}% Variação",
                           key="card2")
        with cols[2]:
            ui.metric_card(title="Banco Pactual",
                           content=(max_close_symbol['BPAC11.SA']).round(2),
                           description=f"{last_variation_symbol['BPAC11.SA'].round(2)}% Variação",
                           key="card3")
        with cols[3]:
            ui.metric_card(title="Banco do Brasil",
                           content=max_close_symbol['BBAS3.SA'].round(2),
                           description=f"{last_variation_symbol['BBAS3.SA'].round(2)}% Variação",
                           key="card4")
        with cols[4]:
            ui.metric_card(title="Sabesp",
                           content=max_close_symbol['SBSP3.SA'].round(2),
                           description=f"{last_variation_symbol['SBSP3.SA'].round(2)}% Variação",
                           key="card5")
        with cols[5]:
            ui.metric_card(title="Petro Recôncavo",
                           content=max_close_symbol['RECV3.SA'].round(2),
                           description=f"{last_variation_symbol['RECV3.SA'].round(2)}% Variação",
                           key="card6")

        # Drop o índice '^BVSP.SA', para somar a variação da carteira
        if '^BVSP.SA' in last_variation_symbol.index:
            last_variation_symbol = last_variation_symbol.drop('^BVSP.SA')

        # Encontrar o símbolo com a maior variação
        symbol_max_variation = last_variation_symbol.idxmax()

        # symbol_max_variation = last_variation_symbol.idxmax() if not last_variation_symbol.empty else "Nenhum destaque"

        with cols[6]:
            ui.metric_card(title="Fechamento",
                        #    content=(max_close_symbol['RECV3.SA']).round(2),
                           content=last_variation_symbol.sum().round(2),
                           description=f'Destaque {symbol_max_variation}',
                           key="card7")

    def analise_diaria(self):
        df = self.filtered_df.copy()
        col1, col2 = st.columns([1.5, 0.75])
        with col1:
            # Use st.line_chart para criar o gráfico de linhas
            st.line_chart(self.pivot_df)
        with col2:
            # Formatar a coluna 'Date' para ordernar
            # df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

            df = df.sort_values(by='Date', ascending=False)

            df = df.drop('Dividends', axis=1)
            st.dataframe(df, hide_index=True, column_order=['Date', 'Symbol', 'Open', 'Low', 'Close', 'Variação'])

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

        # NÃO ESTOU UTILIZANDO ESSE GRÁFICO
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


if __name__ == "__main__":
    Application()
