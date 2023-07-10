"""
Provide implementation of private Threads API.
"""
import requests
import json
import time
from urllib.parse import quote

from threads.apis.abstract import AbstractThreadsApi
from threads.utils import generate_android_device_id


class PrivateThreadsApi(AbstractThreadsApi):
    """
    Private Threads API implementation.
    """

    INSTAGRAM_API_URL = 'https://i.instagram.com/api/v1'

    def __init__(self, username: str = None, password: str = None):
        """
        Construct the object.

        Arguments:
            username (str): a user's Instagram username.
            password (str): a user's Instagram password.
        """
        super().__init__()

        if username is not None and password is not None:
            self.instagram_api_token = self._get_instagram_api_token()

        self.username = username
        self.password = password

        self.timezone_offset = -14400
        self.android_device_id = generate_android_device_id()

    def _get_instagram_api_token(self):
        """
        Get a token for Instagram API.
        """
        block_version = '5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73'

        parameters_as_string = json.dumps({
            'client_input_params': {
                'password': self.password,
                'contact_point': self.username,
                'device_id': self.android_device_id,
            },
            'server_params': {
                'credential_type': 'password',
                'device_id': self.android_device_id,
            },
        })

        bk_client_context_as_string = json.dumps({
            'bloks_version': block_version,
            'styles_id': 'instagram',
        })

        params = quote(string=parameters_as_string, safe="!~*'()")
        bk_client_context = quote(string=bk_client_context_as_string, safe="!~*'()")

        response = requests.post(
            url=f'{self.INSTAGRAM_API_URL}/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/',
            headers={
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
            data=f'params={params}&bk_client_context={bk_client_context}&bloks_versioning_id={block_version}'
        )

        bearer_key_position = response.text.find('Bearer IGT:2:')
        response_text = response.text[bearer_key_position:]

        backslash_key_position = response_text.find('\\\\')
        token = response_text[13:backslash_key_position]

        return token

    def get_user(self, id: str):
        """
        Get a user.

        Arguments:
            id (int): a user's identifier.
        """
        response = requests.get(
            url=f'{self.INSTAGRAM_API_URL}/users/{id}/info/',
            headers={
                'Authorization': f'Bearer IGT:2:{self.instagram_api_token}',
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        )

        return response.json()

    def search_user(self, query: str):
        """
        Search for a user.

        Arguments:
            query (str): a search query.
        """
        response = requests.get(
            url=f'{self.INSTAGRAM_API_URL}/users/search/?q={query}',
            headers={
                'Authorization': f'Bearer IGT:2:{self.instagram_api_token}',
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        )

        return response.json()

    def get_user_followers(self, id: int):
        """
        Get a user's followers.

        Arguments:
            id (int): a user's identifier.
        """
        response = requests.get(
            url=f'{self.INSTAGRAM_API_URL}/friendships/{id}/followers/',
            headers={
                'Authorization': f'Bearer IGT:2:{self.instagram_api_token}',
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        )

        return response.json()

    def get_user_following(self, id: int):
        """
        Get a user's following.

        Arguments:
            id (int): a user's identifier.
        """
        response = requests.get(
            url=f'{self.INSTAGRAM_API_URL}/friendships/{id}/following/',
            headers={
                'Authorization': f'Bearer IGT:2:{self.instagram_api_token}',
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        )

        return response.json()

    def follow_user(self, id: int):
        """
        Follow a user.

        Arguments:
            id (int): a user's identifier.
        """
        response = requests.post(
            url=f'{self.INSTAGRAM_API_URL}/friendships/create/{id}/',
            headers={
                'Authorization': f'Bearer IGT:2:{self.instagram_api_token}',
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        )

        return response.json()

    def create_thread(self, caption: str):
        """
        Create a thread.

        Arguments:
            caption (str) a thread's caption.
        """
        current_timestamp = time.time()
        user_id = self.get_user_id(username=self.username)

        parameters_as_string = json.dumps({
            'publish_mode': 'text_post',
            'text_post_app_info': '{"reply_control":0}',
            'timezone_offset': str(self.timezone_offset),
            'source_type': '4',
            'caption': caption,
            '_uid': user_id,
            'device_id': self.android_device_id,
            'upload_id':  int(current_timestamp),
            'device': {
                'manufacturer': 'OnePlus',
                'model': 'ONEPLUS+A3010',
                'android_version': 25,
                'android_release': '7.1.1',
            }
        })

        encoded_parameters = quote(string=parameters_as_string, safe="!~*'()")

        response = requests.post(
            url=f'{self.INSTAGRAM_API_URL}/media/configure_text_only_post/',
            headers={
                'Authorization': f'Bearer IGT:2:{self.instagram_api_token}',
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
            data=f'signed_body=SIGNATURE.{encoded_parameters}'
        )

        return response.json()
