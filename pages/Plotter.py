import pandas as pd
from pandas import ExcelWriter
import io
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import skimage as ski
import streamlit as st
import xlsxwriter
from streamlit_theme import st_theme

#Criar Página
st.set_page_config(page_title='Plotternary',layout='wide')


#Input do nome do Óleo e Tensoativo
dados = st.form(key='my_form')
sub_A=str(dados.text_input('Enter the name of Substance A:'))
sub_B=str(dados.text_input('Enter the name of Substance B:'))
sub_C=str(dados.text_input('Enter the name of Substance C:'))
submit_button = dados.form_submit_button(label='Submit')

#Gerar dataframe vazio para download após preenchimento dos nomes 
if len(sub_A) != 0:

    buffer = io.BytesIO()
    
    #Df vazio para preencher
    df_vazio = pd.DataFrame(columns = [sub_A, sub_B, sub_C,'Classification - use words or letters'])
    
    #Create a Pandas Excel writer using XlsxWriter as the engine.

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
      df_vazio.to_excel(writer, sheet_name='Sheet1', index=False)
   
    st.text('Fill the Excel template (Warning: make sure you are using . as your decimal separator)')
    
    st.download_button(
        label="Download Excel template",
        data=buffer,
        file_name='Template.xlsx',
        mime="application/vnd.ms-excel")
   
    st.text('Upload the previously filled Excel template')

    uploaded_file = st.file_uploader("Choose an Excel file")
    
    if uploaded_file is not None:
        
        fig = go.Figure()
        
        dataframe=pd.read_excel(uploaded_file)
   
        contorno=st.checkbox('Check this box for region contouring. (Warning: make sure your compositions sum up to 1)')

        pontos=st.checkbox('Check this box for scattered dots representing the regions')

        if pontos == True:    
            
            for i in range(0,len(dataframe['Classification'].unique())):
                
                vals=dataframe['Classification'].unique().tolist()

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
                    cliponaxis=False,
                    name=codigo))

                #Legenda dos Eixos
                fig.update_layout({
                    'ternary':{
                        'sum':1,
                        'aaxis':{'title': sub_A, 'min': 0.0, 'linewidth':2, 'ticks':'','layer':'below traces'},
                        'baxis':{'title': sub_B, 'min': 0.0, 'linewidth':2, 'ticks':'','layer':'below traces'},
                        'caxis':{'title': sub_C, 'min': 0.0, 'linewidth':2, 'ticks':'','layer':'below traces'}}})

                fig.update_layout(height=1200, width=1200)
                fig.update_layout()
        
           if contorno == True:

            composition=np.transpose(dataframe[[sub_A,sub_B,sub_C]].values)
      
            scale_dict={s:i for i, s in enumerate(dataframe['Classification'].unique(), start=0)}

            dataframe['Code'] = dataframe['Classification'].map(scale_dict)
 
            fig = ff.create_ternary_contour(composition,
                                            dataframe['Code'],
                                            pole_labels=[sub_A,sub_B,sub_C],
                                            interp_mode='ilr',
                                            colorscale='Portland',
                                            showscale=True)
           st.plotly_chart(fig, use_container_width=True)
        
                


























