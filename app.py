#!/bin/bash python3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


class Server:
    '''
    Main class, responsible for instantiating the server and database
    '''
    def __init__(self) -> None:
        self.app = Flask(__name__, template_folder='./templates/')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mediahome.db'
        self.db = SQLAlchemy(self.app)

        class User(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            username = self.db.Column(self.db.String(40), nullable=False)
            password = self.db.Column(self.db.String(80), nullable=False)

        self.def_adm = User(username='admin', password='admin')

    def create_database(self):
        with self.app.app_context():
            self.db.create_all()
            print("[Info]: Database was created!")
            self.db.session.add(self.def_adm)
            self.db.session.commit()
            print("[Info]: Default credentials were added!")

    def create_server(self):
        '''
        This function is responsable for creating and
        setup whole server
        '''
        @self.app.route('/')
        def home():
            return "hello!"

        @self.app.route('/login', methods=['GET', 'POST'])
        def login_page():
            if request.method == 'POST':
                self.username = request.form['username']
                self.password = request.form['password']

            elif request.method == 'GET':
                return render_template('login.html')
            else:
                pass

        return self.app.run(debug=False)


server = Server()
server.create_database()
server.create_server()
