# %%
import psycopg2
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configuração da conexão com o banco de dados PostgreSQL
connection = psycopg2.connect(
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT'),
    dbname=os.environ.get('DB_NAME')
)
cursor = connection.cursor()

# Tratamento do datetime para a consulta, utilizando como primeiro fator: Dia presente seguido do dia seguinte (No meu caso real, foi necessário esse tratamento)
data_1 = datetime.now()
data_1 = data_1.replace(hour=3, minute=0, second=0)
data_2 = data_1 + timedelta(days=1)
data_2 = data_2.replace(hour=2, minute=59, second=59)
timestamp_1 = data_1.strftime('%Y-%m-%d %H:%M:%S')
timestamp_2 = data_2.strftime('%Y-%m-%d %H:%M:%S')

sql_query = sua_consulta


try:
    # Execute a consulta
    cursor.execute(sql_query)

    # Recupere os resultados
    results = cursor.fetchall()

    # Verifique se não há resultados e, se for o caso, dispare um e-mail de aviso
    if not results:
        # Configuração das informações do e-mail
        email_de = "xxxxxxx@gmail.com"
        email_para = "yyyyyyyyyyy@.com.br"
        assunto = "Aviso: Consulta sql não retornou resultados!"

        # Corpo do e-mail
        corpo_email = "A consulta SQL não retornou resultados, checar disponibilidade do algoritmo ou logs do script diário."

        # Configuração do servidor SMTP e autenticação
        servidor_smtp = "smtp.gmail.com"
        porta_smtp = 587 #padrão
        usuario = "xxxxxxx@gmail.com"
        senha = "xxxx" # Com a nova política de segurança da google, você precisa criar uma senha de acesso para aplicativos dentro da suite da sua conta google.

        # Crie uma mensagem de e-mail
        mensagem = MIMEMultipart()
        mensagem["From"] = email_de
        mensagem["To"] = email_para
        mensagem["Subject"] = assunto
        mensagem.attach(MIMEText(corpo_email, "plain"))
        mensagem["Importance"] = "High"

        # Inicie a conexão SMTP e envie o e-mail
        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()
            server.login(usuario, senha)
            server.sendmail(email_de, email_para, mensagem.as_string())

    # Exiba os resultados (se houver)
    for row in results:
        print(row)

except Exception as e:
    print("Ocorreu um erro durante a execução da consulta:", e)

connection.close()

# %%
