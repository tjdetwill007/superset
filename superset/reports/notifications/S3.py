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

class S3SubTypes:
    S3_CRED = 'AWS_S3_credentials'
    S3_CONFIG = 'AWS_S3_pyconfig'
    S3_ROLE = 'AWS_S3_IAM'


class S3Notification(BaseNotification):

    type = ReportRecipientType.S3
    
    def _get_inline_files(self):
        current_datetime = datetime.datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d")
        report_name= self._content.name
        name_prefix=f"{report_name}/{formatted_date}/"

        if self._content.csv:
    
                data = {
                    f'{name_prefix}{report_name}{random.randint(1,1000)}.csv': self._content.csv
                }
                return data
        
        if self._content.screenshots:
            images = {
                f'{name_prefix}Screenshot{random.randint(1,1000)}.png': screenshot
                for screenshot in self._content.screenshots
            }
            return images
        return []
    
    def _get_aws_keys(self, role_arn):

        aws_access_key_id=app.config["AWS_ACCESS_KEY"]
        aws_secret_access_key=app.config["AWS_SECRET_KEY"]
        sts_client = boto3.client('sts', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        response = sts_client.assume_role(
            RoleArn=role_arn,RoleSessionName='AssumeRoleSession', DurationSeconds=3600)
        temp_cred = response['Credentials']
        return temp_cred
    
    def _execute_s3_upload(self, file_body, bucket_name, contentType, aws_access_key_id,aws_secret_access_key):
        
        for key,file in file_body.items():
            file = BytesIO(file)
            s3=boto3.client('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
            s3.upload_fileobj(file,bucket_name,key,ExtraArgs={
                'Metadata': {'Content-Disposition': 'inline'},
                'ContentType': contentType})

            logger.info(
                    "Report sent to Aws S3 Bucket, notification content is %s",self._content.header_data
                )

    def send(self):
        files = self._get_inline_files()
        file_type = "csv" if self._content.csv else "png"
        bucket_name=json.loads(self._recipient.recipient_config_json)["target"]
        s3_Subtype=self._content.aws_S3_types

        try:

            if s3_Subtype == S3SubTypes.S3_CRED:

                aws_access_key_id = self._content.aws_key
                aws_secret_access_key = self._content.aws_secretKey

                self._execute_s3_upload(file_body=files, bucket_name=bucket_name, contentType=file_type, aws_access_key_id= aws_access_key_id,aws_secret_access_key=aws_secret_access_key)

            elif s3_Subtype == S3SubTypes.S3_ROLE:

                aws_cred=self._get_aws_keys(self._content.aws_arn_role)
                aws_access_key_id = aws_cred['AccessKeyId']
                aws_secret_access_key = aws_cred['SecretAccessKey']
                self._execute_s3_upload(file_body=files, bucket_name=bucket_name, contentType=file_type, aws_access_key_id= aws_access_key_id,aws_secret_access_key=aws_secret_access_key)

            elif s3_Subtype == S3SubTypes.S3_CONFIG:
                aws_access_key_id=app.config["AWS_ACCESS_KEY"]
                aws_secret_access_key=app.config["AWS_SECRET_KEY"]

                self._execute_s3_upload(file_body=files, bucket_name=bucket_name, contentType=file_type, aws_access_key_id= aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
            else:
                logger.error(f"Unsupported AWS S3 method, Must be {S3SubTypes.S3_CONFIG} | {S3SubTypes.S3_CRED} | {S3SubTypes.S3_ROLE}")

        except SupersetErrorsException as ex:
            raise NotificationError(
                ";".join([error.message for error in ex.errors])
            ) from ex
        except Exception as ex:
            raise NotificationError(str(ex)) from ex
