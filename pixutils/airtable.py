from settings import AIRTABLE_BASE, AIRTABLE_API_KEY
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
    if 'records' in response:
        print(len(response['records']), 'results')
        if 'offset' in response:
            print(response['offset'])
            acquix.update(lookup_challenges(query, offset=response['offset']))
        for entry in response['records']:
            acquis = entry['fields'].get('acquis')
            competence = entry['fields']['competences'][0]
            for skill in acquis:
                level = int(skill[-1])
                acquix.add((competence, level, skill))
    else:
        print(response)
    return sorted(acquix)
