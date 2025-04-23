from guardrails import Guard, OnFailAction
from guardrails.hub import ProfanityFree, LogicCheck

guard = Guard()
guard.name = 'assistant-output-guard'

guard.use_many(
    ProfanityFree(on_fail=OnFailAction.EXCEPTION),
    LogicCheck(on_fail=OnFailAction.EXCEPTION)
)
