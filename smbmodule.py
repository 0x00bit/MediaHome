import smbclient
from smbprotocol import exceptions as ex


class SmbConnection:
    def __init__(self, server, user=None, passwd=None, workgroup="WORKGROUP", path=None):
        self._server = server
        self._user = user
        self._passwd = passwd
        self.workgroup = workgroup
        self.path = path
        self.smb = smbclient

    def _get_conn_parameters(self):
        """Returns connection parameters to start the connection with smb server"""
        return self._server, self._user, self._passwd

    def start_conn(self):
        # Starting my connection
        _server, _user, _passwd = self._get_conn_parameters()
        return self.smb.register_session(_server, _user, _passwd)

    def list_files(self, folder):
        self.dirs = []
        self.files = []
        """List all files on some folder"""
        dirs = self.smb.listdir(f"{self._server}/{folder}")
        if len(dirs) > 0:
            items = self.smb.listdir(f"{self._server}/{folder}")
            for item in items:
                try:
                    self.smb.walk(f"{self._server}/{folder}/{item}")
                    self.dirs.append(item)

                except ex.SMBOSError as e:
                    if e.errno == 20: 
                        self.files.append(item)
                    else:
                        raise e
            return self.dirs, self.files

    def delete_file(self, path):
        try:
            self.smb.remove(path)
            return f'File: {path} was removed'

        except ex.SMBOSError as e:
            if e.errno == 21:  # Erro 21 means directory
                self.smb.removedirs(path)
                directory = path.split('/')[-1]  # Get directory name
                return f'Folder {directory} was removed'
            else:
                raise e

        except ex.exceptions.NotFound:
            return "File not Found"
