from pixutils.airtable import make_request, lookup_challenges, update_challenges
from collections import Counter, defaultdict
import json

competences = {}
titles = {}
response = make_request('/Compétences', {'fields': ['Sous-domaine', 'Titre']})
for entry in response['records']:
    competences[entry['id']] = entry['fields']['Sous-domaine']
    titles[entry['fields']['Sous-domaine']] = entry['fields']['Titre']

knowledge = defaultdict(lambda: defaultdict(set))
challengesOfCompetence = defaultdict(set)
acquix, comp_chall = lookup_challenges('')
for competence, level, skill in acquix:
    knowledge[competences[competence]][level].add(skill)

for competence in sorted(knowledge):
    print('#', competence, titles[competence])
    for level in sorted(knowledge[competence]):
        nb_skills = len(knowledge[competence][level])
        print('Level {} : 8 pix pour {} acquix donc {:.2f} pix par skill, ex. {}'.format(level, nb_skills, 8 / nb_skills, sorted(list(knowledge[competence][level]))[:5]))

for competence_id, challenge_id in comp_chall:
    challengesOfCompetence[competence_id].add(challenge_id)

for competence_id in challengesOfCompetence:
    print(competence_id, list(challengesOfCompetence[competence_id])[:5])

keys = {
    # competence: (competence_id, course_id)
    '1.1': ('recsvLz0W2ShyfD63', 'recNPB7dTNt5krlMA'),
    '1.2': ('recIkYm646lrGvLNT', 'recAY0W7xurA11OLZ'),
    '1.3': ('recNv8qhaY887jQb2', 'recR9yCEqgedB0LYQ'),
    '3.1': ('recOdC9UDVJbAXHAm', 'rec43mpMIR5dUzdjh'),
    '3.2': ('recbDTF8KwupqkeZ6', 'recVtTay20uxEqubF'),
    '3.3': ('recHmIWG6D0huq6Kx', 'recRKkLdx99wfl3qs'),
    '3.4': ('rece6jYwH4WEw549z', 'recTMfUJzFaNiUt64'),
    '4.1': ('rec6rHqas39zvLZep', 'recO1qH39C0IfggLZ'), # 4.1 Sécuriser
    '4.2': ('recofJCxg0NqTqTdP', 'recrJ90Sbrotzkb7x'), # 4.2
    '4.3': ('recfr0ax8XrfvJ3ER', 'recRlIVstCemVM8jE'), # 4.3
    '5.1': ('recIhdrmCuEmCDAzj', 'rec5gEPqhxYjz15eI'), # 5.1
    '5.2': ('recudHE5Omrr10qrx', 'recfLYUy8fYlcyAsl'), # 5.2
}

first_challenge = {}

courses = make_request('/Tests?view=Tests de positionnement', {'fields': ['Nom', 'Épreuves']})
print(json.dumps(courses, indent=4))
for course in courses['records']:
    # print(course['fields'])
    first_challenge[course['id']] = course['fields']['Épreuves'][-1]
    print('Test', course['fields']['Nom'], len(course['fields']['Épreuves']), 'épreuves')
    print('Premier challenge', first_challenge[course['id']])
    print()

for competence in keys:
    competence_id, course_id = keys[competence]
    challenges = challengesOfCompetence[competence_id]
    print('Test', competence, len(challenges), 'épreuves')
    challenges.remove(first_challenge[course_id])
    challenges = [first_challenge[course_id]] + list(challenges)
    print(len(challenges), 'épreuves dont', challenges[0])
    update_challenges(course_id, challenges)
