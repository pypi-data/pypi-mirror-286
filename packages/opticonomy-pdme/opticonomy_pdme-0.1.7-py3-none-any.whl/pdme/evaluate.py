import openai
import math
import json


class pdme_llm:
    def __init__(self, client, model_name, is_chat = False):
        self.client = client
        self.model_name = model_name
        self.is_chat = is_chat

    def evaluate(self, prompt, labels):
        response = self.generate(prompt, 1)
        
        label_probabilities = self.probability_of_labels(response, labels)
        return label_probabilities

    # handles both chat and completions type models
    def generate(self, input, max_tokens, logprobs = 5):
        if self.is_chat:
            response = self.client.chat.completions.create(
                    model=self.model_name,  # You can choose the model you prefer
                    messages=input,
                    max_tokens=max_tokens,  # Limit the response to exactly one token
                    logprobs=True,  # Get the log probabilities of the top tokens
                    top_logprobs = logprobs,
                )
        else:
            response = self.client.completions.create(
                    model=self.model_name,  # You can choose the model you prefer
                    prompt=input,
                    max_tokens=max_tokens,  # Limit the response to exactly one token
                    logprobs=logprobs,  # Get the log probabilities of the top tokens
                )
        return response
    
    def probability_of_labels(self, response, labels):
        #response = response.json()
        response = json.loads(response.json())

        logprobs = response["choices"][0]["logprobs"]["top_logprobs"][0]

        # Convert log probabilities to logits (using some math tricks)
        def logprob_to_logit(lp):
            return lp - math.log(1.0 - math.exp(lp))

        # Convert logits back to probabilities
        def logit_to_prob(l):
            e_l = math.exp(l)
            return e_l / (1.0 + e_l)

        label_probabilities = []
        for label in labels:
            curr_logprob = logprobs.get(label, None)
            curr_logit = logprob_to_logit(curr_logprob) if curr_logprob is not None else 0

            # Apply temperature scaling
            temperature = 3.0  # Adjust as needed. Higher values make predictions less extreme.
            curr_logit /= temperature

            curr_prob = logit_to_prob(curr_logit)

            label_probabilities.append(curr_prob)

        # Normalize the probabilities to sum to 100%
        total_prob = sum(label_probabilities)

        label_probabilities = [prob / total_prob for prob in label_probabilities]

        return label_probabilities