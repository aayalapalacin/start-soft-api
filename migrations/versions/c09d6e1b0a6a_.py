"""empty message

Revision ID: c09d6e1b0a6a
Revises: 049703462ecd
Create Date: 2024-08-21 18:14:28.151337

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c09d6e1b0a6a'
down_revision = '049703462ecd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choices', schema=None) as batch_op:
        batch_op.alter_column('choice_type',
               existing_type=postgresql.ENUM('INSURANCE_SALES', 'WEB_DESIGN', 'BUSINESS_DEV_MARKETING', 'REAL_ESTATE', name='choicetype'),
               type_=sa.String(length=40),
               existing_nullable=False)

    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=postgresql.ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', name='statusenum'),
               type_=sa.String(length=30),
               existing_nullable=False)

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=postgresql.ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', name='statusenum'),
               type_=sa.String(length=30),
               existing_nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=postgresql.ENUM('CLIENT', 'CONTRACTOR', name='userrole'),
               type_=sa.String(length=30),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.String(length=30),
               type_=postgresql.ENUM('CLIENT', 'CONTRACTOR', name='userrole'),
               existing_nullable=False)

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.String(length=30),
               type_=postgresql.ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', name='statusenum'),
               existing_nullable=False)

    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.String(length=30),
               type_=postgresql.ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', name='statusenum'),
               existing_nullable=False)

    with op.batch_alter_table('choices', schema=None) as batch_op:
        batch_op.alter_column('choice_type',
               existing_type=sa.String(length=40),
               type_=postgresql.ENUM('INSURANCE_SALES', 'WEB_DESIGN', 'BUSINESS_DEV_MARKETING', 'REAL_ESTATE', name='choicetype'),
               existing_nullable=False)

    # ### end Alembic commands ###
