import paramiko

DIRECTORY = 'I:/Science/CIS/wyb15135/'
# connect and authenticate
COMP = "cafe.cis.strath.ac.uk"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(COMP, username="wyb15135", password="GlSparkle08#14", allow_agent=False)

sftp_client = ssh.open_sftp()
remote_file = sftp_client.open('remote_filename')
try:
    for line in remote_file:
        print()
finally:
    remote_file.close()
