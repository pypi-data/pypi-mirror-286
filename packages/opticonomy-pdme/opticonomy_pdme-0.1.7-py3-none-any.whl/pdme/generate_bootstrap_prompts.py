import random

def create_bootstrap_prompts(template: str, seeds: dict, num: int = 1):
    def fill_template(template, seeds):
        prompt = template
        for key, values in seeds.items():
            chosen_values = random.sample(values, template.count(key))
            for value in chosen_values:
                prompt = prompt.replace(key, value, 1)
        return prompt

    bootstrap_prompts = [fill_template(template, seeds) for _ in range(num)]
    return bootstrap_prompts