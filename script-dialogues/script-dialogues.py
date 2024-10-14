import json
import os
from openai import OpenAI

# Your OpenAI API key (replace with your actual key)
client = OpenAI(
    api_key="",
)

# Load the JSON file
with open('input.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if "mSource" not in data or "mTerms" not in data["mSource"]:
    print("Помилка: ключі 'mSource' або 'mTerms' не знайдено!")

terms = data["mSource"]["mTerms"]["Array"]

# Prepare a list to hold the translated data
translated_data = []

# Process the data
# Assuming data is a list of strings, alternating between ID and text
for index, item in enumerate(terms):

#    if index >= 10:
#        break

    id_line = item["Term"]
    text_line = item["Languages"]["Array"][0]

    print(f"Translating text for ID: {id_line}")

    # Call the OpenAI API to translate text_line from Russian to Ukrainian
    try:
        chat_completion = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'system', 'content': 'Translate the following text from Russian to Ukrainian. Maintain the tone, style, and nuances of the original text. Preserve the atmosphere and emotional depth typical of Disco Elysium. Adapt slang and idiomatic expressions to sound natural in Ukrainian. If a direct translation results in an awkward phrase, feel free to rephrase it to fit the context. Use correct Ukrainian grammar and stylistic conventions. Think twice before translation'},
                {'role': 'user', 'content': text_line}
            ],
            temperature=0.7,
        )

        translated_text = chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        translated_text = "[Translation Error]"

    # Append the id_line and the translated text to the translated_data
    data["mSource"]["mTerms"]["Array"][index]["Languages"]["Array"][0] = translated_text

    # Save the translated data back to a JSON file
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

print("Translation completed. Translated data saved to 'output.json'.")
