from tmdb.settings import TMDB_KEY, TMDB_URL

import json
import requests


def tmdb_request(method, path, params = None):

    url = "{base_uri}{path}".format(base_uri = TMDB_URL, path = path)
        
    api_dict = {'api_key': TMDB_KEY}
    if params:
        params = params.copy()
        params.update(api_dict)
    else:
        params = api_dict

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Connection': 'close'}

    response = requests.request(
        method, url, params = params, 
        data = None,
        headers = headers)

    response.raise_for_status()
    response.encoding = 'utf-8'
    return response.json()