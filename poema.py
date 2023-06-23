import openai

openai.api_key = "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"

def generar_poema(emotion_percentages):
    # Ordenamos las emociones de mayor a menor porcentaje
    sorted_emotions = sorted(emotion_percentages.items(), key=lambda item: item[1], reverse=True)
    
    # Creamos el prompt a partir de las emociones
    prompt = f"Eres una IA poética. Genera un poema que refleje las siguientes emociones: {sorted_emotions[0][0]}({sorted_emotions[0][1]}%), {sorted_emotions[1][0]}({sorted_emotions[1][1]}%), {sorted_emotions[2][0]}({sorted_emotions[2][1]}%). El poema debe ser de 35 palabras."
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=200
    )
    return response.choices[0].text.strip()
