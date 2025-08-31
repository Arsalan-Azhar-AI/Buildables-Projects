from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
class SimpleChatBot:
    def __init__(self, api_key: str):
        """Initialize the chatbot with OpenAI API key"""
        self.client = Groq(api_key=api_key,)
        self.conversation_history = []
        self.system_prompt = "You are a helpful AI assistant."
    def get_response(self, user_input: str) -> str:
 
        messages = [{"role": "system", "content": self.system_prompt}]
        
        messages.extend(self.conversation_history)
  
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
        
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})

            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return ai_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
def get_system_prompt_presets():
    """Return predefined system prompts"""
    return {
        "1": ("Professional Assistant", "You are a helpful, professional, friendly, and knowledgeable AI assistant."),
        "2": ("Creative Writer", "You are a creative writing assistant. Help with brainstorming, storytelling, and creative projects. Be imaginative and inspiring."),
        "3": ("Technical Expert", "You are a technical expert. Provide detailed, accurate technical information with step-by-step explanations."),
    }

def main():
    print("🤖 Welcome to the Simple ChatBot!")
    print("="*40)

    if not api_key:
        print("❌ API key is required to continue.Please Add your api key in env file")
        return

    try:
        chatbot = SimpleChatBot(api_key)
        print("✅ Chatbot initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        return

    print(f"\n💡 Current system prompt: {chatbot.system_prompt}")
    while True:
        user_input=input("\n You:  ").strip()
        if not user_input:
            continue
        if user_input=="exit":
            print("👋 Good Bye!")
            break
        elif user_input=="system":
            print("\n System Prompt Options.")
            prompts=get_system_prompt_presets()
            for key,(name,_) in prompts.items():
                print(f"{key}: {name}")
            choice=input("Select your System Prompt.").strip()
            if choice in prompts:
                name, prompt = prompts[choice]
                chatbot.system_prompt=prompt
                chatbot.conversation_history = [] 
                print("System Prompt Updated!")


            else:
                found = False
                for key, (name, prompt) in prompts.items():
                    if choice.lower() == name.lower():
                        chatbot.system_prompt = prompt
                        chatbot.conversation_history = []
                        print(f"✅ System Prompt Updated to: {name}!")
                        found = True
                        break
                if not found:
                    print("❌ Invalid choice.")
        else:
            print(f"\n💡 Current system prompt: {chatbot.system_prompt}")
            print("\n🤖 Assistant:", end=" ")
            response = chatbot.get_response(user_input)
            print(response)

if __name__=="__main__":
    main()




