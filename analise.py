import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Investimentos",
    page_icon="💲",
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Report a Bug': "mailto:edsonbarboza2006@hotmail.com",
        'About': 'Aplicativo desenvolvido por Edson Barboza com objetivo de realizar acompanhamento de ações.'
    })

@st.cache_data(ttl=21600)
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


    def display_data(self):
        self.df = get_acoes()
        st.title('👨🏻‍💼 Análise Carteira de Ações')
        
        # Adiciona o slider para selecionar o intervalo de datas
        dates = self.df['Date'].dt.strftime('%d/%m/%Y').unique()
        
        inicio_data, fim_data = st.select_slider(
                                                "Selecione o intervalo de datas",
                                                options=dates,
                                                value=(dates.min(), dates.max())
                                                )

        # Filtro por Symbol
        select_symbol = st.multiselect('Selecione as ações', self.df['Symbol'].unique(), placeholder='Escolha uma opção')
        
        if select_symbol:
            self.df = self.df[self.df['Symbol'].isin(select_symbol)]

        # Filtra o DataFrame com base no intervalo de datas selecionado
        mask = (self.df['Date'] >= inicio_data) & (self.df['Date'] <= fim_data)
        filtered_df = self.df.loc[mask]
        

        # Verifique quantos símbolos únicos estão presentes no DataFrame filtrado
        unique_symbols = filtered_df['Symbol'].unique()

        if len(unique_symbols) > 1:
            # Se houver mais de um símbolo, use pivot_table para reestruturar o DataFrame
            pivot_df = filtered_df.pivot_table(index='Date', columns='Symbol', values='Close')
        else:
            # Se houver apenas um símbolo, mantenha o DataFrame como está
            pivot_df = filtered_df.set_index('Date')[['Close']]

        # Ordene o DataFrame pelo índice 'Date'
        pivot_df = pivot_df.sort_values(by='Date')

        def analise_diaria():    
            col1, col2 = st.columns([1.5, 0.75])
            with col1:
                # Use st.line_chart para criar o gráfico de linhas
                st.line_chart(pivot_df)
            with col2:
                # Formatar a coluna 'Date' para exibir apenas a data
                filtered_df['Date'] = filtered_df['Date'].dt.strftime('%d\%m\%Y')

                df = filtered_df.drop('Dividends', axis=1)
                st.dataframe(df, hide_index=True, column_order=['Date', 'Symbol', 'Open', 'Low', 'Close', 'Variação'])

        def variacao():
            if len(unique_symbols) > 1:
                # Se houver mais de um símbolo, use pivot_table para reestruturar o DataFrame
                pivot_df_variacao = filtered_df.pivot_table(index='Date', columns='Symbol', values='Variação')
            else:
                # Se houver apenas um símbolo, mantenha o DataFrame como está
                pivot_df_variacao = filtered_df.set_index('Date')[['Variação']]

            # Ordene o DataFrame pelo índice 'Date'
            pivot_df_variacao = pivot_df_variacao.sort_values(by='Date')

            st.line_chart(pivot_df_variacao)

        def volume():
            if len(unique_symbols) > 1:
                # Se houver mais de um símbolo, use pivot_table para reestruturar o DataFrame
                pivot_df_volume = filtered_df.pivot_table(index='Date', columns='Symbol', values='Volume')
            else:
                # Se houver apenas um símbolo, mantenha o DataFrame como está
                pivot_df_volume = filtered_df.set_index('Date')[['Volume']]

            # Ordene o DataFrame pelo índice 'Date'
            pivot_df_volume = pivot_df_volume.sort_values(by='Date')

            st.line_chart(pivot_df_volume)
            
            

        tab1, tab2, tab3 = st.tabs(['Análise diária', 'Variação %', 'Volume'])

        with tab1:
            analise_diaria()
        with tab2:
            variacao()
        with tab3:
            volume()



if __name__ == "__main__":
    Application()