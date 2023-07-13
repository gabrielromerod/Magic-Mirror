import openai

openai.api_key = "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"

def generar_poema(emotion_percentages):
    # Ordenamos las emociones de mayor a menor porcentaje
    sorted_emotions = sorted(emotion_percentages.items(), key=lambda item: item[1], reverse=True)
    
    # Creamos el prompt a partir de las emociones
    prompt = f"Eres una IA poética. Genera un poema que refleje las siguientes emociones: {sorted_emotions[0][0]}({sorted_emotions[0][1]}%), {sorted_emotions[1][0]}({sorted_emotions[1][1]}%), {sorted_emotions[2][0]}({sorted_emotions[2][1]}%). El poema debe ser de 35 palabras."
    
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "Eres una IA poética."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']
