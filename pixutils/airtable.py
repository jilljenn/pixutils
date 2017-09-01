from settings import AIRTABLE_BASE, AIRTABLE_API_KEY
from collections import defaultdict
import requests
import json
import os


# AirTable Reference:
# https://support.airtable.com/hc/en-us/articles/203255215-Formula-Field-Reference#logical_operators

def make_request(request, extra_params={}):
    r = requests.get('https://api.airtable.com/v0/%s%s'
                     % (AIRTABLE_BASE, request),
                     headers={'Authorization': 'Bearer %s'
                              % AIRTABLE_API_KEY},
                     params={**extra_params})  # 'maxRecords': 5,
    return r.json()


def lookup_challenges(query, offset=None):
    params = {'filterByFormula':
            ('AND(' +
             (r"""FIND("{}", {{Consigne}}), """.format(query) if query else '') +
             r"""OR({Statut} = 'validé', {Statut} = 'validé sans test', {Statut} = 'pré-validé'), """
             # r"""FIND("@publi4", {acquis}), """
             r"""NOT({acquis} = BLANK())"""
             # r"""{Type d'épreuve} = 'QROC'"""
             ')'),
         'fields': ['Record ID', 'Consigne', 'Statut', 'acquis', 'competences']}
    if offset is not None:
        params['offset'] = offset
    response = make_request('/Épreuves', params)
    acquix = set()
    comp_chall = set()
    if 'records' in response:
        print(len(response['records']), 'results')
        if 'offset' in response:
            print(response['offset'])
            next_acquix, next_comp_chall = lookup_challenges(query, offset=response['offset'])
            acquix.update(next_acquix)
            comp_chall.update(next_comp_chall)
        for entry in response['records']:
            challenge_id = entry['fields']['Record ID']
            acquis = entry['fields'].get('acquis')
            competence = entry['fields']['competences'][0]
            comp_chall.add((competence, challenge_id))
            for skill in acquis:
                level = int(skill[-1])
                acquix.add((competence, level, skill))
    else:
        print(response)
    return sorted(acquix), comp_chall

def update_challenges(adaptive_course_id, challenge_ids):
    new_test = {'fields': {'Épreuves': list(challenge_ids)[::-1]}}
    r = requests.patch('https://api.airtable.com/v0/{}/Tests/%s'.format(AIRTABLE_BASE) % adaptive_course_id, headers={
        'Authorization': 'Bearer {}'.format(AIRTABLE_API_KEY), 'Content-type': 'application/json'}, data=json.dumps(new_test))
    print(r.json())
