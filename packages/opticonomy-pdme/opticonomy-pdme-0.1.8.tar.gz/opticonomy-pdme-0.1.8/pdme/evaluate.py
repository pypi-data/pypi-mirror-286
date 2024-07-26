import math
import json
from collections import defaultdict
import pandas as pd

class pdme_llm:
    """
    A class to interact with language models for evaluation and ELO ranking computation.

    Attributes:
        client (object): The client object for the language model API.
        model_name (str): The name of the model to use.
        is_chat (bool): Indicates if the model is a chat-based model.

    Methods:
        evaluate(prompt, labels): Evaluates the given prompt and returns label probabilities.
        generate(input, max_tokens, logprobs=5): Generates a response from the model.
        probability_of_labels(response, labels): Computes the probability of given labels from the model response.
        compute_online_elo(battles, calibration_model, K=4, SCALE=400, BASE=10, INIT_RATING=1000): Computes ELO rankings based on model battles.
    """

    def __init__(self, client, model_name, is_chat=False):
        """
        Initializes the pdme_llm object.

        Args:
            client (object): The client object for the language model API.
            model_name (str): The name of the model to use.
            is_chat (bool, optional): Indicates if the model is a chat-based model. Defaults to False.
        """
        self.client = client
        self.model_name = model_name
        self.is_chat = is_chat

    def evaluate(self, prompt, labels):
        """
        Evaluates the given prompt and returns label probabilities.

        Args:
            prompt (str): The prompt to be evaluated.
            labels (list): The list of labels to evaluate.

        Returns:
            list: A list of probabilities corresponding to the labels.
        """
        response = self.generate(prompt, 1)
        label_probabilities = self.probability_of_labels(response, labels)
        return label_probabilities

    def generate(self, input, max_tokens, logprobs=5):
        """
        Generates a response from the model.

        Args:
            input (str): The input prompt or messages for the model.
            max_tokens (int): The maximum number of tokens to generate.
            logprobs (int, optional): The number of log probabilities to return. Defaults to 5.

        Returns:
            object: The response from the model.
        """
        if self.is_chat:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=input,
                max_tokens=max_tokens,
                logprobs=True,
                top_logprobs=logprobs,
            )
        else:
            response = self.client.completions.create(
                model=self.model_name,
                prompt=input,
                max_tokens=max_tokens,
                logprobs=logprobs,
            )
        return response

    def probability_of_labels(self, response, labels):
        """
        Computes the probability of given labels from the model response.

        Args:
            response (object): The response from the model.
            labels (list): The list of labels to compute probabilities for.

        Returns:
            list: A list of probabilities corresponding to the labels.
        """
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

    def compute_online_elo(self, battles, calibration_model, K=4, SCALE=400, BASE=10, INIT_RATING=1000):
        """
        Computes ELO rankings based on model battles.

        Args:
            battles (DataFrame): A DataFrame containing model battles with columns ['Model 1', 'Model 2', 'Winner'].
            calibration_model (str): The model to calibrate the ELO scores to.
            K (int, optional): The K-factor for ELO computation. Defaults to 4.
            SCALE (int, optional): The scale factor for ELO computation. Defaults to 400.
            BASE (int, optional): The base for ELO computation. Defaults to 10.
            INIT_RATING (int, optional): The initial rating for models. Defaults to 1000.

        Returns:
            DataFrame: A DataFrame containing models and their computed ELO rankings.
        """
        rating = defaultdict(lambda: INIT_RATING)

        for model_a, model_b, winner in battles[['Model 1', 'Model 2', 'Winner']].itertuples(index=False):
            ra = rating[model_a]
            rb = rating[model_b]
            ea = 1 / (1 + BASE ** ((rb - ra) / SCALE))
            eb = 1 / (1 + BASE ** ((ra - rb) / SCALE))
            if winner == "Model 1":
                sa = 1
            elif winner == "Model 2":
                sa = 0
            elif winner == "tie" or winner == "tie (bothbad)":
                sa = 0.5
            else:
                raise Exception(f"unexpected vote {winner}")
            rating[model_a] += K * (sa - ea)
            rating[model_b] += K * (1 - sa - eb)

        # Calibrate the specified model to 800
        delta = (800 - rating[calibration_model])
        for model in battles["Model 1"].unique():
            rating[model] += delta

        elo_df = pd.DataFrame(list(rating.items()), columns=['model_name', 'elo_ranking'])
        elo_df = elo_df.sort_values(by='elo_ranking', ascending=False).reset_index(drop=True)

        return elo_df
