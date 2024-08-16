"""empty message

Revision ID: 0fe8d3aebb0a
Revises: 8662a5111496
Create Date: 2024-08-16 01:21:31.187368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fe8d3aebb0a'
down_revision = '8662a5111496'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=300), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('role', sa.Enum('CLIENT', 'CONTRACTOR', name='userrole'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'IN_PROGRESS', 'COMPLETED', name='statusenum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('completion_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('choices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('choice_type', sa.Enum('INSURANCE_SALES', 'WEB_DESIGN', 'BUSINESS_DEV_MARKETING', 'REAL_ESTATE', name='choicetype'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contracts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('contractor_id', sa.Integer(), nullable=False),
    sa.Column('terms', sa.Text(), nullable=False),
    sa.Column('client_signature', sa.Boolean(), nullable=False),
    sa.Column('contractor_signature', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['contractor_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('contractor_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'IN_PROGRESS', 'COMPLETED', name='statusenum'), nullable=False),
    sa.Column('completion_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['contractor_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=300), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('tasks')
    op.drop_table('contracts')
    op.drop_table('choices')
    op.drop_table('projects')
    op.drop_table('users')
    # ### end Alembic commands ###
