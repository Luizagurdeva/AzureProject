
import pandas as pd
import numpy as np
import calendar
import requests
import io

githubpath = 'https://github.com/Luizagurdeva/AzureProject/tree/main/data'
githubpath = './data/'
# path = "/Users/luiza/Documents/GitHub/dashlesson/data/"

df_customers = pd.read_excel(githubpath + "my_shop_data.xlsx", sheet_name="customers")
df_order = pd.read_excel(githubpath + "my_shop_data.xlsx", sheet_name="order")
df_employee = pd.read_excel(githubpath + "my_shop_data.xlsx", sheet_name="employee")
df_products = pd.read_excel(githubpath + "my_shop_data.xlsx", sheet_name="products")


def get_sales_data():
    # Employee name
    df_employee['employee_name'] = df_employee['firstname'] + ' ' + df_employee['lastname']

    # Customers name
    df_customers['customer_name'] = df_customers['first_name'] + ' ' + df_customers['last_name']

    df_products['product_name'] = df_products['productname']

    df_order['total'] = df_order['unitprice'] * df_order['quantity']
    df_order['deliverytime'] = df_order['deliverydate'] - df_order['orderdate']
    df_order['orderyear'] = df_order['orderdate'].dt.strftime("%Y")
    df_order['ordermonth'] = pd.to_datetime(df_order['orderdate'])
    df_order['ordermonth'] = df_order['ordermonth'].dt.month_name()

   
    order = pd.merge(df_order, df_products, on='product_id')
    order = pd.merge(order, df_employee, on='employee_id')
    order = pd.merge(order, df_customers, on='customer_id')

    # Order - Select colomns
    order = order[['order_id', 
                'product_id', 'productname', 'type',
                'customer_id', 'customer_name', 'city', 'country',
                'employee_id', 'employee_name', 
                'orderdate', 'deliverydate', 'deliverytime', 'orderyear', 'ordermonth',
                'total', 'quantity', 'product_name']]

    # Retuner til app.py
    return order

def get_year():
    # Year - Create a dataframe with years usede in the order dataframe
    df_year = df_order['orderdate'].dt.strftime("%Y").unique()
    df_year.sort()

    return df_year


def get_month():
        # Month - Create a dataframe with month names
    months = []
    for x in range(1, 13):
        months.append(calendar.month_name[x])

    df_month = pd.DataFrame(months, columns=["monthnames"])

    return df_month