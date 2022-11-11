#random uuid generator
import string
import secrets

class uuid_generator():
    def __init__(self):
        self.full= string.ascii_letters+string.digits+string.punctuation
        self.uuid=''
        self.length= 12

    def uid(self):
        for i in range(self.length):
            self.uuid+= ''.join(secrets.choice(self.full))
        return self.uuid

print(type(uuid_generator().uid()))
