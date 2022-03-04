#Importar as bibliotecas
from ast import Div
from distutils import debug
from itertools import count
from operator import length_hint
from tkinter import X
from click import option
import dash
from dash import html
from dash import dcc
from dash import Dash
import dash_table as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np 
import plotly.express as px
import os
from pathlib import Path

#Script para converter a base de dados para csv
#Lendo o arquivo csv
df = pd.read_csv('r_drone.csv', encoding = 'latin-1', sep =';')

#Criando uma cópia dos dados 
dataframe = df.copy()
dataframe['data'] = pd.to_datetime(dataframe['data_voo'])
dataframe['Ano'] = dataframe['data'].dt.strftime('%Y')

#Deletando Colunas que não tenho interesse 
drop_cols=['hora_inicio','hora_conclusao','hora_inicio2','hora_termino','porcentagem_inicial_bateria','porcentagem_final_bateria']
global_df = dataframe.drop(drop_cols, axis = 1)

#Contagem dos drones
n_aeronave = np.unique(dataframe['aeronave_utilizada'], return_counts= True)
resultado_aero =len(n_aeronave[1])


#Aeronave que fez mais voo
distancia_por_aeronave = global_df.groupby(['aeronave_utilizada','Ano']).sum()['distancia_percorrida']
#Criando o arquivo csv e lendo
distancia_por_aeronave.to_csv('dados_aero_voo.csv', sep=';', encoding='utf-8')
df_aeronave = pd.read_csv('dados_aero_voo.csv', encoding = 'utf-8', sep =';')

#Aeronaves mais usadas
aeronave_qtd_voo_df = dataframe.groupby(['data_voo','aeronave_utilizada'])[['distancia_percorrida']].mean()
aeronave_qtd_voo_df.reset_index(inplace=True)  

#Menor distancias
menor_distancia_por_aeronave = df_aeronave.groupby('aeronave_utilizada').sum()['distancia_percorrida']
# menor = min(menor_distancia_por_aeronave)
menor = min(distancia_por_aeronave)


#Baterias mais usadas
bateria_qtd_voo_df = global_df.groupby(['bateria_utilizada','aeronave_utilizada','Ano']).sum()['distancia_percorrida'] 
 #Criando o arquivo csv e lendo
bateria_qtd_voo_df.to_csv('dados_bateria_voo.csv', sep=';', encoding='utf-8')
df_bateria = pd.read_csv('dados_bateria_voo.csv', encoding = 'utf-8', sep =';')


#Contagem de baterias
n_bateria = np.unique(dataframe['bateria_utilizada'], return_counts= True)
resultado_bateria =len(n_bateria[1])

#DATAS DE VOO
mylist = dataframe['data_voo']
for x in range(len(mylist)):
  print(mylist[x])


#medoa de distancia percorrida
media = np.mean(global_df['distancia_percorrida'])

#DATAS DE VOO
mylistbateria = dataframe['bateria_utilizada']
for x in range(len(mylistbateria)):
  print(mylistbateria[x])

#pilotos 
n_pilotos = np.unique(global_df['piloto'], return_counts=True)
resultado_piloto = len(n_pilotos[1])

#quantidade total de voo de voo realizado por dara_voo

piloto_qtd_voo_df= global_df.groupby(['data_voo','piloto'])[['distancia_percorrida']].mean()
piloto_qtd_voo_df.reset_index(inplace=True)


n_voo = np.unique(piloto_qtd_voo_df['data_voo'], return_counts=True)
resultado_voo = len(n_voo[1])


#Distancia total por piloto
piloto_distancia_por_aeronave = dataframe.groupby('piloto').sum()['distancia_percorrida']



#------------------------------------------------------------------------------------------

#piloto por local
piloto_qtd_voo_local = global_df.groupby(['piloto','local']).sum()['distancia_percorrida']
piloto_qtd_voo_local.to_csv('dados_plt_voo.csv', sep=';', encoding='utf-8')

