import smbclient


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
        """List all files on some folder"""
        dirs = self.smb.listdir(f"{self._server}/{folder}")
        if len(dirs) > 0:
            print(f'Files: {dirs}')
        else:
            print('Empty directory')
