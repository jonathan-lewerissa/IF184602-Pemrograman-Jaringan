import os
import sys
import shutil
import time
from ftplib import FTP

address = '10.151.254.61'
user = 'progjar'
password = 'progjar123'

os.system('clear')
print os.getcwd()+'/'
# sys.stdout.write('Enter server address: ')
# address  = sys.stdin.readline().strip()
# sys.stdout.write('Enter username: ')
# user  = sys.stdin.readline().strip()
# sys.stdout.write('Enter password: ')
# password  = sys.stdin.readline().strip()

f = FTP(address)
f.login(user,password)
print "Connected to ", address

def downpress(path, dest):
    try:
        f.cwd(path)
        os.chdir(dest)
        os.mkdir(dest+path)
    except OSError:
        print 'OS Error'
        pass
    except ftplib.error_perm:
        print 'error: could not change to ', path
        sys.exit()
    
    filelist = f.nlst()

    for file in filelist:
        try:
            print 'TRY FOLDER: '+ path+'/'+file
            f.cwd(path+'/'+file)
            downpress(path+'/'+file,dest)
        except:
            print 'FILE: ' +dest+path
            os.chdir(dest+path)
            fb = open(dest+path+'/'+file,'wb')
            f.retrbinary('RETR '+file,fb.write)
            fb.close()

def zipfolder(path, ziph):
    for root, dirs, files, in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root,file))

while True:
    sys.stdout.write('>> ')
    command = sys.stdin.readline().strip().split()
    
    try:
        if command[0] == 'LIST':
            print "List of directories: ", f.nlst()
        elif command[0] == 'DOWNLOAD' or command[0] == 'RETR':
            fd = open(command[1],'wb')
            f.retrbinary('RETR '+command[1], fd.write)
            fd.close()
        elif command[0] == 'UPLOAD' or command[0]=='STOR':
            fd = open(command[1], 'rb')
            f.storbinary('STOR '+command[1], fd)
            fd.close()
        elif command[0] == 'PWD':
            print "Current work directory: ", f.pwd()
        elif command[0] == 'MKDIR':
            f.mkd(command[1])
        elif command[0] == 'DOWNPRESS':
            print command[1]
            init = os.getcwd()
            downpress('/'+command[1],os.getcwd())
            time.sleep(1)
            os.chdir(init)
            os.system('zip -r '+os.getcwd()+'/'+command[1]+ ' '+os.getcwd()+'/'+command[1])
            os.system('rm -r '+os.getcwd()+'/'+command[1])
        else:
            print "Invalid command"
    except:
        f.quit()