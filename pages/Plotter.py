import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import skimage as ski
import streamlit as st
import xlsxwriter


#Criar Página
st.set_page_config(page_title='Plotternary',layout='wide')

st.sidebar.image("sidebar_light.png",  use_container_width=True)

#Título da Página
st.image("light_logo.png")

#Input do nome do Óleo e Tensoativo
dados = st.form(key='my_form')
sub_A=str(dados.text_input('Enter the name of Substance A:'))
sub_B=str(dados.text_input('Enter the name of Substance B:'))
sub_C=str(dados.text_input('Enter the name of Substance C:'))
submit_button = dados.form_submit_button(label='Submit')

#Gerar dataframe vazio para download após preenchimento dos nomes 
if len(sub_A) != 0:

    #Df vazio para preencher
    df_vazio = pd.DataFrame(columns = [sub_A, sub_B, sub_C,'Classification'])
    
    #Create a Pandas Excel writer using XlsxWriter as the engine.
      
    table=df_vazio.to_excel('Template.xlsx')
   
    st.text('Fill the Excel template (Warning: make sure you are using . as your decimal separator)')
    
    st.download_button(
        label="Download Excel template",
        file_name="Template.xlsx",
        mime="application/vnd.ms-excel")
   
    st.text('Upload the previously filled Excel template')

    uploaded_file = st.file_uploader("Choose an Excel file")
    
    if uploaded_file is not None:

        dataframe=pd.read_excel(uploaded_file)
   
        fig = go.Figure()

        contorno=st.checkbox('Check this box for region contouring. (Warning: make sure your compositions sum up to 1)')

        pontos=st.checkbox('Check this box for scattered dots representing the regions')

        if pontos == True:    
            
            for i in range(0,len(dataframe['Classification'].unique())):
                
                vals=dataframe['Classification'].unique()

                #Caracterização das Amostras
                
                codigo = str(vals[i])
                
                df_code = dataframe[dataframe['Classification']==codigo]

                fig.add_trace(
                go.Scatterternary(
                    mode='markers',
                    a=df_code[sub_A],
                    b=df_code[sub_B],
                    c=df_code[sub_C],
                    marker=dict(size=8),
                    name=codigo))

                #Legenda dos Eixos
                fig.update_layout({
                    'ternary':{
                        'sum':1,
                        'aaxis':{'title': sub_A, 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                        'baxis':{'title': sub_B, 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                        'caxis':{'title': sub_C, 'min': 0.01, 'linewidth':2, 'ticks':'outside' }}})

                fig.update_layout(height=1200, width=1200)
                fig.update_layout()

        if contorno == True:

            composition=np.transpose(dataframe[[sub_A,sub_B,sub_C]].values)
            scale=dataframe['Classification'].values
 
            fig = ff.create_ternary_contour(composition,
                                            scale,
                                            pole_labels=[sub_A,sub_B,sub_C],
                                            interp_mode='ilr',
                                            colorscale='Portland',
                                            showscale=True)
        
        st.plotly_chart(fig, use_container_width=True)
