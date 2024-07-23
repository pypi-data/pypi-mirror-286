import pandas as pd
from enola import tracking_batch
from enola.enola_types import ErrOrWarnKind
import pandas as pd
import random

# Listas de nombres y ciudades para seleccionar aleatoriamente
nombres = ['Juan', 'María', 'Pedro', 'Lucía', 'Ana', 'Luis', 'Carlos', 'Sofía']
ciudades = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Zaragoza', 'Málaga', 'Murcia']
ocupaciones = ['Ingeniero', 'Médico', 'Abogado', 'Arquitecto', 'Profesor', 'Enfermero', 'Contador', 'Desarrollador']

# Función para generar un nombre aleatorio
def generar_nombre():
    return random.choice(nombres)

# Función para generar una ciudad aleatoria
def generar_ciudad():
    return random.choice(ciudades)

# Función para generar una ocupación aleatoria
def generar_ocupacion():
    return random.choice(ocupaciones)

# Función para generar un valor de score aleatorio
def generar_score_value():
    return random.randint(50, 100)

# Función para generar un grupo de score aleatorio
def generar_score_group():
    return random.choice(['A', 'B', 'C', 'D'])

# Función para generar un ID de cliente aleatorio
def generar_client_id():
    return random.randint(1000, 9999)

# Función para generar un ID de producto aleatorio
def generar_product_id():
    return random.randint(2000, 9999)

# Generar los datos
data = []
for _ in range(1000000):
    registro = {
        'Nombre': generar_nombre(),
        'Edad': random.randint(18, 65),
        'Ciudad': generar_ciudad(),
        'Ocupación': generar_ocupacion(),
        'score_value': generar_score_value(),
        'score_group': generar_score_group(),
        'client_id': generar_client_id(),
        'product_id': generar_product_id()
    }
    data.append(registro)

# Crear el DataFrame
df = pd.DataFrame(data)

# Mostrar las primeras filas del DataFrame
print(df.head())



#token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFTk9MQV9IVUVNVUwwNC1mYTIyOTZkNDBiYjUwMzNkYTdhZjE1N2JiMzUwYjc2ZiIsImlkIjoiZWFmMWJlOTUtMDFkNy00MzU5LTk4NDctMGE2NjBjNGEzMTE4IiwiZGlzcGxheU5hbWUiOiJOdWV2aXRhIDEiLCJhZ2VudERlcGxveUlkIjoiRU5PTEFfSFVFTVVMMDQtZmEyMjk2ZDQwYmI1MDMzZGE3YWYxNTdiYjM1MGI3NmYiLCJjYW5UcmFja2luZyI6dHJ1ZSwiY2FuRXZhbHVhdGUiOmZhbHNlLCJjYW5HZXRFeGVjdXRpb25zIjpmYWxzZSwidXJsIjoiaHR0cDovL2xvY2FsaG9zdDo3MDcyL2FwaSIsInVybEJhY2tlbmQiOiJodHRwOi8vbG9jYWxob3N0OjcwNzEvYXBpIiwib3JnSWQiOiJFTk9MQV9IVUVNVUwwNCIsImlzU2VydmljZUFjY291bnQiOnRydWUsImlhdCI6MTcxOTE2MjU2OCwiZXhwIjoxODQ1MjU5MjA4LCJpc3MiOiJlbm9sYSJ9.WYJbsHmtHYZ0CuzKZB4l0WfJVbHd4dAZRhRI0rIqYwk"
#token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFTk9MQV9IVUVNVUwwNC1mYTIyOTZkNDBiYjUwMzNkYTdhZjE1N2JiMzUwYjc2ZiIsImlkIjoiNTdlNWQ4ZDYtZWE1ZC00ZTA3LTg1ZjgtMWM0NWYwZGIyOTNhIiwiZGlzcGxheU5hbWUiOiJUb2tlbiB2MiIsImFnZW50RGVwbG95SWQiOiJFTk9MQV9IVUVNVUwwNC1mYTIyOTZkNDBiYjUwMzNkYTdhZjE1N2JiMzUwYjc2ZiIsImNhblRyYWNraW5nIjp0cnVlLCJjYW5FdmFsdWF0ZSI6dHJ1ZSwiY2FuR2V0RXhlY3V0aW9ucyI6dHJ1ZSwidXJsIjoiaHR0cHM6Ly9hcGlzZW5kLmVub2xhLWFpLmNvbS9hcGkiLCJ1cmxCYWNrZW5kIjoiaHR0cHM6Ly9hcGkuZW5vbGEtYWkuY29tL2FwaSIsIm9yZ0lkIjoiRU5PTEFfSFVFTVVMMDQiLCJpc1NlcnZpY2VBY2NvdW50Ijp0cnVlLCJpYXQiOjE3MTkzMzE0NzQsImV4cCI6MTg0NTQzMTk5OSwiaXNzIjoiZW5vbGEifQ.K5TcleYXZbb5vAd62VsMKx2IeEVLuyet6QhHi3-LaNg"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFTk9MQV9IVUVNVUwwOC0xY2MzNjUwMTE0MGUzZjFmMWNkZWNlYjgwNjBhN2ZlZCIsImlkIjoiNTlkZDNlNDgtZmEyNi00ZmRhLWEwMmYtNmU2OWMxNDE2YTFiIiwiZGlzcGxheU5hbWUiOiJjdWVudGEgc2VydmljaW8gMSIsImFnZW50RGVwbG95SWQiOiJFTk9MQV9IVUVNVUwwOC0xY2MzNjUwMTE0MGUzZjFmMWNkZWNlYjgwNjBhN2ZlZCIsImNhblRyYWNraW5nIjp0cnVlLCJjYW5FdmFsdWF0ZSI6dHJ1ZSwiY2FuR2V0RXhlY3V0aW9ucyI6dHJ1ZSwidXJsIjoiaHR0cDovL2xvY2FsaG9zdDo3MDcyL2FwaSIsInVybEJhY2tlbmQiOiJodHRwOi8vbG9jYWxob3N0OjcwNzEvYXBpIiwib3JnSWQiOiJFTk9MQV9IVUVNVUwwOCIsImlzU2VydmljZUFjY291bnQiOnRydWUsImlhdCI6MTcyMTI1MTgzNCwiZXhwIjoxODQ3MzMyNzk5LCJpc3MiOiJlbm9sYSJ9.kU_VZEy_fsC3j0QRvgiF9XyhL9IVw6o4khgyp6PkSdI"
myAgent = tracking_batch.TrackingBatch(
    token=token, 
    dataframe=df,
    period="2020-01-01",
    product_id_column_name="product_id",
    client_id_column_name="client_id",
    score_value_column_name="score_value",
    score_group_column_name="score_group",
    score_cluster_column_name="score_cluster",
    name="Ejecución Uno", 
    is_test=True)

a = myAgent.execute(batch_size=2502)
print(len(a))
b = 10


