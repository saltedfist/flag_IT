from database.ext import Mail, Message


def send_mail(msg):
    d = [{
        'subject': msg['s'],
        'recipients': msg['r'],
        'html': msg['c']
    }]
    for i in range(len(d)):
        with Mail.connect() as conn:
            try:
                conn.send(Message(**d[i]))
                d[i]['response'] = 'ok'
            except Exception as e:
                d[i]['response'] = str(e)

    # 邮件未完成.
