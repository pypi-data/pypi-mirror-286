
from __future__ import annotations
from .configuration import Configuration
from .owncloud import Owncloud
import os 
import json 
import uuid
import hashlib
import tempfile
from .webdavefs import OwncloudFS as cFS
import shutil
import tarfile




def get_machine_uuid():
    # 获取MAC地址
    mac = uuid.getnode()
    # 将MAC地址转换为字符串
    mac_str = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    # 使用SHA-256哈希算法生成唯一标识码
    unique_id = hashlib.sha256(mac_str.encode()).hexdigest()
    return unique_id


def _safeExtract(tar_path, extract_to):
    """
    解压 tar 文件到指定目录。
    
    :param tar_path: tar 文件的路径。
    :param extract_to: 文件解压的目标目录。
    """
    # 确保目标解压目录存在，如果不存在，则创建它
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    
    # 打开 tar 文件
    with tarfile.open(tar_path, "r") as tar:
        # 解压全部内容到指定目录
        tar.extractall(path=extract_to)
        # print(f"文件已成功解压到 {extract_to}")





class FileSystem:
    """ logical file system on a cloud
    """    

    def __init__(self):
        self._conf = Configuration() 
        self._oc = Owncloud()
        self._ALQ_RemoteDir = "/ALQ_REMOTE_DATA"
        self._ALQ_RemoteConfig = f"{self._ALQ_RemoteDir}/setting.txt"
        self._ALQ_RemoteSync = f"{self._ALQ_RemoteDir}/sync"
        self._mkdirsIfNotExist( self._ALQ_RemoteDir )

    def _mkdirsIfNotExist(self,dirpath):
        # dirpath = /like/this/one 
        segs = [ s for s in dirpath.strip().split("/") if len(s)>0  ]
        p = '' 
        for seg in segs:
            p += "/" + seg 
            if not self._isPathExist(p):
                self._oc.mkdir( p )

    def _getConfigDict(self):
        if self._isPathExist(self._ALQ_RemoteConfig):
            confDict = json.loads(self._oc._getClient().get_file_contents(self._ALQ_RemoteConfig).decode()) 
            return confDict
        else:
            return {} 
        
    def _getUserPass(self):
        oConfig = self._conf._getSectionDict(section="owncloud")
        username = oConfig.get('username',None)
        password = oConfig.get('password',None) 
        return username,password

    def _setConfigDict(self,dataDict):
        self._oc._getClient().put_file_contents( remote_path = self._ALQ_RemoteConfig, data = json.dumps(dataDict))

    def _isPathExist(self,path):
        return self._oc._isPathExist(path) 

    def _getSyncTags(self):
        conf = self._getConfigDict() 
        syncTags = conf.get('syncTags',{}) 
        return syncTags

    def sync(self):
        # tagItem ->   tagName : {  'pcdir':[ 'mid_cwd',... ]   }, tagName is also the path of on the cloud
        conf = self._getConfigDict() 
        if 'syncTags' not in conf:
            conf['syncTags'] = {} 
            
        mid = get_machine_uuid() 
        cwd = os.getcwd() 
        localTag = f"{mid}_{cwd}" 
        tag = None
        for syncTag in conf['syncTags']:
            if localTag in conf['syncTags'][syncTag]['pcdir']:
                tag = syncTag 
                break 
        if tag is None:
            if len(conf['syncTags']) >0:
                print("This is the first sync in this dir. Which of the following target do you want to link?")
                for syncTag in conf['syncTags']:
                    print(f" * {syncTag} ") 
                tag = input("Please type the syncTag name. If you type a new one that is not in the list, a new point will be created for you.\n")
            else:
                tag = input("Please type a new name for recording this sync.\n")
        remotePath = self._ALQ_RemoteSync + "/" + tag 
        if tag not in conf['syncTags']:
            conf['syncTags'][tag] = { 'pcdir':[] } 
            self._mkdirsIfNotExist( remotePath ) 
        if localTag not in conf['syncTags'][tag]['pcdir']:
            conf['syncTags'][tag]['pcdir'].append(localTag) 
        self._setConfigDict(conf)
        self._oc.sync(localPath=cwd,remotePath=remotePath)


    def sendshare(self,localPath:str):
        """ <localPath>,  share a local file or directory to public, other can download it by: getsharefrom <username> 
        """        
        username,password = self._getUserPass() 
        if not ( username is not None and password is not None  ):
            raise Exception('owncloud is not set')
        cfs = cFS(username='public',password='public')
        lp = os.path.abspath(localPath) 
        basename = os.path.basename(lp)
        if os.path.isdir( lp ):
            # dir
            meta = {
                'isdir':True, 
                'filename':f"{basename}",
            } 
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_file = os.path.join(temp_dir, f"{basename}.tar") 
                shutil.make_archive(os.path.splitext(zip_file)[0], 'tar', lp) 
                cfs.uploadFile(localPath=zip_file,remotePath=f"/sharing/share_{username}_data")
        else:
            meta = {
                'isdir':False, 
                'filename':f"{basename}",
            }
            # single file 
            cfs.uploadFile(localPath=lp,remotePath=f"/sharing/share_{username}_data")
        with tempfile.TemporaryDirectory() as temp_dir:
            _meta_pf = os.path.join( temp_dir, 'tmp.txt'  )
            with open(_meta_pf,'w') as fi:
                fi.write( json.dumps(meta) )
            cfs.uploadFile(localPath=_meta_pf,remotePath=f"/sharing/share_{username}_meta.txt")
            zip_file = os.path.join(temp_dir, f"{basename}.tar") 
        return "done!"

    def getsharefrom(self,username:str):
        '''<username>, get a shared resource from the <username>'''
        # poc = self._getPublicDirClient() 
        metaFile = f"share_{username}_meta.txt" 
        dataFile = f"share_{username}_data"
        cfs = cFS(username='public',password='public')
        meta = json.loads(cfs.readFileBinary(f"/sharing/{metaFile}").decode())
        if meta['isdir']:
            localPath = os.path.join( os.getcwd(),meta['filename'] ) 
            with tempfile.TemporaryDirectory() as temp_dir:
                localZipFile = os.path.join(temp_dir, f"{meta['filename']}.tar")
                # poc.get_file(remote_path=dataFile,local_file=localZipFile) 
                cfs.downloadFile(remotePath=f"/sharing/{dataFile}",localPath=localZipFile)
                # shutil.unpack_archive(localZipFile, localPath)
                _safeExtract(tar_path=localZipFile, extract_to=localPath)
        else:
            localPath = os.path.join( os.getcwd(),meta['filename'] ) 
            cfs.downloadFile(remotePath=f"/sharing/{dataFile}",localPath=localPath)
        print(f"download data to: {localPath}")


    def test(self):
        oc = self._oc._getPublicDirClient() 


        


#         public_link = 'http://domain.tld/owncloud/A1B2C3D4'

# oc = owncloud.Client.from_public_link(public_link)
# oc.drop_file('myfile.zip')


    

