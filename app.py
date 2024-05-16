#!/bin/bash python3
from flask import Flask, render_template, request, session, redirect, jsonify
from smbmodule import SmbConnection
from smbprotocol import exceptions as ex


class Server:
    '''
    Main class, responsible for instantiating the server and database
    '''
    def __init__(self):
        self.app = Flask(__name__, template_folder='./templates/')
        self.smb_server = SmbConnection('127.0.0.1')
        self.session = None
        self.app.secret_key = "cookedpotatos"

    def create_server(self):

        '''
        This function is responsable for creating and
        setup whole server
        '''

        @self.app.route('/', methods=['GET', 'POST'])
        def home():
            return render_template('index.html'), 200

        # Endpoint to logout
        @self.app.route('/logout', methods=['GET'])
        def logout():
            print(session, dir(session))
            session.pop("session", None)
            return redirect("/", code=200)

        # Authentication page
        @self.app.route('/login', methods=['GET', 'POST'])
        def login_page():
            if request.method == 'POST':
                self.smb_server._user = request.form['username']
                self.smb_server._passwd = request.form['password']
                # The path will receives the username
                self.smb_server.path = self.smb_server._user
                
                try:
                    # Check is the session already exist
                    if self.smb_server._user in session:
                        session.pop(self.smb_server._user, None)
                        print("Removing existing session...")
                    
                    smb_session = self.smb_server.start_conn()
                    if smb_session._connected is True:
                        session[self.smb_server._user] = smb_session.session_key
                        return redirect(f"/home/{self.smb_server._user}", code=302)

                except ex.SMBException:
                    return render_template('bad_login.html'), 401

            return render_template('login.html')

        # Default page of user directory
        @self.app.route('/home/<user>', methods=['GET', 'POST'])
        def home_user(user):
            # If user session exist, save the session in class and return HTML page
            if self.smb_server._user in session:
                self.session = session[self.smb_server._user]
                print(self.smb_server._user)
                directory_files = self.smb_server.list_files(self.smb_server._user)
                # If the list of directory doesn't return None, show the normal page with files
                if type(directory_files) != None:
                    return render_template('dir_list.html', files_dir=directory_files), 200
                else:
                    return render_template('dir_list.html'), 200
            else:
                return render_template('bad_login.html'), 401

        return self.app.run(host='localhost', debug=False)
    
