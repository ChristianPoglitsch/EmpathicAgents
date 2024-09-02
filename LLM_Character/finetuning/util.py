def get_formatted_prompt(prompt):
    return f"### Human: {prompt} ### Assistant:"


def print_generated_text(stage, prompt, text1, text2):
    """Print generated text for the given stage."""
    print(f"\n{stage}")
    print(prompt)
    print(text1)
    print("----")
    print(text2)
