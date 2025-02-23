"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requerimientos son los siguientes:
    
    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo espacio
      entre palabra y palabra.
    """
    # Leer el archivo usando pd.read_fwf para obtener cada línea como un registro
    df_lines = pd.read_fwf("files/input/clusters_report.txt", header=None, names=["line"])
    
    # Localizar la línea separadora (la primera que comienza con '-' luego de limpiar espacios)
    dash_index = df_lines[df_lines["line"].str.strip().str.startswith("-")].index[0]
    
    # Seleccionar las líneas de datos que siguen a la línea separadora y eliminar líneas vacías
    data = df_lines.loc[dash_index+1:].copy()
    data = data[data["line"].str.strip() != ""].reset_index(drop=True)
    
    # Marcar las líneas que inician con un dígito (indicando el inicio de un nuevo registro)
    data["is_new"] = data["line"].str.strip().str.match(r"^\d")
    # Crear un grupo acumulativo para cada registro
    data["group"] = data["is_new"].cumsum()
    
    # Concatenar las líneas de cada grupo en un solo string
    grouped = data.groupby("group")["line"].apply(lambda x: " ".join(x.str.strip())).reset_index(drop=True)
    
    # Procesar cada registro para extraer las columnas deseadas
    records = []
    for record in grouped:
        parts = record.split()
        # La primera parte es el cluster, la segunda la cantidad de palabras clave
        cluster = int(parts[0])
        cantidad = int(parts[1])
        
        # La tercera parte contiene el porcentaje; puede venir seguido de un token '%' o ya incluirlo.
        porcentaje_token = parts[2]
        if porcentaje_token.endswith("%"):
            porcentaje = float(porcentaje_token.replace("%", "").replace(",", "."))
            kw_start = 3
        else:
            # Si el siguiente token es '%' se omite
            if parts[3] == "%":
                porcentaje = float(porcentaje_token.replace(",", "."))
                kw_start = 4
            else:
                porcentaje = float(porcentaje_token.replace(",", "."))
                kw_start = 3
        
        # El resto del registro corresponde a las palabras clave
        keywords = " ".join(parts[kw_start:])
        # Eliminar punto final si lo hubiera
        if keywords.endswith("."):
            keywords = keywords[:-1]
        # Asegurar que cada coma sea seguida de un único espacio: dividir y rearmar
        keywords = ", ".join(token.strip() for token in keywords.split(",") if token.strip())
        
        records.append([cluster, cantidad, porcentaje, keywords])
    
    # Crear el DataFrame con los nombres de columna solicitados
    df = pd.DataFrame(records, columns=[
        "cluster", 
        "cantidad_de_palabras_clave", 
        "porcentaje_de_palabras_clave", 
        "principales_palabras_clave"
    ])
    # Asegurar que los nombres de las columnas estén en minúsculas y con guiones bajos
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    return df

if __name__ == '__main__':
    df = pregunta_01()
    print(df)
