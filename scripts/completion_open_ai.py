import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def completion(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=500,
    temperature=0
    )

    return response.choices[0].text

print(completion("What is the name of president of the unites state"))
