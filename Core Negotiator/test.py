from guardrails.hub import GroundedAIHallucination
from guardrails import Guard

guard = Guard().use(GroundedAIHallucination(quant=True))

guard.validate("The capital of France is London.", metadata={
    "query": "What is the capital of France?",
    "reference": "The capital of France is Paris."
}) 

 # Validator fails

guard.validate("The capital of France is Paris.", metadata={
    "query": "What is the capital of France?",
    "reference": "The capital of France is Paris."
})
# Validator passes

# with llm
messages = [{"role":"user", "content":"What is the capital of France?"}]

guard(
  messages=messages,
  model="gpt-4o-mini",
  metadata={
    "query": messages[0]["content"],
    "reference": "The capital of France is Paris."
})

# Validator passes