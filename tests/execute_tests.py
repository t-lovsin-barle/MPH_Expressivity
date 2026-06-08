from src.evaluate import evaluate_on_BREC, evaluate_on_other

results_BREC = evaluate_on_BREC()

results_other = evaluate_on_other()

print(results_BREC)
print('-----------------------')
print(results_other)