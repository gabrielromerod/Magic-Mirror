import openai
import json

openai.api_key = "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"

def generar_video_prompt():
    base_prompt = "Eres una IA creadora. Genera un escenario para un video que represente un momento bello de la vida humana. El video tendrá 120 frames y cada descripción corresponderá a un momento específico en el video."

    all_video_prompts = {}

    # Genera 50 prompts de video
    for prompt_number in range(1, 3):
        # Genera una serie de momentos para el video
        video_prompts = {}
        for frame in [0, 30, 60, 90, 120]:
            prompt = base_prompt + f" Describe lo que sucede en el frame {frame}."
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0.5,
                max_tokens=50
            )
            video_prompts[str(frame)] = response["choices"][0]["text"].strip() # type: ignore

        all_video_prompts[f'prompt_{prompt_number}'] = video_prompts

    # Guarda todos los prompts de video en un solo archivo JSON
    with open('all_video_prompts.json', 'w', encoding='utf-8') as f:
        json.dump(all_video_prompts, f)

# Genera los prompts de video
generar_video_prompt()
