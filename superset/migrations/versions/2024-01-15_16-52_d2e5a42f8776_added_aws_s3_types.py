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
"""added aws s3 types

Revision ID: d2e5a42f8776
Revises: 931022261b3b
Create Date: 2024-01-15 16:52:10.670855

"""

# revision identifiers, used by Alembic.
revision = 'd2e5a42f8776'
down_revision = '931022261b3b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():

    op.add_column('report_schedule', sa.Column('aws_S3_types', sa.String(length=200), nullable=True))



def downgrade():
    pass
