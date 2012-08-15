__author__ = ''
__version__ = 0.01

from sys import exit
import requests

class OpenFileDB:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login()

    def login(self):
        '''
        Authenticate and get a token
        '''
        url = 'https://openfiledb.com/api/login'
        token = requests.get(url, auth=(self.username, self.password), verify=False)
        self.token = token.json['token'] if token else 'invalid'
        if self.token == 'invalid': exit('Login failed. Please, check your credentials.')

    def get(self, hash):
        '''
        Gets the most recent document related to a hash
        '''
        url = 'http://openfiledb.com/api/file/' + self.token + '/' + hash
        data = requests.get(url)
        return data.json

    def set(self, hash, data):
        '''
        Sets a document related to a hash. It will return an error if hash exists in DB.
        '''
        url = 'http://openfiledb.com/api/file/' + self.token + '/' + hash
        data = requests.post(url, data)
        return data.json

    def update(self, hash, data):
        '''
        Updates a document related to a hash. The hash needs to exist in the DB.
        '''
        url = 'http://openfiledb.com/api/file/' + self.token + '/' + hash
        data = requests.put(url, data)
        return data.json

    def comment(self, hash, text):
        '''
        Sets a document related to a hash. It will return an error if hash exists in DB.
        '''
        url = 'http://openfiledb.com/api/comment/' + self.token + '/' + hash
        data = {'comment': text}
        data = requests.post(url, data)
        return data.json

    def get_comments(self, hash):
        '''
        Sets a document related to a hash. It will return an error if hash exists in DB.
        '''
        url = 'http://openfiledb.com/api/comment/' + self.token + '/' + hash
        data = requests.get(url)
        return data.json

    def get_nice(self, hash):
        '''
        Gets the most recent document related to a hash, AND beautifies/classifies the response into:
        Basic, Data and Comments
        '''
        data = self.get(hash)
        if not 'error' in data and not 'result' in data:
            # Divide RAW data into basic, data and comments
            basic = {}
            metadata = {}
            comments = {}
            for key, value in data.iteritems():
                if key in ['sha1', 'sha256', 'md5', 'crc32', 'filename', 'filesize', 'source']:
                    basic[key] = value
                elif 'comment:' in key:
                    comments[key.split('comment:')[1]] = value
                else:
                    metadata[key] = value
            return dict(hash=hash, basic=basic, metadata=metadata, comments=comments)

    def flag(self, hash):
        '''
        Flag a file with inappropriate content/abusive, tec.
        '''
        url = 'http://openfiledb.com/api/flag/' + self.token + '/' + hash
        data = requests.post(url)
        return data.json

    def versions(self, hash):
        '''
        Get ALL the versions of the data linked to a hash.
        '''
        url = 'http://openfiledb.com/api/versions/' + self.token + '/' + hash
        data = requests.get(url)
        return data.json

    def logout(self):
        '''
        Logout a user. All tokens related to user will expire.
        '''
        url = 'http://openfiledb.com/api/logout/' + self.token
        data = requests.get(url)
        return data.json
