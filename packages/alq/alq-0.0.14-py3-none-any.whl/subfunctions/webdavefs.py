
from webdav3.client import Client
import tempfile
import os 

# pip install webdavclient3

class BaseFs():

    def _getHostUrl(self):
        raise Exception('host name not set!') 

    def __init__(self,username,password):
        _options = {
            'webdav_hostname': self._getHostUrl(),
            'webdav_login':    username,
            'webdav_password': password,
        }
        self._client = Client(_options)

    def listPath(self,path:str)->list[str]: 
        """_summary_

        Args:
            path (str): example: /path/to/there

        Returns:
            list[str]: ['file','directory/']
        """        
        return self._client.list(path) 

    def uploadFile(self,localPath:str,remotePath:str):
        self._client.upload_sync(remote_path=remotePath, local_path=localPath)

    def downloadFile(self,remotePath:str,localPath:str):
        self._client.download_sync(remote_path=remotePath, local_path=localPath)

    def readFileBinary(self,remotePath:str):
        with tempfile.TemporaryDirectory() as temp_dir:
            _meta_pf = os.path.join( temp_dir, 'tmp.data'  )
            self.downloadFile(remotePath=remotePath,localPath=_meta_pf)
            with open(_meta_pf,'rb') as f:
                return f.read()

class OwncloudFS(BaseFs):
    
    def _getHostUrl(self):
        return "http://192.168.1.7:8096/remote.php/webdav/"
    


if __name__ == '__main__':
    c = OwncloudFS(username='public',password='public') 
    c.downloadFile( localPath='/home/hengyue/Documents/Projects/test/webdavefs33.py', remotePath="/haha/1.txt" )

