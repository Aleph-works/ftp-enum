import ftplib
import argparse

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


# Get all the arguments
args = vars(parse.parse_args())

print(args)

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

if __name__ == '__main__':
    if args['dir'] and args['file']:
        ftp_file_download(server=args['url'],username=args['username'], password=args['password'])