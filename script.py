from ftplib import FTP

ftp = FTP('139.59.59.19');
ftp.login('anonymous','anonymous');
print(ftp.retrlines('LIST'));