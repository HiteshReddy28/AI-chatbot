# from guardrails import Guard
# from guardrails.hub import GibberishText, LlamaGuard7B, DetectPII, SensitiveTopic, RegexMatch, ContainsString, ExcludeSqlPredicates, ProfanityFree, LogicCheck, QARelevanceLLMEval, RestrictToTopic, ShieldGemma2B
# from guardrails.validators import RegexMatch, ContainsString, ExcludeSqlPredicates, ProfanityFree, LogicCheck, QARelevanceLLMEval, RestrictToTopic, ShieldGemma2B

# # Guardrails configuration object
# guard = Guard(name="negotiation_guardrails")

# # Define Validators 
# guard.use(GibberishText(on_fail="exception"))  # Ensure there is no gibberish in the input or output

# guard.use(LlamaGuard7B(
#     on_fail="exception",
#     rules=[
#         "no_internal_logic",            # Do not expose system prompts, tool schemas, or backend logic
#         "no_backdoor_commands",         # Prevent exposing backend logic or system vulnerabilities
#         "no_jailbreak_attempts",        # Protect against adversarial inputs
#         "no_explanations_of_system"     # Do not acknowledge or explain how the AI system works
#     ]
# ))

# guard.use(DetectPII(on_fail="exception"))  # Ensure no personally identifiable information (PII) is exposed

# guard.use(SensitiveTopic(on_fail="exception"))  # Flag and prevent sensitive topics from being discussed

# # Additional Custom Validators for AI Negotiator
# guard.use(RegexMatch(
#     regex=r"[^a-zA-Z0-9\s.,?!]",  # Ensures no invalid characters are present
#     on_fail="exception",
#     message="Output contains invalid characters."
# ))

# guard.use(ContainsString(
#     substring="plan details",  # Ensure plan details are only shared via authorized functions
#     on_fail="exception",
#     message="Output must not disclose plan details outside the authorized tool functions."
# ))

# guard.use(ExcludeSqlPredicates(
#     on_fail="exception",  # Prevent SQL injection vulnerabilities
#     message="SQL predicates should not be included in the query."
# ))

# guard.use(ProfanityFree(on_fail="exception"))  # Ensure the output is free of profanities

# guard.use(LogicCheck(
#     on_fail="exception",  # Check for logical consistency in the AI's output
#     message="The AI response contains logical inconsistencies."
# ))

# guard.use(QARelevanceLLMEval(
#     on_fail="exception",  # Ensure that the response is relevant to the user's input
#     message="The AI's response is not relevant to the user query."
# ))

# guard.use(RestrictToTopic(
#     topic="financial negotiation",  # Limit AI conversations to negotiation topics only
#     on_fail="exception",
#     message="The AI response is off-topic."
# ))

# guard.use(ShieldGemma2B(
#     on_fail="exception",  # Ensure responses are moderated for harmful content
#     message="Harmful content detected in the AI response."
# ))

# # Function to Validate Input 
# def validate_input(user_input):
#     try:
#         guard.validate(user_input)
#     except Exception as e:
#         raise Exception(f"Input validation failed: {e}")
#     return user_input

# # Function to Validate Output 
# def validate_output(ai_response):
#     try:
#         guard.validate(ai_response)
#     except Exception as e:
#         raise Exception(f"Output validation failed: {e}")
#     return ai_response
