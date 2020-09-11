import subprocess
import logging
import sys
import time


class TorInstance(object):
    def __init__(self, control_port, password):
        self.reload(control_port, password)

    def reload(self, control_port, password):
        password_hash = self.genTorPassHash(password)
        config = {
            # 'ClientOnly': '1',
            'ControlPort': control_port,
            # 'DataDirectory': '~/.tor/temp',
            # 'Log': ['DEBUG stdout', 'ERR stderr' ],
            # 'CookieAuthentication': '1',
            'HashedControlPassword': password_hash
        }

        with open('/etc/tor/torrc', 'w+') as f:
            for key in config.keys():
                line = (key + " " + config[key] + "\n")
                print(line)
                f.write(line)

        time.sleep(1)
        subprocess.run(['killall', 'tor'])
        subprocess.run(['service', 'tor', 'start'])
        subprocess.run(['curl', '--socks5', '127.0.0.1:9050',
                        'http://checkip.amazonaws.com/'])

    def genTorPassHash(self, password):
        logging.info("Generating a hashed password")
        hashpass = str(subprocess.check_output(
            ['tor', '--hush', '--hash-password', str(password)]))
        # print(hashpass)
        # print(hashpass[-64:-3])
        # Strip newline and warnings
        return hashpass[-64:-3]