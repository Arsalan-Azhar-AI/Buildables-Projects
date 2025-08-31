from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
class ChatImplementation:
  def __init__(self):
    self.client = Groq(api_key=api_key,)
    self.chat_history=[]
  def get_response(self):
    while True:
      user_input=input("Enter the prompts or type exit to quit!\n")
      if user_input=="exit":
        print("Good Bye")
        break
      try:
        messages=[{'role':'system','content':"You are a helpful Assitance. Give the detail answer."}]
        messages.extend(self.chat_history)
        messages.append({'role':'user','content':user_input})

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=200,
        )

        llm_response=chat_completion.choices[0].message.content
        self.chat_history.append({'role':'user','content':user_input})
        self.chat_history.append({'role':'assistant','content':llm_response})
        if len(self.chat_history)>20:
          self.chat_history=self.chat_history[-10:]
        print("\n")
        print("*****************************************")
        print(llm_response)
        print("*****************************************")
      except Exception as e:
        print(f"Error{str(e)}")

chatbot=ChatImplementation()
chatbot.get_response()