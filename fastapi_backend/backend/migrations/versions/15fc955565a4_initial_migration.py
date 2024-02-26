"""Initial migration

Revision ID: 15fc955565a4
Revises: 
Create Date: 2024-10-16 23:43:16.406631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15fc955565a4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fastapi_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('second_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False, comment='Is the user a superuser?'),
    sa.Column('is_confirmed', sa.Boolean(), nullable=False, comment='Has the user confirmed their email?'),
    sa.Column('is_deleted', sa.Boolean(), nullable=False, comment='Has this user been deleted?'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('fastapi_user_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Integer(), nullable=False),
    sa.Column('is_successfully', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['fastapi_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute(
        '''
            CREATE OR REPLACE FUNCTION prevent_log_update()
            RETURNS TRIGGER AS $$
            BEGIN
                RAISE EXCEPTION 'Изменения в таблице fastapi_user_log запрещены';
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;
        '''
    )
    op.execute(
        '''
            CREATE TRIGGER prevent_log_entries_update
            BEFORE UPDATE ON fastapi_user_log
            FOR EACH ROW EXECUTE PROCEDURE prevent_log_update();
        '''
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DROP TRIGGER IF EXISTS prevent_log_entries_update ON log_entries')
    op.execute('DROP FUNCTION IF EXISTS prevent_log_update')
    op.drop_table('fastapi_user_log')
    op.drop_table('fastapi_user')
    # ### end Alembic commands ###