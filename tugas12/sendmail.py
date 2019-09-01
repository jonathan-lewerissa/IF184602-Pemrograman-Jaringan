import smtplib

username = "jonathan.rehuel16@gmail.com"
password = "58ac7fc07a07f4229b16c8c83748be7e24b1978fd9dbb53b9b09f7ee8f9e52d1"
FROM_EMAIL_ADDRESS = username
TO_EMAIL_ADDRESS = username
MESSAGE = "Subject: Ashiap\r\nHAIIIIII\r\nHAIII JUGA"

server = smtplib.SMTP_SSL('smtp.gmail.com',465)
server.login(username,password)
server.sendmail(FROM_EMAIL_ADDRESS, TO_EMAIL_ADDRESS, MESSAGE)