# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Added aws columns

Revision ID: 931022261b3b
Revises: f3c2d8ec8595
Create Date: 2024-01-15 15:19:52.548672

"""

# revision identifiers, used by Alembic.
revision = '931022261b3b'
down_revision = 'f3c2d8ec8595'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():

    op.add_column('report_schedule', sa.Column('aws_key', sa.String(length=100), nullable=True))
    op.add_column('report_schedule', sa.Column('aws_secretKey', sa.String(length=100), nullable=True))
    op.add_column('report_schedule', sa.Column('aws_arn_role', sa.String(length=200), nullable=True))
    


def downgrade():
   pass
