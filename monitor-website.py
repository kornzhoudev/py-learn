import requests
import smtplib
import os
import paramiko
import linode_api4
import time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')

def restart_server_and_container():
    # restart linode server
    print('Rebooting the server...')
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance, 44294556)
    nginx_server.reboot()

    # restart the application
    while True:
        nginx_server = client.load(linode_api4.Instance, 44294556)
        if nginx_server.status == 'running':
            time.sleep(5)
            restart_container()
            break

def send_notification(email_msg):
    print("Sending an email...")
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message= f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname='143.42.46.167',
        username='root',
        port=22,
        key_filename='/Users/nikkitang/.ssh/id_rsa'
    )
    stdin, stdout, stderr = ssh.exec_command('docker start 90b3349be95e')
    print(stdout.readlines())
    ssh.close()
    print('Application restarted')

def monitor_application():
    try:
        res = requests.get('http://143-42-46-167.ip.linodeusercontent.com:8080/')
        if res.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Application Down. Fix it!')
            msg = f'Application return {res.status_code}'
            send_notification(msg)
            restart_container()

    except Exception as ex:
        print(f'Connection error happened {ex}')
        msg = "Application not accessible at all"
        send_notification(msg)
        restart_server_and_container()

schedule.every(5).seconds.do(monitor_application)

while True:
    schedule.run_pending()