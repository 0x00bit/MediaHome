#!/bin/bash python3
from flask import Flask, render_template, request, session, redirect
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

        @self.app.route('/login', methods=['GET', 'POST'])
        def login_page():
            if request.method == 'POST':
                self.username = request.form['username']
                self.password = request.form['password']
                self.smb_server._user = self.username
                self.smb_server._passwd = self.password
                try:
                    smb_session = self.smb_server.start_conn()
                    if smb_session._connected is True:
                        session["username"] = self.username
                        return redirect("/user", code=302)
                    else:
                        print(smb_session._connected)
                        print(smb_session)

                except ex.SMBException:
                    return render_template('bad_login.html'), 401

            return render_template('login.html')

        @self.app.route('/user', methods=['GET', 'POST'])
        def home_user():
            if "username" in session:
                self.username = session["username"]
                return render_template('dir_list.html'), 200
            else:
                return render_template('bad_login.html'), 401

        return self.app.run(host='localhost', debug=False)
