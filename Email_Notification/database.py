import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils
from psycopg2 import sql
import yaml
import psycopg2
from config import config


sender_data = yaml.load(open('credentials.yml'))
sender_email=sender_data['user']['email']
password=sender_data['user']['password']
reply_to="noreply@kgpexpress.com"


# Obtain the configuration parameters
params = config()
# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)
cur = conn.cursor()
query_statement = yaml.load(open('query.yml'))

cur.execute(query_statement['get_user']['query'])
all_users = cur.fetchall()

for user in all_users: 
	#print(user)
	user_name=user[0]
	receiver_email=user[1]
	name = user[2] + " " + user[3]

	raw_sql = query_statement['get_event']['query']
	#print(raw_sql)
	like_term = '{}'.format(user_name)
	cur.execute(raw_sql,(like_term,))
	events = cur.fetchall()

	if len(events) > 0:
		msg_content = "Subject : \t Event Name \t Timing \t Description\n"
		for event in events:
			msg_content = msg_content + event[0] + "("+ event[1] + ")" + "\t" + event[2] + "\t" + event[4]+'-'+event[5]+'\t'+event[3]+'\n' 
		message = MIMEMultipart("alternative")
		message["Subject"] = "multipart test"
		message["From"] = email.utils.formataddr(('KGPExpress', sender_email))
		message["To"] = email.utils.formataddr((name, receiver_email))
		message.add_header('reply-to',reply_to)
		html = """\
		<html>
		  <body>
		    <p>Hi """ + name + """",<br>
		       Your schedule for tomorrow is <br>""" + msg_content +"""
		    </p>
		    <p>
		    <br>
		    KGPExpress Team
		    </p>
		  </body>
		</html>
		"""
		#part3=receiver_email
		# Turn these into plain/html MIMEText objects
		part1 = MIMEText(text, "plain")
		part2 = MIMEText(html, "html")
		part3 = MIMEText(receiver_email, "plain")
		# Add HTML/plain-text parts to MIMEMultipart message
		# The email client will try to render the last part first
		message.attach(part1)
		message.attach(part2)
		#message.attach(part3)
		print(message.as_string())
		# Create secure connection with server and send email
		context = ssl.create_default_context()
		print("sending mail")
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		    server.login(sender_email, password)
		    server.sendmail(
		        sender_email, receiver_email, message.as_string()
		    )

# close the communication with the PostgreSQL
cur.close()