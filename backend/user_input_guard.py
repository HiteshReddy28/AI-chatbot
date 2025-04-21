from guardrails import Guard, OnFailAction
from guardrails.hub import ProfanityFree, GibberishText

guard = Guard()
guard.name = 'user-input-guard'

guard.use_many(
    ProfanityFree(on_fail=OnFailAction.EXCEPTION),
    GibberishText(on_fail=OnFailAction.EXCEPTION)
)
