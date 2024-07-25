import re
import socket
import time
import urllib.parse
from typing import Optional, Any

import jwt
import requests
from requests import RequestException
from terevintosoftware.pkce_client import PkceClient, PkceLoginConfig
from terevintosoftware.pkce_client.token_config_map import TokenConfigMap


def _insert_proxy_auth(proxy_url: str, username: Optional[str], password: Optional[str]) -> str:
    if '//' not in proxy_url:
        raise ValueError('Proxy URL must contain http:// or https://')
    if username:
        prefix, hostname = proxy_url.split("//")
        password_str = f":{urllib.parse.quote(password)}" if password else ""
        return f"{prefix}//{urllib.parse.quote(username)}{password_str}@{hostname}"
    else:
        return proxy_url


def _is_token_expired(token: str, token_refresh_window: int = 60) -> bool:
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        if 'exp' in decoded:
            exp_time = decoded['exp']
            current_time = time.time()
            # time in seconds
            return current_time > exp_time - token_refresh_window
        return False
    except jwt.DecodeError:
        raise
    except jwt.ExpiredSignatureError:
        return True


def _parse_azp_from_token(token: str) -> str:
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get('azp', None)
    except jwt.DecodeError:
        raise


def _get_azure_storage_url(account: str, container: str) -> str:
    """Generates an Azure blob storage url.

    Parameters:
        account (str): the Azure storage account name
        container (str): the Azure storage container name

    Returns:
        str: Azure blob storage url
    """

    return f'https://{account}.blob.core.windows.net/{container}'


def _sanitize_url(url: str) -> str:
    """
    handles multiple slashes in url by replacing them with a single slash, while keeping the double slashes after protocol scheme
    :param url:
    :return:
        sanitized url
    """
    parts = url.split('://')
    result = parts[0] + '://' + re.sub('//+', '/', parts[1])
    return result


def _find_free_port():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Bind the socket to a random port
            s.bind(('', 0))

            # Get the port number
            _, port = s.getsockname()

            return port
        except OSError as e:
            raise EnvironmentError(f"Unable to bind a free port: {e}")
        finally:
            # Close the socket
            s.close()


class TokenHolder:
    def __init__(self, **kwargs: Any) -> None:
        self.domain = kwargs['domain']
        self.realm = kwargs['realm']
        self.client_id = kwargs['client_id']
        self.session = kwargs['session']

        # Time window (in seconds) before access_token expiry when it's still valid but eligible for refresh.
        self.token_refresh_window = kwargs.get('token_refresh_window', 60)
        self.access_token = kwargs.get('access_token', '')
        self.refresh_token = kwargs.get('refresh_token', '')

    def get_tokens_with_credentials(self, username, password) -> None:
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "username": username,
            "password": password
        }
        try:
            response = self.session.post(f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token', data=data)
            response.raise_for_status()
            response_json = response.json()

            # Ensure the expected keys are in the response
            if "access_token" in response_json and "refresh_token" in response_json:
                self.access_token = response_json["access_token"]
                self.refresh_token = response_json["refresh_token"]
            else:
                raise KeyError("Expected keys 'access_token' and 'refresh_token' not found in response")

        except (KeyError, RequestException, ValueError) as err:
            print(f'An error occurred: {err}')
            raise
        except Exception as err:
            print(f'An unexpected error occurred: {err}')
            raise

    def get_tokens_by_authflow(self) -> None:

        config = PkceLoginConfig(
                authorization_uri=f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/auth',
                token_uri=f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token',
                scopes=["openid"],
                client_id=self.client_id,
                internal_port=_find_free_port(),
                add_random_state=True,
                random_state_length=32,
                verify_authorization_server_https=False,
                token_config_map=TokenConfigMap(scopes='scope'))

        login_client = PkceClient(config)
        pkce_token = login_client.login()
        self.access_token = pkce_token.access_token
        self.refresh_token = pkce_token.refresh_token

    def _refresh_tokens(self):
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            response = self.session.post(f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token', headers=headers, data=payload)
            response.raise_for_status()
            response_json = response.json()
            self.access_token = response_json.get("access_token")
            self.refresh_token = response_json.get("refresh_token")
        except requests.exceptions.HTTPError as http_err:
            raise TokenRefreshError(response.status_code, f"Failed to refresh tokens: HTTP error occurred - {http_err}") from http_err
        except requests.exceptions.RequestException as req_err:
            raise TokenRefreshError(-1, f"Failed to refresh tokens: Request error occurred - {req_err}") from req_err
        except KeyError as key_err:
            raise TokenRefreshError(-1, f"Failed to refresh tokens: Key error occurred - Missing {key_err} in the response") from key_err
        except Exception as err:
            raise TokenRefreshError(-1, f"Failed to refresh tokens: An unexpected error occurred - {err}") from err

    def get_token(self) -> str:
        if _is_token_expired(self.access_token, self.token_refresh_window):
            self._refresh_tokens()
        return self.access_token


class TokenRefreshError(Exception):
    """Custom exception for errors occurring during token refresh."""

    def __init__(self, status_code, message="Error occurred during token refresh"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.status_code > 0:
            return f"{self.message} (Status Code: {self.status_code})"
        else:
            return self.message
