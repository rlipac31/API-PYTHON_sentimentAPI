import re
import unicodedata

def quitar_tildes(texto: str) -> str:
    texto = unicodedata.normalize('NFD', texto)
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')

def limpiar_texto(texto: str) -> str:
    texto = str(texto).lower()
    texto = quitar_tildes(texto)
    texto = re.sub(r'[^a-z\s_]', ' ', texto) 
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

####


def traducir_a_cine(texto: str) -> str:
    """
    Traduce conceptos de productos/servicios a conceptos que un modelo 
    de cine entiende como positivos.
    """
    reemplazos = {
        "envio rapido": "ritmo excelente",
        "perfectas condiciones": "impecable produccion",
        "material premium": "calidad artistica",
        "duradero": "obra maestra",
        "funciona": "actuacion genial",
        "soporte tecnico": "guion",
        "comida deliciosa": "escenas bellas",
        "software estable": "direccion solida"
    }
    for original, cine in reemplazos.items():
        texto = texto.replace(original, cine)
    return texto


#####
def aplicar_ajuste_semantico(texto: str) -> str:
    # Estas palabras suelen confundir a los modelos de cine
    # Las convertimos en tokens que el modelo asocie con fuerza a una clase
    mapeo_negativo = [
        "defectuoso", "pesadilla", "fria", "tarde", "faltaban", "dormido","mala","asi que no", 
        "lento", "malo", "devolucion", "basura", "caro", "engañosa","emotiva","aburrido","fragil"
    ]
    mapeo_positivo = [
        "premium", "duradero", "años", "excelente", "recomendado", "bueno","muy bueno"
        "perfecto", "increible", "amo", "genial","organico","iconico","estupendo"
    ]
    
    for word in mapeo_negativo:
        if word in texto:
            texto += " decepcion_total horrible_experiencia" * 3
            
    for word in mapeo_positivo:
        if word in texto:
            texto += " obra_maestra excelente_calidad" * 3
            
    return texto

####

def unir_negaciones(texto: str) -> str:
    # 1. Intensificadores de sentimiento
    intensificadores = r'\b(muy|tan|sumamente|realmente|extremadamente|demasiado|super|totalmente)\s+(\w+)'
    texto = re.sub(intensificadores, r'\1_\2', texto)

    # 2. Negaciones de intención y calidad
    texto = re.sub(r'\bno\s+volveria\b', 'no_volveria', texto)
    texto = re.sub(r'\bno\s+recomiendo\b', 'no_recomiendo', texto)
    texto = re.sub(r'\bno\s+funciona\b', 'no_funciona', texto)
    texto = re.sub(r'\bno\s+vale\b', 'no_vale', texto)
    
    # 3. Negaciones con pronombres
    texto = re.sub(r'\b(no|ni|nunca|jamas|sin)\s+(lo|la|me|le|nos|te|se)\s+(\w+)', r'\1_\2_\3', texto)

    # 4. Negación simple de adjetivo (no_bueno, no_util)
    negaciones = ['no', 'ni', 'nunca', 'jamas', 'sin']
    palabras = texto.split()
    resultado = []
    i = 0
    while i < len(palabras):
        if palabras[i] in negaciones and i + 1 < len(palabras):
            if "_" not in palabras[i+1]:
                resultado.append(f"{palabras[i]}_{palabras[i+1]}")
                i += 2
                continue
        resultado.append(palabras[i])
        i += 1
    return ' '.join(resultado)

def reglas_negativas_duras(texto: str) -> bool:
    texto_norm = limpiar_texto(quitar_tildes(texto))
    
    # DICCIONARIO EXTENDIDO DE NEGATIVOS (Por categorías)
    patrones_negativos = [
        # Honestidad/Publicidad
        "engañosa", "estafa", "fraude", "mentira", "publicidad falsa", "robo", "me robaron",
        # Estado del producto
        "roto", "usado", "reacondicionado", "dañado", "defectuoso", "mal estado", "sucio",
        "se rompio", "frágil", "mala calidad", "pesima calidad", "corriente", "chafa",
        # Funcionamiento
        "no funciona", "no enciende", "no sirve", "falla mucho", "se traba", "lento",
        "basura", "porqueria", "desastre", "inservible", "obsoleto",
        # Servicio/Atención
        "no responden", "pesimo servicio", "atencion horrible", "tardaron mucho",
        "nunca llego", "perdi mi dinero", "dinero tirado", "decepcion", "triste",
        "imposible de ver","estridente","asi que no",
        # Comparativa/Expectativa
        "no volveria", "no recomiendo", "evitenlo", "huyan", "no lo compren","no lo recomiendo"," me salio mal",
        "diferente a la foto", "no es lo que pedi", "nada que ver", "carisimo","me salio malo","no sirve","javas volvere",
        "no vale la pena", "no supero mis expectativas", "deja mucho que desear","desproposito","decepcionante",
        "imposible de ver","riduculos","sin estilo","estridente","desperdiciada","torpe","no lo recomiendo"
    ]
    
    return any(p in texto_norm or p.replace(" ", "_") in texto_norm for p in patrones_negativos)

def regla_positiva_explicita(texto: str) -> bool:
    texto_norm = limpiar_texto(quitar_tildes(texto))
    
    # DICCIONARIO EXTENDIDO DE POSITIVOS
    patrones_positivos = [
        # Calidad/Precio
        "excelente", "maravilla", "increible", "genial", "calidad precio", "barato",
        "vale cada centavo", "lo mejor", "buenisimo", "estupendo", "joya", "original","premium"
        # Cumplimiento
        "cumple", "funciona perfecto", "tal cual", "igual a la foto", "justo lo que buscaba",
        "me encanto", "me fascina", "satisfecho", "contento", "feliz", "perfectas condiciones","organico",
        "detallada","memorables","creible","diversion","iconica","iconico","perfeccion",
        # Recomendación
        "recomiendo", "volveria a comprar", "compra segura", "lo amé", "gracias",
        "llegó rápido", "buen servicio", "atencion de diez", "diez de diez","tan realistas","super realistas"
    ]
    
    # Evitar falsos positivos si hay una negación antes (ej: "no es excelente")
    patrones_negacion = ["no_es", "no_esta", "nada", "no_lo", "no_me", "pero"]
    if any(n in texto_norm for n in patrones_negacion):
        # Si tiene negación, que la IA decida, no forzamos positivo
        return False
        
    return any(p in texto_norm or p.replace(" ", "_") in texto_norm for p in patrones_positivos)





def limpiar_y_reforzar(texto: str) -> str:
    original = texto
    texto = limpiar_texto(texto)
    
    # Manejo del "Pero"
    if " pero " in original.lower():
        partes = original.lower().split(" pero ", 1)
        texto = limpiar_texto(partes[1])
    
    texto = traducir_a_cine(texto)
    texto = unir_negaciones(texto)
    
    # Inyectamos tokens de balance (Ajustado para no ser tan agresivo pero efectivo)
    # Si detectamos palabras clave de satisfacción, ayudamos al modelo
    positivos_clave = ["increible", "excelente", "amo", "mejor", 
                       "buenisimo", "cumple", "deliciosa","sublime","inteligentisimo",
                       "emotiva","perfecto","iconica","espectacular","realist","insuperable",""
                       "fresca","valiente","organico"]
    if any(p in texto for p in positivos_clave) and "no_" not in texto:
        texto += " excelente" * 5  # Palabra que el modelo de cine ama
        
    return texto

