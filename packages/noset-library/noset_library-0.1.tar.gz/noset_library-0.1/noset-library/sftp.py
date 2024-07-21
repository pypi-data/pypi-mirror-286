#%%
#Packages
import os

#Configure logging
from logger import configure_logging

logger = configure_logging(os.environ.get('LOGFILE_PATH'))
#%%

try:
    import paramiko
except Exception as e:
    logger.error(f"Missing Package: {e}")
    raise SystemExit("Exiting...")

def connect_to_sftp(host, username, password):
    try:
        ssh_client = paramiko.SSHClient()

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(hostname=host, username=username, password=password)
    except Exception as e:
        logger.error("Error connecting to the SFTP server: "+str(e))
        raise SystemExit("Exiting...")


