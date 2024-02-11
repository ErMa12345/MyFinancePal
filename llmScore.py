import openai
from emotionDetection import EmotionalRiskCalculator

api_key = "key"

def score_response(original_response):
    try:
        calculator = EmotionalRiskCalculator()
        score = calculator.process_free_response_question(response)
        # Add your own GPT input to the original response
        gpt_input = f"Score: {score}\n%. Original Response: {original_response}\n"

        # Make a request to ChatGPT-3.5 API for scoring
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are an AI assistant analyzing responses from investors. Given an initial nlp_score percentage,  Your goal is to score their responses out of 100 percent based on the degree of informativeness and emotional content and the score that the nlp model gave. 
                  The higher the percent the more informative it is. Investors were asked to provide explanations or justifications for their investment decisions.
                   """},
                {"role": "user", "content": gpt_input},
                {"role": "assistant", "content": "Generate with a maximum of 3 tokens the percentage value"}
            ],
            api_key=api_key
        )

        # Extract the GPT-generated response
        gpt_generated_response = response.choices[0].text.strip()

        return gpt_generated_response

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return {"error": error_message}

# Example usage
response_example = "I am confident in this stock because I have researched different articles"
result = score_response(response_example)
print("GPT Score:", result)

