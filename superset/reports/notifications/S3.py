import json
import logging
import boto3
from flask_babel import gettext as __
from io import BytesIO
import random
import datetime
from superset import app
from superset.exceptions import SupersetErrorsException
from superset.reports.models import ReportRecipientType
from superset.reports.notifications.base import BaseNotification
from superset.reports.notifications.exceptions import NotificationError
from superset.utils.decorators import statsd_gauge

logger = logging.getLogger(__name__)

class S3Notification(BaseNotification):

    type = ReportRecipientType.S3
    
    def send(self):
        print(f"Testing the aws keys from ui:{self._content.aws_key}")
        images = {}
        report_name= self._content.name
        current_datetime = datetime.datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d")
        name_prefix=f"cira-screenshots-{formatted_date}/{report_name}/"
        if self._content.screenshots:
            images = {
                f'{name_prefix}Screenshot{random.randint(1,1000)}.png': screenshot
                for screenshot in self._content.screenshots
            }
        bucket_name=json.loads(self._recipient.recipient_config_json)["target"]
        aws_access_key_id=app.config["AWS_ACCESS_KEY"]
        aws_secret_access_key=app.config["AWS_SECRET_KEY"]
        region=app.config["AWS_REGION"]
        s3=boto3.client('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region)

        try:
            for key,file in images.items():
                file = BytesIO(file)
                s3.upload_fileobj(file,bucket_name,key,ExtraArgs={
            'Metadata': {'Content-Disposition': 'inline'},
            'ContentType': 'image/png'
        })
            logger.info(
                "Report sent to Aws S3 Bucket, notification content is %s",self._content.header_data
            )
        except SupersetErrorsException as ex:
            raise NotificationError(
                ";".join([error.message for error in ex.errors])
            ) from ex
        except Exception as ex:
            raise NotificationError(str(ex)) from ex
