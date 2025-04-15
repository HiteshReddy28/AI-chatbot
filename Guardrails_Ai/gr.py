#DetectPII,Gibberish Text, LogicCheck,ToxicLanguage,ResponsivenessCheck,GroundedAIHallucination
from guardrails import Guard
from guardrails import Guard
from guardrails.hub import DetectPII, GibberishText, ToxicLanguage, ResponsivenessCheck, GroundedAIHallucination, LogicCheck

# -----------------------------------
# Input Guardrails
# -----------------------------------
input_guard = Guard(name="input_guardrails")

# Use only the input validators provided
input_guard.use(DetectPII(on_fail="exception"))
input_guard.use(GibberishText(on_fail="exception"))

def validate_input(text):
    try:
        input_guard.validate(text)
    except Exception as e:
        raise Exception(f"Input validation failed: {e}")
    return text

# -----------------------------------
# Output Guardrails
# -----------------------------------
output_guard = Guard(name="output_guardrails")

# Use only the output validators provided
output_guard.use(LogicCheck(on_fail="exception"))
output_guard.use(ToxicLanguage(on_fail="exception"))
output_guard.use(ResponsivenessCheck(on_fail="exception"))
#output_guard.use(GroundedAIHallucination(on_fail="exception", quant=True))

def validate_output(text):
    try:
        output_guard.validate(text)
    except Exception as e:
        raise Exception(f"Output validation failed: {e}")
    return text
