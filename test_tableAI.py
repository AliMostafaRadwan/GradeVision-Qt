# from transformers import pipeline
import pandas as pd

# # prepare table + question
# data = {"Image": ["1685501.tif", "1685502.tif", "1685503.tif"], "Grade": ["87", "53", "69"]}
# table = pd.DataFrame.from_dict(data)
# question = "what is the grade of 1685501.tif ?"

df = pd.read_csv('test.csv')
# print(df)
# print(table)

# # pipeline model
# # Note: you must to install torch-scatter first.
# tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")

# # result

# print(tqa(table=df, query=question)['cells'][0])
# #53



"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai

genai.configure(api_key="AIzaSyByx3JEeVjLSoBI1NytJI27ElksQBwtpJ0")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


prompt_parts = ["what the score of this paper and where is the wrong answers 1685500", df.to_string()]

response = model.generate_content(prompt_parts)
print(response.text)