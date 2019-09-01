import smtplib
import time
import imaplib
import email

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "jonathan.rehuel16" + ORG_EMAIL
FROM_PWD    = "58ac7fc07a07f4229b16c8c83748be7e24b1978fd9dbb53b9b09f7ee8f9e52d1"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs

mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(FROM_EMAIL, FROM_PWD)
mail.select('inbox')
type, data = mail.search(None,'ALL')
mail_ids = data[0]

now = 0

mail_ids = mail_ids.split()
mail_ids.reverse()
id_list = split(mail_ids,5)

while True:
    print "What would you like to do? (NOW, NEXT, PREV, OPEN [id])"
    command = raw_input()
    command.strip()
    print command

    if command.split()[0] == "OPEN":
        typ, data = mail.fetch(command.split()[1], '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                print msg
                email_subject = msg['subject']
                email_from = msg['from']
                print 'From : ' + str(email_from) + '\n'
                print 'Subject : ' + str(email_subject) + '\n'

                print "What to do now? (REPLY, FWD, NONE)"
                command2 = raw_input()

                alamat_kirim = ""

                if command2 == "REPLY":
                    alamat_kirim = str(email_from).strip()
                    subject = "Re:"
                    alamat_kirim = alamat_kirim.split('<')[1]
                    alamat_kirim = alamat_kirim.split('>')[0]

                    msg2 = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (FROM_EMAIL, str(alamat_kirim), subject)

                    print "message >>"
                    while 1:
                        try:
                            line = raw_input()
                        except EOFError:
                            break
                        if not line:
                            break
                        msg2 = msg2 + line

                elif command2 == "FWD":
                    print "kirim kemana?"
                    alamat_kirim = raw_input()
                    alamat_kirim = str(alamat_kirim).strip()
                    subject = "Fwd: "
                    msg2 = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (FROM_EMAIL, str(alamat_kirim), subject,msg)
                
                print FROM_EMAIL, alamat_kirim, subject

                server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                server.login(FROM_EMAIL,FROM_PWD)
                server.sendmail(FROM_EMAIL, alamat_kirim, msg2)

    else:
        if command == "NEXT":
            if now < len(id_list):
                now += 1
            else:
                print "You're on the last page"
                continue
        if command == "PREV":
            if now > 0:
                now -= 1
            else:
                print "You're on the first page"
                continue

        first_email_id = int(id_list[now][0])
        lastest_email_id = int(id_list[now][-1])

        print first_email_id, lastest_email_id
        for ii in id_list[now]:
            print ii
            typ, data = mail.fetch(int(ii), '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print ii, 'From: ', str(email_from)[0:20], 'Sub: ', str(email_subject)[0:20]
                    # print 'From : ' + str(email_from) + '\n'
                    # print 'Subject : ' + str(email_subject) + '\n'
