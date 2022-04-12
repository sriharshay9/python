import pandas as pd
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from github import Github
from prettytable import PrettyTable
from pretty_html_table import build_table
#import requests

table = PrettyTable()

repo_to_scan = input ("Enter the git repo: ")
# github_token = input ("Enter the authentication token: ")
from_mail_id = input ("Enter the from mail id: ")
to_mail_id = input ("Enter the to mail id: ")
# r = requests.get('https://github.com/ekzhang/bore.git')
# print(r.json)

g = Github()
def pull_request():
    repo = g.get_repo(repo_to_scan)
    pulls = repo.get_pulls(state='all', sort='created', base='master')
    mydict = {"Title":[],"State":[], "Number":[], "Create Time":[], "Merged Status":[]}
    for pr in pulls:
       state = pr.state
       number = pr.number
       title = pr.title
       time = pr.created_at
       merge = pr.is_merged()
       mydict["Title"].append(title)
       mydict["State"].append(state)
       mydict["Number"].append(number)
       mydict["Create Time"].append(time)
       mydict["Merged Status"].append(merge)
    data = pd.DataFrame(mydict)
    return(data)


def send_mail(body):

    message = MIMEMultipart()
    message['Subject'] = 'Pull Request Report'
    message['From'] = from_mail_id
    message['To'] = to_mail_id

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], 'yaadagani')
    server.sendmail(message['From'], message['To'], msg_body)
    server.quit()


def send_country_list():
    gdp_data = pull_request()
    output = build_table(gdp_data, 'blue_light')
    send_mail(output)
    return "Mail sent successfully."


send_country_list()