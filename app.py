
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import calendar
import plotly.express as px
import plotly.graph_objects as go

import structured_data
order = structured_data.get_sales_data()
df_year = structured_data.get_year()
df_month = structured_data.get_month()

fig_employee = px.bar(order, 
    x='employee_name', y='total', 
    color='type', text='total', title='Sales by Employee',
    hover_data=[],
    labels={'total':'Total sales', 'employee_name':'Employee', 'type':'Product Type'})
fig_employee.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_employee.update_layout(uniformtext_minsize=7, uniformtext_mode='hide', xaxis_tickangle=46)

fig_products = px.bar(order, 
    x='product_name', y='quantity', 
    color='type', text='total', title='Product Sales',
    hover_data=[],
    labels={'productsale':'Product Sales', 'product_name':'Product', 'type':'Product Type'})
fig_products.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_products.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=45)

#app = dash.Dash(__name__)

dash_app = dash.Dash(__name__)
app = dash_app.server

dash_app.layout = html.Div(
    children=[
        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                html.H2('Sales by Employees'),
                                html.P('Select filters from dropdown'),

                    html.Div(children="Month", className="menu-title"),
                            dcc.Dropdown(
                                id='drop_month',
                                options=[{'label':selectmonth, 'value':selectmonth} for selectmonth in df_month['monthnames']],
                            ),
                    html.Div(children="Year", className="menu-title"),
                            dcc.Dropdown(
                                id='drop_year',
                                options=[{'label':selectyear, 'value':selectyear} for selectyear in df_year]
                            ),
                            ]
                    ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id="sales_employee", figure=fig_employee),
                                dcc.Graph(id="sales_products", figure=fig_products)
                            ]
                    ),
                ]
            )
        ]
)


# we are taking the input of the contents, and 'drop_month', 'drop_year' - 'value' 
@dash_app.callback(Output('sales_employee', 'figure'),
              [Input('drop_month', 'value')],
              [Input('drop_year', 'value')])
              

def update_graph(drop_month, drop_year):
    if drop_year:
        if drop_month:
          
            order_fig1 = order.loc[(order['orderyear'] == drop_year) & (order['ordermonth'] == drop_month)]
        else:
           
            order_fig1 = order.loc[order['orderyear'] == drop_year]
    else:
        if drop_month:
            
            order_fig1 = order.loc[order['ordermonth'] == drop_month]
        else:
            # Ingen data - ikke noget valgt
            order_fig1 = order
        
    return {'data':[go.Bar(
        x = order_fig1['employee_name'],
        y = order_fig1['total']
            )
        ]
    }


if __name__ == '__main__':
    dash_app.run_server(debug=True)
