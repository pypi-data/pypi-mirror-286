from __future__ import annotations

from pathlib import Path
import yaml

class CredentialsError(RuntimeError): ...

class Credentials(dict):

    @classmethod
    def load(
        cls, 
        type: str, 
        user: str, 
        app: str = 'obstechutils', 
        path: Path = Path('~/.config')
    ) -> Credentials:

        path = path.expanduser()
        filename = Path(f"{path}/{app}/credentials.yaml")
        if not filename.exists():
            msg = f'No credentials for {app} in {path}'
            raise ConnectionError(msg)

        try:
            with open(filename) as in_:
                credentials = yaml.safe_load(in_)
        except Exception as e:
            msg = f'Bad credentials for {app}: {e}'
            raise CredentialsError(msg)

        try:
            credentials = credentials[type]
        except:
            msg = f'No credenitals for {app} of type {type}'
            raise CredentialsError(msg)

        try:
            credentials = credentials[user]
        except:
            msg = f'No credentials for {user}' 
            raise CredentialsError(msg) 
        
        return cls(**credentials)

