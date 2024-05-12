import streamlit as st
from ctransformers import AutoModelForCausalLM

# Load the DialoGPT model
llm = AutoModelForCausalLM.from_pretrained("zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf")

def get_prompt(instruction: str, history: list[str] | None = None) -> str:
    system = "You are an AI assistant that gives helpful answers. You answer the question in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n"
    if history is not None:
        prompt += f"This is the conversation history: {''.join(history)}. Now answer the question: "
    prompt += f"{instruction}\n\n### Response:\n"
    return prompt

with st.sidebar:
    st.title('🤗💬 SAMVIDH')
    st.markdown('''
    
    
 ✨ Features &  How to Use 💡:

- Instant Assistance 💬: Get quick and helpful responses to your research questions.
- Conversation History 📚: Easily access past queries and answers for reference.
- Educational Support 🎓: SAMVIDH offers concise answers to enhance your understanding.
- Enter your query in the text input box labeled "You."
- SAMVIDH will provide prompt responses to assist you.


    ''')
    

def main():
    st.title('🤖 SAMVIDH Chat Interface')

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    
    st.write("Please tell me how can I assist you!")

    user_input = st.text_input("YOU:")
    if user_input:
        question = user_input
        prompt = get_prompt(question, st.session_state.conversation_history)  # Include conversation history in prompt
        answer = "SAMVIDH: "

        for word in llm(prompt, stream=True):
            answer += word

        st.write(answer)

        # Add the question and answer to conversation history
        st.session_state.conversation_history.append(f"{question}\n{answer}")

        # Display previous queries and their answers as separate blocks
        st.write("\n\n## Previous Conversations:")
        for idx, entry in enumerate(st.session_state.conversation_history[::-1]):
            query, response = entry.split("\n")
            st.write(f"Previous Query {len(st.session_state.conversation_history)-idx}:", query)
            st.write(f"Previous Answer {len(st.session_state.conversation_history)-idx}:", response)

if __name__ == '__main__':
    main()

