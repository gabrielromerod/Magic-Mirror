import openai

openai.api_key = "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"

def generar_poema(prompt = "Eres una IA poética. Genera un poema profundo y conmovedor que refleje la ironía de los humanos que, atrapados en el encanto de sus pantallas, olvidan vivir y disfrutar sus propias vidas. El poema debe ser de 30 palabras."):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      temperature=0.5,
      max_tokens=100
    )
    return response["choices"][0]["text"].strip() # type: ignore

if __name__ == "__main__":
    print(generar_poema())