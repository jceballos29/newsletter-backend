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


@app.task(name="send_email_subscribe")
def send_email_subscribe(email, newsletter):
    send_mail(
        subject="New Subscription",
        from_email='hello@newsletter.com',
        recipient_list=[email],
        message=f'Congratulations! You have subscribed to the newsletter: {newsletter}',
        html_message=f'''
                    <body>
                        <h1>Congratulations!</h1>
                        <p>You have subscribed to the newsletter: {newsletter}</p>
                    </body>
        '''
    )


@app.task(name="send_email_unsubscribe")
def send_email_unsubscribe(email, newsletter):
    send_mail(
        subject="Unsubscribe",
        from_email='hello@newsletter.com',
        recipient_list=[email],
        message=f'You have unsubscribed to the newsletter: {newsletter}',
        html_message=f'''
                    <body>
                        <p>You have unsubscribed to the newsletter: {newsletter}</p>
                    </body>
        '''
    )


@app.task(name="send_email_share")
def send_email_share(email, emails, newsletter):
    send_mail(
        subject="Share Newsletter",
        from_email=email,
        recipient_list=emails,
        message=f'My newsletter {newsletter} is available for you to add content.',
        html_message=f'''
                    <body>
                        <h1>Share Newsletter</h1>
                        <p>My newsletter <b>{newsletter}</b>  is available for you to add content.</p>
                    </body>
                '''
    )


# @app.on_after_configure.connect
# def setup_periodic_task(sender, frequency, email, newsletter, **kwargs):
#     sender.add_pero

@app.task(name="send_email")
def send_email(email, newsletter):
    send_mail(
        subject="Stay Informed",
        from_email='hello@newsletter.com',
        recipient_list=[email],
        message=f'Enter our newsletter {newsletter} and check if you have missed something.',
        html_message=f'''
                <body>
                    <h1>Stay Informed</h1>
                    <p>Enter our newsletter <b>{newsletter}</b> and check if you have missed something.</p>
                </body>
            '''
    )
