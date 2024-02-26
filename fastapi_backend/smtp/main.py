import json
import logging
import smtplib

from fastapi_backend.core.connectors.rabbitmq import QueueConnector

from .modules import create_user_log, decode_token, find_user, send_email
from .settings import RABIT_SETTINGS

# Init logger.
logger = logging.getLogger(__name__)


class SMTPServer:
    queue_connector = QueueConnector(**RABIT_SETTINGS)
    queue = queue_connector.name_of_queue(name="email")
    channel = queue_connector.channel

    def __init__(self):
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.__call__,
            auto_ack=True,
        )
        logger.info("Waiting for messages.")
        self.channel.start_consuming()

    def __call__(self, ch, method, properties, body):
        data = json.loads(body)
        token = data.get("token")
        sender_email, _ = decode_token(token=token)
        sender = find_user(email=sender_email)
        try:
            send_email(data['subject'], data['body'], data['to_email'])
        except smtplib.SMTPHeloError:
            message = "The server refused our HELO reply."
            logger.debug(message)
            logger.exception("Failed send email.")
        except smtplib.SMTPDataError:
            message = "The SMTP server didn't accept the data"
            logger.debug(message)
            logger.exception("Failed send email.")
        except smtplib.SMTPSenderRefused:
            message = "Sender address refused."
            logger.debug(message)
            logger.exception("Failed send email.")
        except smtplib.SMTPRecipientsRefused:
            message = "All recipient addresses refused."
            logger.debug(message)
            logger.exception("Failed send email.")
        except smtplib.SMTPNotSupportedError:
            message = "The SMTP server didn't accept the data"
            logger.debug(message)
            logger.exception("Failed send email.")
        except smtplib.SMTPAuthenticationError:
            message = "Authentication error."
            logger.debug(message)
            logger.exception("Failed send email.")
        except smtplib.SMTPException:
            message = "Base exception smtp."
            logger.debug(message)
            logger.exception("Failed send email.")
        else:
            create_user_log(sender.id)


if __name__ == "__main__":
    SMTPServer()
