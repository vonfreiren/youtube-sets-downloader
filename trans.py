import openai
openai.api_key = ""

filename = 'Avicii Tomorrowland 2011 (Full Video Set)'
prompt = "What is the name of the song in filename: "+filename+ "?"


completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000)


print(completion.choices[0]['text'])
