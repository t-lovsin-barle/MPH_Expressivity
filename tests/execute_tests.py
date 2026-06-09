from src.evaluate import evaluate_on_BREC, evaluate_on_other

results_BREC = evaluate_on_BREC(filter_1='degree', Rips=True)
print(results_BREC)
print('-----------------------')


results_other = evaluate_on_other(filter_1='degree', Rips=True)
print(results_other)