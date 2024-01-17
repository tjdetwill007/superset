/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import React, { FunctionComponent, useState } from 'react';
import { styled, t, useTheme } from '@superset-ui/core';
import { Select } from 'src/components';
import Icons from 'src/components/Icons';
import { NotificationMethodOption } from 'src/views/CRUD/alert/types';
import { StyledInputContainer } from '../AlertReportModal';
import LabeledErrorBoundInput from 'src/components/Form/LabeledErrorBoundInput';
import { noBottomMargin } from 'src/components/ReportModal/styles';

const StyledNotificationMethod = styled.div`
  margin-bottom: 10px;

  .input-container {
    textarea {
      height: auto;
    }
  }

  .inline-container {
    margin-bottom: 10px;

    .input-container {
      margin-left: 10px;
    }

    > div {
      margin: 0;
    }

    .delete-button {
      margin-left: 10px;
      padding-top: 3px;
    }
  }
`;

type NotificationSetting = {
  method?: NotificationMethodOption;
  recipients: string;
  options: NotificationMethodOption[];
};

interface NotificationMethodProps {
  setting?: NotificationSetting | null;
  index: number;
  onUpdate?: (index: number, updatedSetting: NotificationSetting) => void;
  onRemove?: (index: number) => void;
}

export const NotificationMethod: FunctionComponent<NotificationMethodProps> = ({
  setting = null,
  index,
  onUpdate,
  onRemove,
}) => {
  const { method, recipients, options } = setting || {};
  const [recipientValue, setRecipientValue] = useState<string>(
    recipients || '',
  );
  const theme = useTheme();
  const s3SubTypes = ['AWS_S3_credentials', 'AWS_S3_pyconfig', 'AWS_S3_IAM'];
  const [s3Method, setS3Method] = useState(null);
  const [bucketName, setBucketName] = useState<string>('');
  const [accessKey, setAccessKey] = useState<string>('');
  const [secretKey, setSecretKey] = useState<string>('');
  const [iam, setIam] = useState<string>('');

  if (!setting) {
    return null;
  }

  const onMethodChange = (method: NotificationMethodOption) => {
    // Since we're swapping the method, reset the recipients
    setRecipientValue('');
    if (onUpdate) {
      const updatedSetting = {
        ...setting,
        method,
        recipients: '',
      };

      onUpdate(index, updatedSetting);
    }
  };

  const onRecipientsChange = (
    event: React.ChangeEvent<HTMLTextAreaElement>,
  ) => {
    const { target } = event;

    setRecipientValue(target.value);

    if (onUpdate) {
      const updatedSetting = {
        ...setting,
        recipients: target.value,
      };

      onUpdate(index, updatedSetting);
    }
  };

  // Set recipients
  if (!!recipients && recipientValue !== recipients) {
    setRecipientValue(recipients);
  }
  const handleS3Method = (e: any) => {
    console.log(e, 'value');
    setS3Method(e);
  };
  const handleAccesskey = (e: any) => {
    setAccessKey(e.target.value);
  };
  const handleSecretkey = (e: any) => {
    setSecretKey(e.target.value);
  };
  const handleIamkey = (e: any) => {
    setIam(e.target.value);
  };

  const handleBucketName = (e: any) => {
    const newBucketName = e.target.value;
    setBucketName(newBucketName);
  };
  return (
    <StyledNotificationMethod>
      <div className="inline-container">
        <StyledInputContainer>
          <div className="input-container">
            <Select
              ariaLabel={t('Delivery method')}
              data-test="select-delivery-method"
              onChange={onMethodChange}
              placeholder={t('Select Delivery Method')}
              options={(options || []).map(
                (method: NotificationMethodOption) => ({
                  label: method,
                  value: method,
                }),
              )}
              value={method}
            />
          </div>
        </StyledInputContainer>

        {method !== undefined && !!onRemove ? (
          <span
            role="button"
            tabIndex={0}
            className="delete-button"
            onClick={() => onRemove(index)}
          >
            <Icons.Trash iconColor={theme.colors.grayscale.base} />
          </span>
        ) : null}
      </div>
      {method === 'S3' && (
        <div className="inline-container">
          <StyledInputContainer>
            <div className="input-container">
              <Select
                ariaLabel={t('S3 methods')}
                data-test="select-delivery-method"
                onChange={handleS3Method}
                placeholder={t('Select S3 Method')}
                options={s3SubTypes.map((option: string) => ({
                  label: option,
                  value: option,
                }))}
                value={s3Method}
              />
            </div>
          </StyledInputContainer>
        </div>
      )}
      {s3Method === 'AWS_S3_credentials' && method !== 'Email' && (
        <div>
          <div className="control-label">{t('Bucket Name')}</div>
          <LabeledErrorBoundInput
            type="text"
            placeholder={t('Type[Bucket Name]')}
            name="bucketName"
            value={bucketName}
            validationMethods={{
              onChange: handleBucketName,
            }}
            css={noBottomMargin}
          />

          <div className="control-label">{t('Access Key')}</div>
          <LabeledErrorBoundInput
            type="password"
            placeholder={t('Type[Access Key]')}
            name="accessKey"
            value={accessKey}
            validationMethods={{
              onChange: handleAccesskey,
            }}
            css={noBottomMargin}
          />
          <div className="control-label">{t('Secret Key')}</div>
          <LabeledErrorBoundInput
            type="password"
            placeholder={t('Type[Secret Key]')}
            name="secretKey"
            value={secretKey}
            validationMethods={{
              onChange: handleSecretkey,
            }}
            css={noBottomMargin}
          />
        </div>
      )}
      {s3Method === 'AWS_S3_IAM' && method !== 'Email' && (
        <>
          <div className="control-label">{t('AWS IAM ROLE')}</div>
          <LabeledErrorBoundInput
            type="password"
            placeholder={t('Type[ AWS IAM ROLE ]')}
            name="bucketName"
            value={iam}
            onChange={e => setIam(e.target.value)}
            validationMethods={{
              onChange: handleIamkey,
            }}
            css={noBottomMargin}
          />
          <div className="control-label">{t('Bucket Name')}</div>
          <LabeledErrorBoundInput
            type="text"
            placeholder="Type[Bucket Name]"
            name="bucketName"
            value={bucketName}
            validationMethods={{
              onChange: handleBucketName,
            }}
            css={noBottomMargin}
          />
        </>
      )}
      {s3Method === 'AWS_S3_pyconfig' && method !== 'Email' && (
        <>
          <div className="control-label">{t('Bucket Name')}</div>
          <LabeledErrorBoundInput
            type="text"
            placeholder="Type[Bucket Name]"
            name="bucketName"
            value={bucketName}
            validationMethods={{
              onChange: handleBucketName,
            }}
            css={noBottomMargin}
          />
        </>
      )}
      {method !== undefined && method === 'Email' ? (
        <StyledInputContainer>
          <div className="control-label">{t(method)}</div>
          <div className="input-container">
            <textarea
              name="recipients"
              value={recipientValue}
              onChange={onRecipientsChange}
            />
          </div>
          <div className="helper">
            {t('Recipients are separated by "," or ";"')}
          </div>
        </StyledInputContainer>
      ) : null}
    </StyledNotificationMethod>
  );
};