#variavel que le o arquivo criado
df_piloto = pd.read_csv('dados_plt_voo.csv', encoding = 'utf-8', sep =';')


# -------------------------------------------------------------------------------



#Quantidade de Locais
n_local = np.unique(global_df['local'], return_counts= True)
resultado_local =len(n_local[1])
print(f"{resultado_local}")

#DATAS DE VOO local
mylistlocal = dataframe['local']
for x in range(len(mylistlocal)):
  print(mylistlocal[x])

#-------------------------------------------------------------------------- END

#Escolhendo o tema da pagina
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR],#darkly,SOLAR
                                            #Deixar a página responsivel
                                            meta_tags= [{'name': 'viewport',
                                                        'content': 'width=device-width, initial-scale=1.0'}]
                                            )

app.layout = dbc.Container([
    dbc.Row([
    
            html.H3('  PROJETO DE DRONES COM PYTHON ',
            className = 'text-center text-success, display-2 shadow'),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
           
            dcc.Graph(
                id = 'grafico_aeronave',
                config={'displayModeBar': True},

                figure=
                    px.bar(df_aeronave,  x = 'aeronave_utilizada',y = 'distancia_percorrida',color = 'aeronave_utilizada',
                            pattern_shape='aeronave_utilizada',
                            animation_frame = 'Ano',
                            text = 'distancia_percorrida',
                            template = 'plotly_dark',
                            title = 'DISTÂNCIA TOTAL PERCORRIDA',
                            labels ={
                                'distancia_percorrida' : 'Distância (m)',
                                'aeronave_utilizada' : 'Aeronave',
                                
                            },
                            color_discrete_sequence = px.colors.qualitative.Pastel)

            )

        ], width = {'size':9, 'order':3 }),

        dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody(
                            html.P('QUANTIDADE DE DRONES',
                                className="card text-white bg-success text-center",
                                ),
                                style= {"flex" :"none"}
                        ),
                            html.H3(f"{resultado_aero} ",
                            className="text-white text-center"),
                        
                        dbc.CardBody(
                            
                            html.P(f'MENOR DISTÂNCIA PERCORRIDA',
                                className="card text-white bg-success text-center",
                                ),
                                style= {"flex" :"none"}
                        ),
                        html.H3(f"{menor}",
                            className="text-white text-center"),

                        dbc.CardBody(
                            
                            html.P(f'MAIOR DISTÂNCIA PERCORRIDA',
                                className="card text-white bg-success text-center",
                                ),
                                style= {"flex" :"none"}
                        ),
                        html.H3(f"{distancia_por_aeronave[0]} ",
                            className="text-white text-center") 

                            
                    ],
                    style={"width": "19.5rem",      
                            "height" : "100%",
                            "justify-content": "center"},
                    ),

        ], width = {'size':3, 'order':3 }),

        html.Br(),

    ]),#end-ROW_01---------------------------------------------------------------------------------------------------------------------------------
    
    html.Br(),

     dbc.Row([
        dbc.Col([
            #  dcc.Dropdown(
            #     id = 'dropdown_aeronave',
            #     options=[
            #         {'label': ' Matrice', 'value' : 'Matrice'},
            #         {'label': 'Mavic', 'value' : 'Mavic'},
            #         {'label': 'Phathon', 'value' : 'Phathon'}
            #     ],
            #     value = 'Phathon'
            # ),
            dcc.Graph(
                id = 'grafico_bateria',
                config={'displayModeBar': True},

                figure= px.bar(df_bateria, x = 'bateria_utilizada', y = 'distancia_percorrida', 
                                color = 'aeronave_utilizada', 
                                animation_frame= 'Ano',
                                text = 'distancia_percorrida',
                                template = 'plotly_dark',
                                title = 'DISTÂNCIA TOTAL PERCORRIDA POR BATERIA',
                                labels ={
                                        'bateria_utilizada' : 'Bateria',
                                        'distancia_percorrida' : 'Distância (m)',
                                        'Ano' : ' Ano ',
                                        'aeronave_utilizada' :  'Aeronave'
                                },
                                color_discrete_sequence = px.colors.qualitative.Pastel),

            )

        ], width = {'size':9, 'order':3 }),


            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody(
                            html.P('QUANTIDADE DE BATERIAS',
                                className="card text-white bg-success text-center"),
                                style= {"flex" :"none"}  
                        ),
                            html.H3(f"{resultado_bateria}",
                            className="text-white text-center"),
                    

                        dbc.CardBody(
                            
                            html.P(f'ÚLTIMA DATA DA BATERIA UTILIZADA',
                                className="card text-white bg-success text-center"),
                                style= {"flex" :"none"}
                        ),
                        html.H4(f"{mylist[x]} ",
                            className="text-white text-center"),
                        

                        dbc.CardBody(
                            
                            html.P(f'ÚLTIMA BATERIA UTILIZADA',
                                className="card text-white bg-success text-center"),
                            style= {"flex" :"none"}
                        ),
                        html.H4(f"{mylistbateria[x]} ",
                            className="text-white text-center") 
                            
                    ],
                    style={"width": "19.5rem",      
                            "height" : "100%",
                            "justify-content": "center"},
                                
                    ),

        ], width = {'size':3, 'order':3 }),

    ]),#ROw_02----------------------------------------------------------------------------------------------------------------------------------

        html.Br(),

     dbc.Row([
    
     dbc.Col([
            dcc.Graph(
                id = 'grafico_data_voo_02',
                config={'displayModeBar': False},

                figure= px.line(dataframe, x= 'data_voo',
                                y = 'distancia_percorrida',
                                animation_frame = 'Ano',
                                markers = True,
                                color = 'aeronave_utilizada',
                                title = 'DISTÂNCIA DIÁRIA PERCORRIDA',
                                template = 'plotly_dark',
                                labels ={
                                        'distancia_percorrida' : 'Distância (m)',
                                        'animation_frame' : ' Ano ',
                                        'data_voo' : 'Datas',
                                        'aeronave_utilizada' : 'Aeronave'
                                },
                                 color_discrete_sequence = px.colors.qualitative.Pastel),
                

            )

        ], width = {'size':9 ,'order':3 }),

        dbc.Col([
                dbc.Card(
                    [
                        
                        dbc.CardBody(
                            
                            html.P(f'MENOR DISTÂNCIA PERCORRIDA DIÁRIA',
                                className="card text-white bg-success text-center"),
                            style= {"flex" :"none"}
                        ),
                        html.H3(f"{min(dataframe['distancia_percorrida'])}",
                            className="text-white text-center"),
                        
                        dbc.CardBody(
                            html.P('MÉDIA DISTÂNCIA PERCORRIDA DIÁRIA',
                                className="card text-white bg-success text-center"),
                            style= {"flex" :"none"}
                        ),
                            
        
                            html.H3(f"{round(media,2)} ",
                            className="text-white text-center"),

                        dbc.CardBody(
                            
                            html.P(f'MAIOR DISTÂNCIA PERCORRIDA DIÁRIA',
                                className="card text-white bg-success text-center"),

                            style= {"flex" :"none"}
                        ),
                        html.H3(f"{max(dataframe['distancia_percorrida'])} ",
                            className="text-white text-center") 

                            
                    ],
                    style={"width": "19.5rem",      
                            "height" : "100%",
                            "justify-content": "center"},
                                
                    ),

        ], width = {'size':3, 'order':3 }),


    ]),#ROw_03----------------------------------------------------------------------------------------------------------------------------------

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id = 'grafico_piloto',
                config={'displayModeBar': False},

                figure= px.bar(df_piloto, x ='piloto',
                                y = 'distancia_percorrida', 
                                text= 'distancia_percorrida',
                                color ='local',
                                title = 'DISTÂNCIA TOTAL PERCORRIDA POR BATERIA',
                                template = 'plotly_dark',
                                labels ={
                                            'distancia_percorrida' : 'Distância (m)',
                                            'piloto' : 'piloto',
                                            'local' : 'Local'
                                },
                                color_discrete_sequence = px.colors.qualitative.Pastel),

            )

        ], width = {'size':9, 'order':3 }),

        dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody(
                            html.P('QUANTIDADE DE PILOTOS',
                                className="card text-white bg-success text-center"),
                            style= {"flex" :"none"}
                        ),
                            html.H3(f"{resultado_piloto} ",
                            className="text-white text-center"),
                        
                        dbc.CardBody(
                            
                            html.P(f'MAIOR DISTÂNCIA FEITA PILOTO',
                                className="card text-white bg-success text-center"),
                            style= {"flex" :"none"}
                        ),
                        html.H3(f"{piloto_distancia_por_aeronave[0]}",
                            className="text-white text-center"),

                        dbc.CardBody(
                            
                            html.P(f'QUANTIDADE TOTAL DE VOOS',
                                className="card text-white bg-success text-center"),
                            style= {"flex" :"none"}
                        ),
                        html.H3(f"{resultado_voo} ",
                            className="text-white text-center") 

                            
                    ],
                    style={"width": "19.5rem",      
                            "height" : "100%",
                            "justify-content": "center"},
                                
                    ),

        ], width = {'size':3, 'order':3 }),

        html.Br(),

    ]),#end-ROW_04---------------------------------------------------------------------------------------------------------------------------------

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id = 'grafico_local_data',
                config={'displayModeBar': True},
                figure=
                    px.bar(dataframe, x= 'local',
                    color = 'aeronave_utilizada',
                    pattern_shape="aeronave_utilizada",
                    template = 'plotly_dark',
                    animation_frame="Ano",
                      labels ={
                        'local' : 'Local de Voo',
                        'aeronave_utilizada' :  'Aeronaves',
                        'count' :  'Quantidade'
                    },
                    color_discrete_sequence = px.colors.qualitative.Pastel, )

            )

        ], width = {'size':9, 'order':4 }),

        dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody(
                            html.P('QUANTIDADE DE LOCAIS',
                                className="card text-white bg-success text-center"),
                            style= {"flex" :"none"}
                        ),
                            html.H3(f"{resultado_local} ",
                            className="text-white text-center"),
                        
                        dbc.CardBody(
                            
                            html.P(f'ULTIMA LOCAL DE VOO',
                                className="card text-white bg-success text-center"),
                            style= {"flex" :"none"}
                        ),
                        html.H3(f"{mylistlocal[x]}",
                            className="text-white text-center"),

                        dbc.CardBody(
                            
                            html.P(f'ULTIMA DATA DE VOO',
                                className="card text-white bg-success text-center"),
                            style= {"flex" :"none"}
                        ),
                        html.H3(f"{mylist[x]} ",
                            className="text-white text-center") 

                            
                    ],
                    style={"width": "19.5rem",      
                            "height" : "100%",
                            "justify-content": "center"},
                                
                    ),

        ], width = {'size':3, 'order':4 }),

        html.Br(),

    ]),#end-ROW_05---------------------------------------------------------------------------------------------------------------------------------
html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id = 'grafico_falha_data',
                config={'displayModeBar': True},

                figure=
                    px.bar(global_df, x= 'falhas', color="aeronave_utilizada",
                         pattern_shape="aeronave_utilizada", labels ={
                        'falhas' : ' Tipos de Falhas',
                        'aeronave_utilizada' :  'Aeronaves',
                        'count' :  'Quantidade'
                    },
                    color_discrete_sequence = px.colors.qualitative.Pastel,template = 'plotly_dark')
             

            )

        ], width = {'size':9}),

        html.Br(),

    ]),#end-ROW_06---------------------------------------------------------------------------------------------------------------------------------


html.Br(),





])#end_container.

app.run_server(debug=False, port=4080)