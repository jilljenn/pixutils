import requests
import json
import os


# AirTable Reference:
# https://support.airtable.com/hc/en-us/articles/203255215-Formula-Field-Reference#logical_operators

def make_request(request, extra_params):
    r = requests.get('https://api.airtable.com/v0/%s%s'
                     % (os.environ['AIRTABLE_BASE'], request),
                     headers={'Authorization': 'Bearer %s'
                              % os.environ['AIRTABLE_API_KEY']},
                     params={'maxRecords': 5, **extra_params})
    return r.json()


def lookup_challenges(query):
    response = make_request(
        '/Épreuves',
        {'filterByFormula':
            (r"""AND(FIND("%s", {Consigne}), """
             r"""{Type d'épreuve} = 'QROC')""" % query),
         'fields': ['Record ID', 'Consigne']})
    for entry in response['records']:
        print('ID:', entry['fields']['Record ID'])
        print(entry['fields']['Consigne'])
        print()
