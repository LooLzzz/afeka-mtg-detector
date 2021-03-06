import os, requests, json

from config import Config

class AuthApi():
    API_ENDPOINT = f'{Config.API_HOSTNAME}/auth'
    TOKEN_PATH = os.path.join(Config.documents_path, 'access-token.json')

    @classmethod
    def CheckJWT(cls):
        if os.path.exists(cls.TOKEN_PATH):
            with open(cls.TOKEN_PATH, 'r') as fp:
                obj = json.load(fp)
            
            if 'access-token' in obj:
                url = cls.API_ENDPOINT
                # headers = {'access-token': obj['access-token']}
                # Authorization: Bearer
                headers = {'Authorization': f'Bearer {obj["access-token"]}'}
                res = requests.get(url, headers=headers)
                
                body = json.loads(res.content)
                if 'username' in body:
                    return body['username']
                

        return False

    @classmethod
    def Login(cls, username, password, save_jwt=True):
        url = f'{cls.API_ENDPOINT}/login'
        body = {
            'username': username,
            'password': password
        }
        
        res = requests.get(url, body)
        body = json.loads(res.content)
        if 'access-token' in body:
            if save_jwt:
                os.makedirs(Config.documents_path, exist_ok=True)
                with open(cls.TOKEN_PATH, 'w') as fp:
                    json.dump(body, fp)
            return True
        return False
    
    @classmethod
    def Register(cls, username, password):
        url = f'{AuthApi.API_ENDPOINT}/register'
        pass
