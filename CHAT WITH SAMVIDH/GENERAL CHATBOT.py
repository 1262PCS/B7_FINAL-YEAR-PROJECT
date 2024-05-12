from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained(
    "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
)

def get_prompt(instruction: str, history: list[str] | None = None) -> str:
    system = "You are an AI assistant that gives helpful answers. You answer the question in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n"
    if history is not None:
        prompt += f"This is the conversation history: {''.join(history)}. Now answer the question: "
    prompt += f"{instruction}\n\n### Response:\n"
    return prompt

def chat_interface():
    print("Hi, I am SAMVIDH, I'll be happy to help with your queries:")
    print("SAMVIDH: Please tell me how can I assist you!")

    history = []  # Initialize conversation history

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("SAMVIDH: Exiting!!!!.")
            break

        question = user_input
        prompt = get_prompt(question, history)  # Include conversation history in prompt
        answer = ""
        print("SAMVIDH: ", end='')

        for word in llm(prompt, stream=True):
            print(word, end="", flush=True)
            answer += word
        print()

        # Add the answer to conversation history
        history.append(answer)

# Example usage
chat_interface()

