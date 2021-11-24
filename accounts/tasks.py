from django.core.mail import send_mail

from newsletter.celery import app


@app.task(name="send_email_registration")
def send_email_registration(username, email, first_name):
    send_mail(
        subject="Successful Registration",
        from_email='hello@newsletter.com',
        recipient_list=[email],
        message=f'Thank you {first_name} for being part of our community. Username: {username}',
        html_message=f'''
                    <body>
                        <h1>Successful Registration</h1>
                        <p>Thank you {first_name} for being part of our community</p>
                        <ul>
                            <li><b>Username:</b> {username}</li>
                        </ul>
                    </body>
        '''
    )