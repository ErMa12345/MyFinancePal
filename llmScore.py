import openai

# Set your OpenAI API key as an environment variable
api_key = "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"

def score_response(original_response):
    try:
        score = 1
        gpt_input = f"NLP Score: {score}\n%. Original Response: {original_response}\n"

        # Make a request to ChatGPT-3.5 API for scoring
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are an AI assistant analyzing responses from investors. Given an initial nlp_score percentage, Your goal is to score their responses out of 100 based on the degree of informativeness and emotional content and the score that the nlp model gave. The higher the number the more informative it is. Investors were asked to provide explanations or justifications for their investment decisions. Highly take into account the specificity of the response and the original nlp score given"""},
                {"role": "user", "content": gpt_input},
                {"role": "assistant", "content": "Generate a percentage with maximum 3 tokens"}
            ],
            max_tokens = 100,
            api_key=api_key
        )

        # Extract the GPT-generated response
        gpt_generated_response = response.choices[0].message['content'].strip()

        words = gpt_generated_response.split()
        print(words)
        for word in words:
            try:
                # Remove percentage sign if present
                if "%" in word:
                    word = word.replace("%", "")
                number = float(word)
                return int(number) if number.is_integer() else number
            except ValueError:
                continue
        return score

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return {"error": error_message}

# Example usage
response_example = "Goo goo gaa gaa"
result = score_response(response_example)
print(result)
