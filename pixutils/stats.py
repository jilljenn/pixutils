from collections import Counter
from slugify import slugify
import pandas as pd
from IPython.display import display


def build_analytics(filename):
    results = {}
    nb_answers = 0
    nb_pass = 0
    with open(filename) as f:
        next(f)  # On saute la première ligne (noms des colonnes)
        for line in f:
            data = line.split(',')
            value = data[1]  # La réponse se trouve en 2e
            result = data[2]  # Le résultat en 3e
            if value != '#ABAND#':
                answer = slugify(value)
                results.setdefault(answer, Counter())[result] += 1
            else:
                nb_pass += 1
            nb_answers += 1
    print(nb_pass, 'abandons')
    print(len(results.keys()), 'réponses distinctes parmi les',
          nb_answers, 'réponses données\n')
    display_cluster(results, results.keys())
    return results


def display_cluster(results, answers, limit=20):
    lines = []
    for answer in sorted(answers, key=lambda
                         answer: -sum(results[answer].values()))[:limit]:
        nb_ok = results[answer]['ok']
        nb_ko = results[answer]['ko']
        total = sum(results[answer].values())
        lines.append([answer, nb_ok, nb_ko, total - nb_ok - nb_ko])
    display(pd.DataFrame(lines, columns=['réponse', 'ok', 'ko', 'aberrants']))
