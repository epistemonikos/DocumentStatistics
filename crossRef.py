#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

good_writer = csv.writer(open('good_results', 'w'), dialect='excel-tab')
bad_writer = csv.writer(open('bad_results', 'w'), dialect='excel-tab')
for cita in open('citas.txt'):
    doi = citation_lookup(cita)
    if doi:
        good_writer.writerow([doi, cita])
    else:
        bad_writer.writerow([doi, cita])

def citation_lookup(citation):
    return requests.get('http://api.crossref.org/works', params={
        'query': citation.strip()
    }).json().get('message', {}).get('items', [{'DOI' : False}])[0]['DOI']
