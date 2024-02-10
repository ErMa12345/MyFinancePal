from textblob import TextBlob
import nltk
import numpy
from nltk import pos_tag, word_tokenize, ne_chunk
from nltk.corpus import stopwords
from nltk.tree import Tree
from finance_keywords import finance_keywords


class EmotionalRiskCalculator:
    def __init__(self):
        self.scores = []

    def process_free_response_question(self, answer):
        # Tokenize the answer into words
        words = word_tokenize(answer)

        # Remove stopwords
        stop_words = set(stopwords.words("english"))
        words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

        # Part-of-speech tagging
        pos_tags = pos_tag(words)

        # Check for complexity based on the presence of noun phrases
        tree = ne_chunk(pos_tags)
        has_complex_structure = any(isinstance(subtree, Tree) and subtree.label() == 'NP' for subtree in tree)

        # Check for specificity based on the presence of named entities
        named_entities = [chunk for chunk in tree if isinstance(chunk, Tree) and chunk.label() == 'NE']

        numeric_entities = [word for word, pos in pos_tags if pos in ['CD']]
        
        additional_keywords = [word for word in words if word.lower() in finance_keywords]

        # Calculate specificity score
        specificity_score = (len(named_entities) + (3.0 *len(additional_keywords) + 2.0 * len(numeric_entities))) / len(words) if words else 0
       # print("Before: ", specificity_score)

        # Calculate complexity score
        complexity_score = 0.5 if has_complex_structure else 0

        # Set a minimum response length threshold for heavy penalization
        min_response_length = 20  # Adjust the threshold as needed

        # Adjust specificity score based on response length
        if len(words) < min_response_length:
            specificity_score *= 0.01  # Heavily penalize specificity for short responses
        else:
            # Increase specificity score in increments for every increase in 10 words
            length_factor_increment = 0.2  # Adjust the increment factor as needed
            length_factor = 1 + length_factor_increment * (len(words) - min_response_length) // 10
            specificity_score *= length_factor

        #print(len(words))
        #print("After: ", specificity_score)

        # Analyze subjectivity using TextBlob
        blob = TextBlob(answer)
        subjectivity_score = blob.sentiment.subjectivity

        # Define weights for each factor
        weight_specificity = 0.8
        weight_complexity = 0.1
        weight_subjectivity = 0.1

        # Combine scores into an overall score
        overall_score = (weight_specificity * specificity_score) + (weight_complexity * complexity_score) + (weight_subjectivity * subjectivity_score)

        # Ensure the overall score is between 0 and 1
        overall_score = min(overall_score, 1)

        self.scores.append(overall_score)

        return overall_score * 100


    def calculate_emotional_risk_percentile(self):
        # Calculate the total score and convert it to a percentile
        total_score = sum(self.scores)
        percentile = (total_score / (len(self.scores))) * 100  # Assuming a maximum possible score of 5 for each question
        return min(percentile, 100)


# Example usage:
calculator = EmotionalRiskCalculator()


# Process free-response question answers
print("Free Response question answer: ", calculator.process_free_response_question('I am confident in this stock because I have researched different articles'))
print("Free Response question answer 2: ", calculator.process_free_response_question('In a sun-dappled meadow, a mischievous fox with a gleam in its eye dashes playfully, evading the watchful gaze of a loyal dog. With a graceful leap, the fox vaults effortlessly over its canine friend, leaving behind a trail of laughter and friendship under the golden sky.'))
print("Free Response question answer 3: ", calculator.process_free_response_question('I have spent 5 days tracking fundamentals ad researching articles andd talking to professionals. This is an amazong stock andd will go up with the performance of the earninggs calls next week.'))
print("Free Response question answer 4: ", calculator.process_free_response_question('I selected this particular stock, ABC Corp, for several reasons. Firstly, after conducting thorough research on its financial statements, I observed consistent revenue growth over the past few year of 1000 percent. Indicating a strong and stable financial performance. Additionally, the company has a low debt-to-equity ratio of 0.98, signifying a healthy balance sheet and reduced financial risk.'))
print("Free Response question answer 5: ", calculator.process_free_response_question('In the shadows of cyberspace, a cunning scammer orchestrates a devious plan, breaching the digital defenses of Robinhood, the famed trading platform. With deft keystrokes, they manipulate accounts, siphoning wealth from unsuspecting investors. Panic ensues as portfolios vanish into the digital abyss, leaving behind a trail of betrayal and shattered dreams in their wake.'))

# Calculate and print the emotional risk percentile
# emotional_risk_percentile = calculator.calculate_emotional_risk_percentile()
# print(f"Emotional Risk Percentile: {emotional_risk_percentile}")
