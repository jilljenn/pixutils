from pixutils.airtable import make_request, lookup_challenges
from collections import Counter, defaultdict

competences = {}
titles = {}
response = make_request('/Compétences', {'fields': ['Sous-domaine', 'Titre']})
for entry in response['records']:
    competences[entry['id']] = entry['fields']['Sous-domaine']
    titles[entry['fields']['Sous-domaine']] = entry['fields']['Titre']

knowledge = defaultdict(lambda: defaultdict(set))
acquix = lookup_challenges('')
for competence, level, skill in acquix:
    knowledge[competences[competence]][level].add(skill)

for competence in sorted(knowledge):
    print('#', competence, titles[competence])
    for level in sorted(knowledge[competence]):
        nb_skills = len(knowledge[competence][level])
        print('Level {} : 40 pix pour {} acquix donc {:.2f} pix par skill, ex. {}'.format(level, nb_skills, 40 / nb_skills, sorted(list(knowledge[competence][level]))[:5]))