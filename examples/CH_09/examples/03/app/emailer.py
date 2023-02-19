from logging import getLogger

import sib_api_v3_sdk
from flask import current_app
from sib_api_v3_sdk.rest import ApiException

logger = getLogger(__name__)
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = current_app.config.get("SIB_API_KEY")


def send_mail(to, subject, contents):
    """Sends an email using SendInBlue

    Args:
        to (string): The email address to send the email to
        subject (string): The subject of the email
        contents (string): The html formatted email contents
    """

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to}],
        html_content=contents,
        sender={"name": "MyBlog", "email": "no-reply@myblog.com"},
        subject=subject
    )
    try:
        api_instance.send_transac_email(smtp_email)
        logger.debug(f"Confirmation email sent to {to}")
    except ApiException as e:
        logger.exception("Exception sending email", exc_info=e)
