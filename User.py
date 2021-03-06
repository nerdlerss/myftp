import hashlib

class AuthException(Exception):
    def __init__(self,username,user=None):
        super().__init__(username,user)
        self.username = username
        self.user = user

class UsernameAlraadyExists(AuthException):
    pass

class PasswordTooShort(AuthException):
    pass

class InvaidUserName(AuthException):
    pass
class InvaidPassword(AuthException):
    pass

class User:
    def __init__(self,username,password,disk_quata=None,home_path=None):
        self.username = username
        self.password = self._encrypt_pw(password)
        self.is_logged_in = False
        self.disk_quata = disk_quata
        self.home_path = home_path

    def _encrypt_pw(self,password):
        hash_string = (self.username+password)
        hash_string = hash_string.encode("utf-8")
        return hashlib.sha256(hash_string).hexdigest()


    def check_password(self,password):
        encry_str = self._encrypt_pw(password)
        return encry_str == password

    def ftp_check_password(self,password):
        return self.password == password


class User_Auth:
    def __init__(self):
        self.users = {}

    def add_user(self,username,password,disk_quata,home_path):
        if username in self.users:
            raise UsernameAlraadyExists(username)
        if len(password) < 6:
            raise PasswordTooShort(username)
        self.users[username] = User(username,password,disk_quata,home_path)


    def login(self,username,password):
        try:
            user = self.users[username]
        except KeyError:
            raise InvaidUserName(username)

        if not user.ftp_check_password(password):
            raise InvaidPassword(username,user)
        user.is_logged_in = True
        return True

