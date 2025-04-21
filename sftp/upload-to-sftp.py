import os
import paramiko

# Configuration
SFTP_HOST = 'localhost'
SFTP_PORT = 2222
SFTP_USER = 'user'
SFTP_PASS = 'password'
REMOTE_DIR = 'upload'
LOCAL_DATA_DIR = './data'

def upload_files():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)

    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        sftp.chdir(REMOTE_DIR)  # Explicitly change to remote dir
    except IOError:
        print(f"⚠️ Remote directory {REMOTE_DIR} does not exist. Attempting to create it...")
        sftp.mkdir(REMOTE_DIR)
        sftp.chdir(REMOTE_DIR)
        print(f"✅ Created and switched to remote directory {REMOTE_DIR}")

    for filename in os.listdir(LOCAL_DATA_DIR):
        local_path = os.path.join(LOCAL_DATA_DIR, filename)
        remote_path = filename  # just the filename, since we are already in REMOTE_DIR

        if os.path.isfile(local_path):
            print(f"⬆️ Uploading {filename} to {REMOTE_DIR}")
            sftp.put(local_path, remote_path)

    sftp.close()
    transport.close()
    print("✅ Upload complete.")

if __name__ == "__main__":
    upload_files()