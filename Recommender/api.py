#!/usr/bin/env python3
import logging
import re
import secrets
from typing import Dict, Any, Optional

import requests
from requests.exceptions import HTTPError

from Recommender import CONFIG, save_config

LOGGER = logging.getLogger(__name__)
BASE_AUTH_URL = 'https://myanimelist.net/v1/oauth2'
BASE_API_URL = 'https://api.myanimelist.net/v2'


def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


def user_authorization() -> bool:
    if not CONFIG['Client ID']:
        return False
    valid = False
    if CONFIG['Access Token']:
        valid = authorization_check()
        if not valid:
            valid = refresh_token()
    if valid:
        return True
    LOGGER.info('Generating a Token')
    code_verifier = code_challenge = get_new_code_verifier()
    authorization_url = f"{BASE_AUTH_URL}/authorize?response_type=code&client_id={CONFIG['Client ID']}&code_challenge={code_challenge}"
    print(f"Follow this URL:\n{authorization_url}")
    response_url = input('Input the response URL >> ')
    reg = re.findall(r'^.*?code=(.*?)(?:&state=(.*)|)$', response_url)[0]
    try:
        body = {
            'client_id': CONFIG['Client ID'],
            'code': reg[0],
            'code_verifier': code_verifier,
            'grant_type': 'authorization_code'
        }
        response = requests.post(f"{BASE_AUTH_URL}/token", data=body)
        response.raise_for_status()
        token_data = response.json()
        CONFIG['Access Token'] = token_data['access_token']
        CONFIG['Refresh Token'] = token_data['refresh_token']
        save_config()
        return True
    except HTTPError as err:
        LOGGER.error(f"Error: {err}")
        LOGGER.debug(f"Request Headers: {err.request.headers}")
    return False


def authorization_check() -> bool:
    LOGGER.info('Validating Token')
    try:
        response = requests.get(f"{BASE_API_URL}/users/@me",
                                headers={'Authorization': f"Bearer {CONFIG['Access Token']}"})
        response.raise_for_status()
        return True
    except HTTPError as err:
        LOGGER.error(f"Error: {err}")
        LOGGER.debug(f"Request Headers: {err.request.headers}")
    return False


def refresh_token() -> bool:
    LOGGER.info('Refreshing Token')
    try:
        body = {
            'client_id': CONFIG['Client ID'],
            'grant_type': 'refresh_token',
            'refresh_token': CONFIG['Refresh Token']
        }
        response = requests.post(f"{BASE_AUTH_URL}/token", data=body)
        response.raise_for_status()
        token_data = response.json()
        CONFIG['Access Token'] = token_data['access_token']
        CONFIG['Refresh Token'] = token_data['refresh_token']
        save_config()
        return True
    except HTTPError as err:
        LOGGER.error(f"Error: {err}")
        LOGGER.debug(f"Request Headers: {err.request.headers}")
    return False


def get_watchlist(username: Optional[str] = None) -> Dict[int, Any]:
    LOGGER.info(f"Retrieving {username or '@me'}'s Watchlist")
    watchlist = {}
    try:
        response = requests.get(f"{BASE_API_URL}/users/{username or '@me'}/animelist",
                                params={'sort': 'list_score', 'limit': 1000},
                                headers={'Authorization': f"Bearer {CONFIG['Access Token']}"})
        response.raise_for_status()
        data = response.json()
        for item in data['data']:
            watchlist[item['node']['id']] = {
                'title': item['node']['title']
            }
    except HTTPError as err:
        LOGGER.error(f"Error: {err}")
        LOGGER.debug(f"Request Headers: {err.request.headers}")
    return watchlist


def get_anime(mal_id: int) -> Optional[Dict[str, Any]]:
    LOGGER.debug(f"Retrieving anime with ID: {mal_id}")
    anime = None
    try:
        response = requests.get(f"{BASE_API_URL}/anime/{mal_id}",
                                params={'fields': ','.join(
                                    ['id', 'title', 'alternative_titles', 'mean', 'rank', 'popularity',
                                     'num_list_users', 'num_scoring_users', 'media_type', 'recommendations',
                                     'statistics'])},
                                headers={'Authorization': f"Bearer {CONFIG['Access Token']}"})
        response.raise_for_status()
        data = response.json()
        anime = {
            'id': data['id'],
            'title': data['title'],
            'alternative_titles': data['alternative_titles'],
            'mean': data['mean'] if 'mean' in data else 0,
            'rank': data['rank'] if 'rank' in data else 0,
            'popularity': data['popularity'],
            'media_type': data['media_type'],
            'recommendations': [{'id': x['node']['id'], 'title': x['node']['title'], 'recs': x['num_recommendations']}
                                for x in data['recommendations']],
            'stats': data['statistics']
        }
        anime['stats']['num_scoring_users'] = data['num_scoring_users']
    except HTTPError as err:
        LOGGER.error(f"Error: {err}")
        LOGGER.debug(f"Request Headers: {err.request.headers}")
    return anime


def search_anime(name: str, limit: int = 10) -> Optional[Dict[str, Any]]:
    LOGGER.debug(f"Retrieving anime with name: {name}")
    anime = None
    try:
        response = requests.get(f"{BASE_API_URL}/anime",
                                 params={'q': name, 'limit': limit},
                                 headers={'Authorization': f"Bearer {CONFIG['Access Token']}"})
        response.raise_for_status()
        data = response.json()
        LOGGER.info(data)
    except HTTPError as err:
        LOGGER.error(f"Error: {err}")
        LOGGER.debug(f"Request Headers: {err.request.headers}")
    return anime
