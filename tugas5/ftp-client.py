from ftplib import FTP
f = FTP('10.151.254.61')

print "welcome: ", f.getwelcome()

f.login('progjar','progjar123')
print "current work directory: ", f.pwd()
names = f.nlst()
print 'List of directory: ', names
f.quit()