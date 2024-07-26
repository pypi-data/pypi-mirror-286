import logging
from transformers import PreTrainedModel
import torch
import math
from itertools import product
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDME:
    def __init__(self, eval_model, test_model):
        """Initialize the PDME class with evaluation and test models."""
        try:
            self.eval_model = eval_model
            self.test_model, self.test_tokenizer = test_model
        except Exception as e:
            logger.error(f"Error initializing PDME: {e}")

    def probability_of_labels(self, prompt, max_tokens, labels):
        try:
            # Generate text using the evaluation model
            generated_text = self.generate_text(self.eval_model, prompt, max_new_tokens=max_tokens)
            logger.info(f"Generated text: {generated_text}")
            
            # Get log probabilities using the evaluation model
            log_probs = self.get_log_probs_langchain(self.eval_model, prompt + generated_text)
            
            if log_probs is None or len(log_probs) == 0:
                logger.error("Failed to get log probabilities")
                return [1/len(labels)] * len(labels)  # Return uniform distribution if we fail

            # logger.info(f"Log probabilities: {log_probs}")

            # Convert log probabilities to logits
            def logprob_to_logit(lp):
                return lp - math.log(1.0 - math.exp(lp))

            # Convert logits back to probabilities
            def logit_to_prob(l):
                e_l = math.exp(l)
                return e_l / (1.0 + e_l)

            label_probabilities = []
            for label in labels:
                # Find the log probability for this label
                label_logprob = next((lp['logprob'] for lp in log_probs if lp['token'].strip() == label.strip()), None)
                
                if label_logprob is not None:
                    curr_logit = logprob_to_logit(label_logprob)
                    
                    # Apply temperature scaling
                    temperature = 1.0  # Reduced from 3.0 to make differences more pronounced
                    curr_logit /= temperature
                    
                    curr_prob = logit_to_prob(curr_logit)
                    label_probabilities.append(curr_prob)
                    logger.info(f"Label: {label}, LogProb: {label_logprob}, Logit: {curr_logit}, Prob: {curr_prob}")
                else:
                    label_probabilities.append(0)
                    logger.info(f"Label: {label} not found in log probabilities")

            # Normalize the probabilities to sum to 100%
            total_prob = sum(label_probabilities)
            if total_prob > 0:
                label_probabilities = [prob / total_prob for prob in label_probabilities]
            else:
                label_probabilities = [1/len(labels)] * len(labels)  # Uniform distribution if all probs are 0

            logger.info(f"Final normalized probabilities: {label_probabilities}")
            return label_probabilities
        except Exception as e:
            logger.error(f"Error in probability_of_labels: {e}")
            return [1/len(labels)] * len(labels)  # Return uniform distribution on error

    def calculate_perplexity(self, log_probs):
        n = len(log_probs)
        log_probs_sum = torch.sum(log_probs).item() if isinstance(log_probs, torch.Tensor) else sum(log_probs)
        perplexity = math.exp(-log_probs_sum / n)
        return perplexity

    def get_token_logprobs(self, logprobs):
        """Return the log probability of the first token and the perplexity for the given response tokens."""
        try:
            if logprobs is None:
                return 0, float('inf')  # Returning 0 logprob and infinity perplexity for null logprobs

            if len(logprobs) > 0:
                first_token_logprob = logprobs[0]['logprob']
                token_logprobs = [lp['logprob'] for lp in logprobs]
                log_probs_tensor = torch.tensor(token_logprobs)
                perplexity = self.calculate_perplexity(log_probs_tensor)
                return first_token_logprob, perplexity
            else:
                return 0, float('inf')
        except Exception as e:
            logger.error(f"Error in get_token_logprobs: {e}")
            return 0, float('inf')
        
    def get_log_probs_langchain(self, llm, text):
        """Get log probabilities from LangChain model given a text input."""
        try:
            bound_llm = llm.bind(logprobs=True)
            response = bound_llm.invoke(text)
            log_probs = response.response_metadata.get("logprobs", {}).get("content", [])
            return log_probs
        except Exception as e:
            logger.error(f"Error get_log_probs_langchain: {e}")
            return None


    def get_text_langchain(self, llm, prompt):
        """Get generated text from LangChain model."""
        try:
            response = llm(prompt)
            generated_text = response.content
            return generated_text
        except Exception as e:
            logger.error(f"Error getting text: {e}")
            return None
        
    def generate_text(self, model, prompt, max_new_tokens=1000):
        """Generate text using the given model."""
        try:
            if isinstance(model, PreTrainedModel):
                logger.info("Generating prompt for Hugging Face model")
                tokenizer = self.test_tokenizer

                inputs = tokenizer(prompt, return_tensors='pt')
                # Get the model's maximum new tokens
                model_max_length = model.config.max_length if hasattr(model.config, 'max_length') else 1024  # Default to 1024 if not set
                generation_length = min(max_new_tokens, model_max_length)

                generated_ids = model.generate(**inputs, max_new_tokens=generation_length)
                generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
                return generated_text
            else:
                logger.info("Generating prompt for OpenAI / LangChain model")
                generated_text = self.get_text_langchain(model, prompt)
                return generated_text
        except Exception as e:
            logger.error(f"generate_text: {e}")
            return None

    def generate_bootstrap_prompt(self, template, seeds, num=3, prompt_type='coding'):
        """
        Generate bootstrap prompts using the provided template and seeds.
        
        Args:
        template (str): The template string for the prompt.
        seeds (dict): A dictionary of seed categories and their corresponding values.
        num (int): The number of prompts to generate.
        prompt_type (str): The type of prompt to generate ('coding' or 'storytelling').
        
        Returns:
        list: A list of generated prompts.
        """
        prompts = []
        prompt_counter = 0
        
        if prompt_type == 'coding':
            # Coding prompt generation
            languages = seeds.get("<language>", [])
            seed_list = seeds.get("<seed>", [])
            
            for lang in languages:
                for i in range(len(seed_list)):
                    for j in range(i + 1, len(seed_list)):
                        if len(prompts) >= num:
                            break
                        seed1 = seed_list[i]
                        seed2 = seed_list[j]
                        prompt = template.replace("{lang}", lang).replace("{seed1}", seed1).replace("{seed2}", seed2)
                        prompt_counter += 1
                        logger.info(f"Bootstrap prompt [{prompt_counter}]: {prompt}")
                        prompts.append(prompt)
                    if len(prompts) >= num:
                        break
                if len(prompts) >= num:
                    break
        
        elif prompt_type == 'storytelling':
            # Storytelling prompt generation
            seed_categories = list(seeds.keys())
            
            while len(prompts) < num:
                seed_values = [random.choice(seeds[category]) for category in seed_categories]
                prompt = template.format(**dict(zip(seed_categories, seed_values)))
                prompt_counter += 1
                logger.info(f"Bootstrap prompt [{prompt_counter}]: {prompt}")
                prompts.append(prompt)
        
        else:
            raise ValueError("Invalid prompt_type. Choose 'coding' or 'storytelling'.")
        
        return prompts

    def create_coding_bootstrap_prompt(self, template, seeds, num=3):
        """Create bootstrap prompts using the provided template and seeds."""
        prompts = []
        languages = seeds["<language>"]
        seed_list = seeds["<seed>"]
        
        prompt_counter = 0
        for lang in languages:
            for i in range(len(seed_list)):
                for j in range(i + 1, len(seed_list)):
                    if len(prompts) >= num:
                        break
                    seed1 = seed_list[i]
                    seed2 = seed_list[j]
                    prompt = template.replace("<language>", lang).replace("<seed>", f"{seed1}, {seed2}")
                    prompt_counter += 1
                    logger.info(f"Bootstrap prompt [{prompt_counter}]: {prompt}")
                    prompts.append(prompt)
        return prompts
    
    def generate_prompt_from_template(self, template, seeds, num=1, prompt_type="synopsis"):
        """Generate prompts either as a synopsis or using a template."""
        if prompt_type == "synopsis":
            return [self.generate_bootstrap_prompt(*seeds)]
        else:
            return self.create_coding_bootstrap_prompt(template, seeds, num)
        
    def generate_question_prompt(self, bootstrap_prompt):
        """Generate a question prompt using the bootstrap prompt."""
        try:
            question_prompt, _ = self.generate_text(self.eval_model, bootstrap_prompt)
            logger.info(f"Generated question prompt: {question_prompt}")
            return question_prompt
        except Exception as e:
            logger.error(f"Error generating question prompt: {e}")
            return ""

    def get_model_response(self, question_prompt):
        """Get the response from the test model for the given question prompt."""
        try:
            response, logprobs = self.generate_text(self.test_model, question_prompt)
            return response, logprobs
        except Exception as e:
            logger.error(f"Error getting model response: {e}")
            return None, None
    
    def compare_logprobs_simple(self, response1, response2):
        """Compare log probabilities of two responses."""
        try:
            response1_logprob, response1_perplexity = self.get_token_logprobs(response1[1], response1[0], self.test_tokenizer)
            response2_logprob, response2_perplexity = self.get_token_logprobs(response2[1], response2[0], self.test_tokenizer)

            response1_reversed_logprob, response1_reversed_perplexity = self.get_token_logprobs(response1[1], response2[0], self.test_tokenizer)
            response2_reversed_logprob, response2_reversed_perplexity = self.get_token_logprobs(response2[1], response1[0], self.test_tokenizer)

            logger.info(f"Evaluation model log probability: {response1_logprob}")
            logger.info(f"Test model log probability: {response2_logprob}")
            logger.info(f"Evaluation model reversed log probability: {response1_reversed_logprob}")
            logger.info(f"Test model reversed log probability: {response2_reversed_logprob}")
            logger.info(f"Evaluation model perplexity: {response1_perplexity}")
            logger.info(f"Test model model perplexity: {response2_perplexity}")
            prob1_better = (response1_logprob + response2_reversed_logprob) / 2
            prob2_better = (response2_logprob + response1_reversed_logprob) / 2

            if prob1_better > prob2_better:
                return [{'model': 'evaluation', 'rank': 1}, {'model': 'test', 'rank': 2}]
            else:
                return [{'model': 'evaluation', 'rank': 2}, {'model': 'test', 'rank': 1}]
        except Exception as e:
            logger.error(f"Error comparing logprobs: {e}")
            return [{'model': 'evaluation', 'rank': 'unknown'}, {'model': 'test', 'rank': 'unknown'}]
    
    def compare_logprob_simple(self, log_prob1, log_prob2):
        """Compare log probabilities of two responses and rank them."""
        try:
            logger.info(f"Evaluation model total log probability: {log_prob1}")
            logger.info(f"Test model total log probability: {log_prob2}")

            if log_prob1 > log_prob2:
                return [{'model': 'evaluation', 'rank': 1}, {'model': 'test', 'rank': 2}]
            else:
                return [{'model': 'evaluation', 'rank': 2}, {'model': 'test', 'rank': 1}]
        except Exception as e:
            logger.error(f"Error comparing logprobs: {e}")
            return [{'model': 'evaluation', 'rank': 'unknown'}, {'model': 'test', 'rank': 'unknown'}]

    def compare_responses(self, question, response1, response2):
        """Compare responses of two models."""
        try:
            return self.compare_logprobs(response1, response2)
        except Exception as e:
            logger.error(f"Error comparing responses: {e}")
            return [{'model': 'evaluation', 'rank': 'unknown'}, {'model': 'test', 'rank': 'unknown'}]

    def evaluate_with_seeds(self, seed_1, seed_2, seed_3, seed_4):
        """Evaluate the models using the given seeds."""
        try:
            bootstrap_prompt = self.generate_bootstrap_prompt(seed_1, seed_2, seed_3, seed_4)
            logger.info(f"Bootstrap prompt: {bootstrap_prompt}")
            question_prompt = self.generate_question_prompt(bootstrap_prompt)
            eval_response, eval_logprobs = self.generate_text(self.eval_model, question_prompt)
            test_response, test_logprobs = self.get_model_response(question_prompt)
            comparison = self.compare_responses(question_prompt, (eval_response, eval_logprobs), (test_response, test_logprobs))
            return comparison
        except Exception as e:
            logger.error(f"Error during evaluation: {e}")
            return []

    def evaluate(self, item, eval_response, test_response, eval_model_name, test_model_name):
        try:
            # Create the comparison prompt
            comparison_prompt = f"This is the question: {item} This is model 1 response: {eval_response}. This is model 2 response: {test_response}. The best model is model"
            
            # Use probability_of_labels function
            labels = [" 1", " 2"]  # Space before numbers to match token boundaries
            max_tokens = 1  # We only need one token for the answer
            
            logger.info("Calculating label probabilities...")
            label_probabilities = self.probability_of_labels(comparison_prompt, max_tokens, labels)
            
            # Determine the result based on probabilities
            if label_probabilities[0] > label_probabilities[1]:
                result = f"'{eval_model_name}' is better"
            elif label_probabilities[0] < label_probabilities[1]:
                result = f"'{test_model_name}' is better"
            else:
                result = "Both models perform equally"
            
            logger.info(f"Probability for '{eval_model_name}': {label_probabilities[0]}")
            logger.info(f"Probability for '{test_model_name}': {label_probabilities[1]}")
            logger.info(f"Result: {result}")
            
            return result, label_probabilities
        
        except Exception as e:
            logger.error(f"An error occurred during evaluation: {str(e)}")
            return None, None