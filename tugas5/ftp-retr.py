from ftplib import FTP
import os

f = FTP('10.151.254.61')
f.login('progjar','progjar123')

fd = open('kdei-bundle','wb')
f.retrbinary('RETR kdei-bundle',fd.write)
fd.close()
f.quit()