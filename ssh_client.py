import paramiko

class SSH:

    def __init__(self, host, port, user, ssh_key_path, timeout=1800):
        self.host = host
        self.port = port
        self.user = user
        self.ssh_key_path = ssh_key_path
        self.timeout = timeout
        self.connect()

    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pkey = paramiko.RSAKey.from_private_key_file(self.ssh_key_path)
        client.connect(hostname=self.host, username=self.user, port=self.port, pkey=pkey, timeout=self.timeout)
        self.client = client

    def exec(self, shell, timeout=1800):
        stdin, stdout, stderr = self.client.exec_command(command=shell, bufsize=1, timeout=timeout)
        while True:
            line = stdout.readline()
            if not line:
                break
            print(line)
        print(stderr.read())
        code = stdout.channel.recv_exit_status()
        return code

    def close(self):
        self.client.close()


s = SSH('localhost', 22, 'johnsaxon', '/Users/johnsaxon/.ssh/id_rsa')
s.connect()
res = s.exec('ls /Users/johnsaxon')
print(res)
s.close()