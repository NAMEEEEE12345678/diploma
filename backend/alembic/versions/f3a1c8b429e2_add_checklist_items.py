from alembic import op
import sqlalchemy as sa
revision='f3a1c8b429e2'; down_revision='e2b9c5f210d1'; branch_labels=None; depends_on=None
def upgrade():
 op.create_table('checklist_items',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('user_id',sa.Integer(),sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False),sa.Column('base_key',sa.String(80)),sa.Column('title',sa.String(180)),sa.Column('checked',sa.Boolean(),nullable=False,server_default=sa.false()),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.text('now()')),sa.UniqueConstraint('user_id','base_key',name='uq_checklist_base'))
 op.create_index(op.f('ix_checklist_items_user_id'),'checklist_items',['user_id'])
def downgrade():
 op.drop_index(op.f('ix_checklist_items_user_id'),table_name='checklist_items')
 op.drop_table('checklist_items')
