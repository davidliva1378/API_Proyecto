import pandas as pd

# Carga de datasets
df = pd.read_csv("Datasets/movies_dataset_sumario.csv", low_memory=False)
# Convertir la columna 'release_date' a datetime, manejando errores
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
cast_df = pd.read_csv("Datasets/cast_desanidado.csv")  # Dataset de actores desanidado
movies_df = pd.read_csv("Datasets/movies_dataset_sumario.csv")  # Dataset de películas (atencion para la funcion 5 de actores)
directores_df = pd.read_csv("Datasets/directores_desanidado.csv", low_memory=False) # Dataset de directores(atencion para la funcion 6 de actores)


#FUNCION 1

# Diccionario para convertir los meses en español a números
meses_espanol = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}

def cantidad_filmaciones_mes(mes: str) -> str:
    """
    Devuelve la cantidad de películas estrenadas en el mes ingresado.

    Args:
        mes (str): Nombre del mes en español.

    Returns:
        str: Mensaje indicando la cantidad de películas estrenadas.
    """
    # Convertir el nombre del mes al número correspondiente
    mes = mes.lower()
    if mes not in meses_espanol:
        return "Mes ingresado no válido. Por favor ingresa un mes en español."

    numero_mes = meses_espanol[mes]

    # Filtrar las películas estrenadas en el mes correspondiente
    filmaciones_en_mes = df[df["release_date"].dt.month == numero_mes]

    # Obtener la cantidad de películas
    cantidad = filmaciones_en_mes.shape[0]

    # Retornar el mensaje
    return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}."

#FUNCION 2

# Diccionario para convertir días en español a números
dias_espanol = {
    'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
    'viernes': 4, 'sábado': 5, 'domingo': 6
}

def cantidad_filmaciones_dia(dia: str) -> str:
    """
    Devuelve la cantidad de películas estrenadas en el día ingresado.

    Args:
        dia (str): Nombre del día en español.

    Returns:
        str: Mensaje indicando la cantidad de películas estrenadas.
    """
    # Convertir el día al número correspondiente
    dia = dia.lower()
    if dia not in dias_espanol:
        return "Día ingresado no válido. Por favor ingresa un día en español."

    numero_dia = dias_espanol[dia]

    # Filtrar las filas donde release_date no es nulo
    df_valid = df.dropna(subset=['release_date'])

    # Filtrar las películas estrenadas en el día correspondiente
    filmaciones_en_dia = df_valid[df_valid['release_date'].dt.weekday == numero_dia]

    # Obtener la cantidad de películas
    cantidad = filmaciones_en_dia.shape[0]

    # Retornar el mensaje
    return f"{cantidad} cantidad de películas fueron estrenadas en los días {dia.capitalize()}."

#FUNCION 3

def score_titulo(titulo_de_la_filmación: str) -> str:
    """
    Devuelve el título, año de estreno y score de una filmación según su título.

    Args:
        titulo_de_la_filmación (str): Título de la filmación.

    Returns:
        str: Mensaje con el título, año de estreno y score.
    """
    # Buscar el título en el dataframe, ignorando mayúsculas y minúsculas
    titulo = df[df['title'].str.lower() == titulo_de_la_filmación.lower()]

    if titulo.empty:
        return "No se encontró ninguna filmación con ese título."

    # Obtener la primera coincidencia
    resultado = titulo.iloc[0]

    # Obtener el año de estreno si la fecha es válida
    año_estreno = (
        resultado['release_date'].year
        if pd.notnull(resultado['release_date'])
        else "No disponible"
    )

    # Obtener el score
    score = resultado['vote_average'] if 'vote_average' in resultado else "No disponible"

    # Retornar el mensaje
    return (
        f"La película '{resultado['title']}' fue estrenada en el año {año_estreno} "
        f"con un score/popularidad de {score}."
    )

#FUNCION 4

