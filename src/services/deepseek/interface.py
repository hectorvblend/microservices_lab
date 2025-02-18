#!/usr/bin/env python3
'''
This file includes the interface to the DeepSeek API.
'''

import requests
from src.settings import DEEPSEEK_HOST, DEEPSEEK_PORT, DEEPSEEK_MODEL

class DeepSeek:
    def __init__(self):
        self.endpoint = f'http://{DEEPSEEK_HOST}:{DEEPSEEK_PORT}/api/generate'
        self.stream = False
        self.model = DEEPSEEK_MODEL

    def pre_prompt_message(self):
        return '''
            Responde únicamente en texto plano, sin etiquetas como <think> o <reasoning>,
            sin caracteres de formato especial, sin comillas innecesarias y sin escapes.
            No agregues prefijos ni explicaciones, solo devuelve la respuesta de forma directa al siguiente texto:

            '''

    def generate(self, prompt: str):
        """
        This method sends a POST request to the DeepSeek model with the given prompt.

        It takes a string as prompt, adds a pre-prompt message and posts it to the DeepSeek model.
        The response is returned as a request object.

        Args:
            prompt (str): The string to be used as prompt to the DeepSeek model.

        Returns:
            requests.Response: The response from the DeepSeek model.
        """
        response = requests.post(
            self.endpoint,
            json={'prompt': f'{self.pre_prompt_message()} {prompt}', 'model': self.model, 'stream': self.stream})
        return response