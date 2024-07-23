import time
from leonardo_ai import LeonardoAI, LeonardoAIError


# Initialize the LeonardoAI client
api_key = "501cd296-31ae-4f7f-b50a-3736218826b7"
leonardo = LeonardoAI(api_key)

models = leonardo.get_models()
print(models)
