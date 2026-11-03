"""Make teaching material versions append-only for the runtime role."""

from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        DROP POLICY material_update ON teaching_assets;
        DROP POLICY material_delete ON teaching_assets;
        REVOKE UPDATE, DELETE ON teaching_assets FROM tutor_app;
    """)


def downgrade() -> None:
    op.execute("""
        GRANT UPDATE, DELETE ON teaching_assets TO tutor_app;
        CREATE POLICY material_update ON teaching_assets FOR UPDATE USING (
          EXISTS (SELECT 1 FROM teaching_asset_owners o WHERE o.id=teaching_assets.id
            AND o.tutor_id::text = current_setting('app.tutor_id', true))
        ) WITH CHECK (EXISTS (SELECT 1 FROM teaching_asset_owners o
            WHERE o.id=teaching_assets.id
            AND o.tutor_id::text = current_setting('app.tutor_id', true)));
        CREATE POLICY material_delete ON teaching_assets FOR DELETE USING (
          EXISTS (SELECT 1 FROM teaching_asset_owners o WHERE o.id=teaching_assets.id
            AND o.tutor_id::text = current_setting('app.tutor_id', true))
        );
    """)
