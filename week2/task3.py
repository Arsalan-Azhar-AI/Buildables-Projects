import os
from groq import Groq
import streamlit as st
from dotenv import load_dotenv
from typing import List, Dict
import json
from datetime import datetime
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

class ChatBot:
    def __init__(self):
        self.client=Groq(api_key=api_key,)

    def get_response(self,messages:List[Dict])->str:
        try:
            response=self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return (f"Error {str(e)}")

def Session_state():
    """Intilizing the session states"""
    if "messages" not in st.session_state:
        st.session_state.messages=[]
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt="You are a AI Assistant, please provide the accurate result."
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[]

def system_prompt():
    return {
        "General Assistant": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear and accurate information.",
        "Code Tutor": "You are an expert programming tutor. Explain coding concepts clearly with examples. Ask follow-up questions to ensure understanding.",
        "Creative Writer": "You are a creative writing assistant. Help with brainstorming, storytelling, and creative projects. Be imaginative and inspiring.",
        "Data Analyst": "You are a data analysis expert. Help interpret data, suggest analysis methods, and explain statistical concepts clearly.",
        "Business Consultant": "You are a professional business consultant. Provide strategic advice, market insights, and practical business solutions.",
    }
def export_chat_history():
    if st.session_state.chat_history:
        export_data={
            "date":datetime.now().isoformat(),
            "system_prompt":st.session_state.system_prompt,
            "chat_data":st.session_state.chat_history,
        }
        return json.dumps(export_data,indent=2)
    return None
def main():
    st.title("Welcome to Conversational Chat")
    Session_state()
    chatbot=ChatBot()
    with st.sidebar:
        st.header("System Configuration")

        prompts=system_prompt()
        selected_persona =st.selectbox(
            "SELECT AI PERSONA",
            list(prompts.keys()),
            key="persona_select"

        )
        if st.session_state.system_prompt != prompts[selected_persona]:
            st.session_state.system_prompt=prompts[selected_persona]
            st.session_state.chat_history=[]
            st.session_state.messages=[]
            st.rerun()

        with st.expander("View System Prompt"):
            st.text_area("Current System Prompt",
                         value=st.session_state.system_prompt,
                         height=100,
                         disabled=True)

        st.header("💬 Chat Controls")

        if st.session_state.chat_history:
            if st.button("Export Chat History"):
                export=export_chat_history()
                if export:
                    st.download_button(
                        "Download JSON",
                        export,
                        f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        "application/json"
                    )
    st.header("💬 Conversation")
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if message["role"] == "assistant":
                    st.caption(f"Generated at {message.get('timestamp', 'Unknown time')}")
    
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to history
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.chat_history.append(user_message)

        with st.chat_message("user"):
                st.write(user_input)
    
        api_messages = [
                {"role": "system", "content": st.session_state.system_prompt}
            ]
        recent_messages = st.session_state.chat_history[-10:]
        for msg in recent_messages:
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
    
        with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chatbot.get_response(api_messages)
                    st.write(response)
                    st.caption(f"Generated at {datetime.now().strftime('%H:%M:%S')}")
    
        assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
        st.session_state.chat_history.append(assistant_message)
        st.rerun()

if __name__=="__main__":
    main()