import openai
from tools.emotionDetection import EmotionalRiskCalculator

# Set your OpenAI API key as an environment variable
api_key = "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"

def score_response(original_response):
    try:
        calculator = EmotionalRiskCalculator()
        score = calculator.process_free_response_question(original_response)

        #score = 1

        gpt_input = f"NLP Score: {score}\n%. Original Response: {original_response}\n"

        # Make a request to ChatGPT-3.5 API for scoring
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are an AI assistant analyzing responses from investors. Your goal is to score their responses out of 100 based on the degree of informativeness and emotional content and the score that the nlp model gave. The higher the number the more informative it is. Investors were asked to provide explanations or justifications for their investment decisions. List out your score and the NLP score and provide an explanation on the next line. Highly take into account the specificity of the response and the original nlp score given"""},
                {"role": "user", "content": gpt_input},
                {"role": "assistant", "content": "Generate a percentage with maximum 3 tokens"}
            ],
            max_tokens = 100,
            api_key=api_key
        )

        # Extract the GPT-generated response
        gpt_generated_response = response.choices[0].message['content'].strip()
        return gpt_generated_response

        # words = gpt_generated_response.split()
        # print(words)
        # for word in words:
        #     try:
        #         # Remove percentage sign if present
        #         if "%" in word:
        #             word = word.replace("%", "")
        #         number = float(word)
        #         return int(number) if number.is_integer() else number
        #     except ValueError:
        #         continue
        # return score

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return {"error": error_message}

# Example usage
response_example = "I selected this particular stock, ABC Corp, for several reasons. Firstly, after conducting thorough research on its financial statements, I observed consistent revenue growth over the past few year of 1000 percent. Indicating a strong and stable financial performance. Additionally, the company has a low debt-to-equity ratio of 0.98, signifying a healthy balance sheet and reduced financial risk."
result = score_response(response_example)

