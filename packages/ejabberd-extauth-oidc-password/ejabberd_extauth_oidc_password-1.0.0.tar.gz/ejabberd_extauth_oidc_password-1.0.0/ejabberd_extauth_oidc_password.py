#!/usr/bin/python3

from oauthlib.oauth2 import InvalidGrantError, LegacyApplicationClient
from pydantic import BaseModel, HttpUrl, SecretStr
from requests_oauthlib import OAuth2Session

from ejabberd_extauth import ExtAuth, ExtAuthHandler


class ServerConfig(BaseModel):
    issuer: HttpUrl
    token_url: HttpUrl
    client_id: str
    client_secret: SecretStr


class OIDCPasswordHandler(ExtAuthHandler):
    name = "oidc_password"

    def _parse_config(self, config: dict) -> dict:
        return {server: ServerConfig.model_validate(server_config) for server, server_config in config.items()}

    def auth(self, user: str, server: str, password: str) -> bool:
        server_config = self._config.get(server, None)
        if server_config is None:
            self._logger.error("Server %s not configured", server)
            return False


        oauth = OAuth2Session(client=LegacyApplicationClient(client_id=server_config.client_id))
        try:
            token = oauth.fetch_token(token_url=str(server_config.token_url), client_secret=server_config.client_secret.get_secret_value(), username=user, password=password)
            self._logger.debug("Successfully acquired token for user %s on server %s", user, server)
        except InvalidGrantError:
            self._logger.debug("Invalid credentials for user %s on server %s", user, server)
            return False
        
        return True
        

def main():
    ExtAuth(OIDCPasswordHandler).run()

if __name__ == "__main__":
    main()
