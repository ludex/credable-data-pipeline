
import os
import paramiko

# Configuration
SFTP_HOST = 'localhost'
SFTP_PORT = 2222
SFTP_USER = 'user'
SFTP_PASS = 'password'
REMOTE_DIR = 'upload'
LOCAL_DATA_DIR = './sftp-downloads'

def download_files():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)

    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        sftp.chdir(REMOTE_DIR)
        print(f"📁 Remote directory set to: {REMOTE_DIR}")
    except IOError:
        print(f"❌ Remote directory {REMOTE_DIR} does not exist.")
        sftp.close()
        transport.close()
        return

    os.makedirs(LOCAL_DATA_DIR, exist_ok=True)

    for filename in sftp.listdir():
        remote_path = filename
        local_path = os.path.join(LOCAL_DATA_DIR, filename)
        print(f"⬇️ Downloading {filename} to {local_path}")
        sftp.get(remote_path, local_path)

    sftp.close()
    transport.close()
    print("✅ Download complete.")

if __name__ == "__main__":
    download_files()