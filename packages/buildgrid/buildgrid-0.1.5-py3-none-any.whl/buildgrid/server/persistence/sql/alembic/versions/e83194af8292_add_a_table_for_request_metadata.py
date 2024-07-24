# Copyright (C) 2024 Bloomberg LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Add a table for request metadata

Revision ID: e83194af8292
Revises: 316ad77858af
Create Date: 2024-06-14 12:49:52.934372

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e83194af8292"
down_revision = "316ad77858af"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "request_metadata",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tool_name", sa.String(), nullable=True),
        sa.Column("tool_version", sa.String(), nullable=True),
        sa.Column("invocation_id", sa.String(), nullable=True),
        sa.Column("correlated_invocations_id", sa.String(), nullable=True),
        sa.Column("action_mnemonic", sa.String(), nullable=True),
        sa.Column("target_id", sa.String(), nullable=True),
        sa.Column("configuration_id", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tool_name",
            "tool_version",
            "invocation_id",
            "correlated_invocations_id",
            "action_mnemonic",
            "target_id",
            "configuration_id",
            name="unique_metadata_constraint",
        ),
    )

    # We need to use `batch_alter_table` for SQLite, where `ALTER TABLE` isn't available
    with op.batch_alter_table("operations") as batch_op:
        batch_op.add_column(sa.Column("request_metadata_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_operation_request_metadata", "request_metadata", ["request_metadata_id"], ["id"]
        )

    # Copy the existing data into the new table, and set the foreign keys accordingly
    op.execute(
        """
        INSERT INTO request_metadata (tool_name, tool_version, invocation_id, correlated_invocations_id)
        SELECT DISTINCT tool_name, tool_version, invocation_id, correlated_invocations_id FROM operations
        """
    )
    op.execute(
        """
        UPDATE operations SET request_metadata_id = metadata.id
        FROM (SELECT * FROM request_metadata) as metadata
        WHERE (
            metadata.tool_name = operations.tool_name
            OR (operations.tool_name IS NULL AND metadata.tool_name IS NULL)
        )
        AND (
            metadata.tool_version = operations.tool_version
            OR (operations.tool_version IS NULL AND metadata.tool_version IS NULL)
        )
        AND (
            metadata.invocation_id = operations.invocation_id
            OR (operations.invocation_id IS NULL AND metadata.invocation_id IS NULL)
        )
        AND (
            metadata.correlated_invocations_id = operations.correlated_invocations_id
            OR (operations.correlated_invocations_id IS NULL AND metadata.correlated_invocations_id IS NULL)
        )
        """
    )


def downgrade() -> None:
    # Copy any relevant metadata back into the `operations` table
    op.execute(
        """
        UPDATE operations
        SET
            tool_name = metadata.tool_name,
            tool_version = metadata.tool_version,
            invocation_id = metadata.invocation_id,
            correlated_invocations_id = metadata.correlated_invocations_id
        FROM (SELECT * FROM request_metadata) AS metadata
        WHERE metadata.id = operations.request_metadata_id;
        """
    )

    with op.batch_alter_table("operations") as batch_op:
        batch_op.drop_constraint("fk_operation_request_metadata", type_="foreignkey")
        batch_op.drop_column("request_metadata_id")

    op.drop_table("request_metadata")
