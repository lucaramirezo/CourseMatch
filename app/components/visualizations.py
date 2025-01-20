import altair as alt

def plot_language_trends(trends_data):
    """
    Crea un gráfico de barras para mostrar lenguajes en auge y declive.

    :param trends_data: DataFrame con las tendencias de lenguajes.
    :return: Gráfico de Altair.
    """
    chart = alt.Chart(trends_data).transform_calculate(
        category='datum.Growth > 0 ? "Auge" : "Declive"'
    ).mark_bar().encode(
        x=alt.X('Growth:Q', title="Crecimiento"),
        y=alt.Y('Language:N', sort='-x', title="Lenguaje"),
        color=alt.Color('category:N', scale=alt.Scale(domain=["Auge", "Declive"], range=["green", "red"])),
        tooltip=['Language', 'Growth']
    ).properties(
        title="Lenguajes en Auge y Declive",
        width=700,
        height=400
    )
    return chart


def plot_learning_methods(methods_data):
    """
    Crea un gráfico de barras horizontales para mostrar métodos de aprendizaje populares.

    :param methods_data: DataFrame con los métodos de aprendizaje.
    :return: Gráfico de Altair.
    """
    chart = alt.Chart(methods_data).mark_bar().encode(
        x=alt.X('TotalFrequency:Q', title="Frecuencia"),
        y=alt.Y('Method:N', sort='-x', title="Método de Aprendizaje"),
        color=alt.Color('TotalFrequency:Q', scale=alt.Scale(scheme='blues')),
        tooltip=['Method', 'TotalFrequency']
    ).properties(
        title="Métodos de Aprendizaje Más Populares",
        width=700,
        height=400
    )
    return chart


def plot_role_language_scatter(roles_df):
    """
    Crea un gráfico de dispersión para mostrar roles y su relación con lenguajes clave.

    :param roles_df: DataFrame limpio con columnas 'DevType', 'Languages', 'AvgPositiveGrowth', 'AvgNegativeGrowth'.
    :return: Gráfico de Altair.
    """
    # Expandir lenguajes separados por comas
    expanded_df = roles_df.assign(
        Language=roles_df['Languages'].str.split(', ')
    ).explode('Language')

    # Crear gráfico de dispersión
    scatter_plot = alt.Chart(expanded_df).mark_circle(size=60).encode(
        x=alt.X('AvgPositiveGrowth:Q', title='Crecimiento Promedio Positivo'),
        y=alt.Y('DevType:N', title='Rol', sort=None),
        color=alt.Color('Language:N', legend=alt.Legend(title='Lenguajes')),
        tooltip=['DevType', 'Language', 'AvgPositiveGrowth', 'AvgNegativeGrowth']
    ).properties(
        title='Relación entre Roles y Lenguajes Clave',
        width=800,
        height=400
    )
    return scatter_plot


def plot_role_language_bubble(roles_df):
    """
    Genera una matriz de burbujas que muestra la relación entre roles y lenguajes clave.

    :param roles_df: DataFrame limpio con columnas 'DevType', 'Languages', 'AvgPositiveGrowth', 'AvgNegativeGrowth'.
    :return: Gráfico de Altair.
    """
    # Expandir lenguajes separados por comas
    expanded_df = roles_df.assign(
        Language=roles_df['Languages'].str.split(', ')
    ).explode('Language')

    # Crear gráfico de burbujas
    bubble_chart = alt.Chart(expanded_df).mark_circle().encode(
        x=alt.X('AvgPositiveGrowth:Q', title='Crecimiento Promedio Positivo'),
        y=alt.Y('DevType:N', title='Rol', sort=None),
        size=alt.Size('AvgPositiveGrowth:Q', title='Crecimiento Positivo'),
        color=alt.Color('AvgPositiveGrowth:Q', scale=alt.Scale(scheme='reds'), title='Crecimiento'),
        tooltip=['DevType', 'Language', 'AvgPositiveGrowth', 'AvgNegativeGrowth']
    ).properties(
        title='Matriz de Burbujas: Relación entre Roles y Lenguajes',
        width=800,
        height=600
    )
    return bubble_chart


def plot_role_language_stacked_bar(roles_df):
    """
    Genera un gráfico de barras apiladas que muestra la relación entre roles y lenguajes clave,
    limitado a los primeros 5 roles por crecimiento positivo promedio.

    :param roles_df: DataFrame con columnas 'DevType', 'Languages', 'AvgPositiveGrowth'.
    :return: Gráfico de Altair.
    """
    # Expandir lenguajes separados por comas
    expanded_df = roles_df.assign(
        Language=roles_df['Languages'].str.split(', ')
    ).explode('Language')

    # Filtrar para mostrar solo los primeros 5 roles diferentes
    top_roles = expanded_df.groupby('DevType')['AvgPositiveGrowth'].mean().sort_values(ascending=False).head(5).index
    filtered_df = expanded_df[expanded_df['DevType'].isin(top_roles)]

    # Crear el gráfico de barras apiladas
    bar_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('sum(AvgPositiveGrowth):Q', title='Crecimiento Total por Lenguaje'),
        y=alt.Y('DevType:N', title='Rol', sort='-x'),
        color=alt.Color('Language:N', legend=alt.Legend(title='Lenguajes')),
        tooltip=['DevType', 'Language', 'AvgPositiveGrowth']
    ).properties(
        title='Relación entre los 5 Roles Principales y Lenguajes Clave (Barras Apiladas)',
        width=800,
        height=400
    )
    return bar_chart



def plot_language_popularity_vs_growth(trends_data):
    """
    Crea un gráfico de dispersión que relaciona popularidad y crecimiento de lenguajes.

    :param trends_data: DataFrame con tendencias de lenguajes.
    :return: Gráfico de Altair.
    """
    chart = alt.Chart(trends_data).mark_circle(size=100).encode(
        x=alt.X('Frequency_Used:Q', title="Popularidad (Veces Trabajado)"),
        y=alt.Y('Growth:Q', title="Crecimiento"),
        color=alt.Color('Growth:Q', scale=alt.Scale(scheme='viridis'), title="Crecimiento"),
        tooltip=['Language', 'Frequency_Used', 'Growth']
    ).properties(
        title="Popularidad vs Crecimiento de Lenguajes",
        width=700,
        height=400
    )
    return chart
