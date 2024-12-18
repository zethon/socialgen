from openai import OpenAI

def get_quotes():
  with open('apikey.data', 'r') as file:
      openai_api_key = file.read()

  client = OpenAI(
    api_key=openai_api_key
  )

  QUERY = """
  Write 3 topical and thoughtful quotes that are about 10-20 words long each,
  separate each quote with the | character, and each quote should be about 
  any one or more of the following topics: life, love, happiness, success, 
  family, dogs, cats, butterflies, soft kisses, boobies.
  """

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "user", "content": QUERY},
    ]
  )

  print(completion.choices[0].message.content)

  # split the quotes by the | character
  return completion.choices[0].message.content.split('|')