def votos_titulo(titulo_de_la_filmación: str) -> str:
    """
    Devuelve el título, cantidad de votos y promedio de votaciones de una filmación.

    Args:
        titulo_de_la_filmación (str): Título de la filmación.

    Returns:
        str: Mensaje con el título, cantidad de votos y promedio,
             o una advertencia si no cumple con el mínimo de 2000 votos.
    """
    # Buscar el título en el dataframe, ignorando mayúsculas y minúsculas
    titulo = df[df['title'].str.lower() == titulo_de_la_filmación.lower()]

    if titulo.empty:
        return "No se encontró ninguna filmación con ese título."

    # Obtener la primera coincidencia
    resultado = titulo.iloc[0]

    # Verificar si cumple con el mínimo de 2000 votos
    if resultado['vote_count'] < 2000:
        return f"La película '{resultado['title']}' no cumple con el mínimo de 2000 votos."

    # Obtener la cantidad de votos y el promedio
    cantidad_votos = int(resultado['vote_count'])
    promedio_votos = resultado['vote_average']

    # Obtener el año de estreno si la fecha es válida
    año_estreno = (
        resultado['release_date'].year
        if pd.notnull(resultado['release_date'])
        else "No disponible"
    )

    # Retornar el mensaje
    return (
        f"La película '{resultado['title']}' fue estrenada en el año {año_estreno}. "
        f"La misma cuenta con un total de {cantidad_votos} valoraciones, "
        f"con un promedio de {promedio_votos}."
    )

#FUNCION 5

def get_actor(nombre_actor: str) -> str:
    """
    Devuelve el éxito de un actor medido a través del retorno total,
    la cantidad de películas en las que ha participado y el promedio de retorno.

    Args:
        nombre_actor (str): Nombre del actor.

    Returns:
        str: Mensaje con la cantidad de filmaciones, retorno total y promedio de retorno.
    """
    # Filtrar las películas en las que el actor ha participado
    peliculas_actor = cast_df[cast_df['actor_name'].str.lower() == nombre_actor.lower()]

    if peliculas_actor.empty:
        return f"No se encontraron participaciones para el actor {nombre_actor}."

    # Combinar con el dataset de películas para obtener información del retorno
    peliculas_actor = peliculas_actor.merge(
        movies_df, left_on='movie_id', right_on='id', how='inner'
    )

    # Reemplazar valores nulos en la columna 'return' por 0
    peliculas_actor['return'] = peliculas_actor['return'].fillna(0)

    # Calcular cantidad de películas, retorno total y promedio de retorno
    cantidad_peliculas = peliculas_actor.shape[0]
    retorno_total = peliculas_actor['return'].sum()
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0

    # Retornar el mensaje formateado
    return (
        f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, "
        f"el mismo ha conseguido un retorno de {retorno_total:.2f} con un promedio de {promedio_retorno:.2f} por filmación."
    )

#FUNCION 6

def get_director(nombre_director: str) -> str:
    """
    Devuelve el éxito de un director medido a través del retorno total,
    junto con el nombre, fecha de lanzamiento, retorno individual, costo y ganancia de cada película.

    Args:
        nombre_director (str): Nombre del director.

    Returns:
        str: Detalle del retorno total y las películas asociadas al director.
    """
    # Filtrar las películas dirigidas por el director
    peliculas_director = directores_df[
        (directores_df['crew_name'].str.lower() == nombre_director.lower()) &
        (directores_df['job'] == 'Director')
    ]

    if peliculas_director.empty:
        return f"No se encontraron películas para el director {nombre_director}."

    # Relacionar con el dataset de películas para obtener datos de budget, revenue, etc.
    peliculas_director = peliculas_director.merge(
        movies_df, left_on='movie_id', right_on='id', how='inner'
    )

    # Reemplazar valores nulos en las columnas necesarias
    peliculas_director['return'] = peliculas_director['return'].fillna(0)
    peliculas_director['budget'] = peliculas_director['budget'].fillna(0)
    peliculas_director['revenue'] = peliculas_director['revenue'].fillna(0)

    # Calcular el retorno total del director
    retorno_total = peliculas_director['return'].sum()

    # Crear una lista con el detalle de cada película
    detalle_peliculas = []
    for _, row in peliculas_director.iterrows():
        nombre_pelicula = row['title']
        fecha_lanzamiento = row['release_date']
        retorno_individual = row['return']
        costo = row['budget']
        ganancia = row['revenue'] - row['budget']

        detalle_peliculas.append(
            f"Película: {nombre_pelicula}, Fecha de lanzamiento: {fecha_lanzamiento}, "
            f"Retorno: {retorno_individual:.2f}, Costo: ${costo:,.2f}, Ganancia: ${ganancia:,.2f}"
        )

    # Combinar el mensaje final
    detalle_peliculas_str = "\n".join(detalle_peliculas)
    return (
        f"El director {nombre_director} tiene un retorno total de {retorno_total:.2f}.\n"
        f"Detalle de sus películas:\n{detalle_peliculas_str}"
    )
