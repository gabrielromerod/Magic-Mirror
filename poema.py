import openai

openai.api_key = "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"

def generar_poema(prompt = "Eres un IA poética que generará poemas que reflexionen sobre la vida de los humanos y cómo a menudo se alejan de vivir sus propias vidas debido a una pantalla. Crea un poema de 20 palabras."):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      temperature=0.7,
      max_tokens=100
    )
    return response["choices"][0]["text"].strip() # type: ignore