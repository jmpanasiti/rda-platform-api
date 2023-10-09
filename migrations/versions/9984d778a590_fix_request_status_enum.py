"""Fix request status enum

Revision ID: 9984d778a590
Revises: 8c8bcfc693d1
Create Date: 2023-09-14 17:39:05.523842

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '9984d778a590'
down_revision = '8c8bcfc693d1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Crear nuevo tipo temporal
    op.execute(
        "CREATE TYPE requeststatusenum_new\
            AS ENUM ('OPEN', 'COMPLETED', 'CANCELLED', 'APPOINTMENT_ASSIGNED', 'ARCHIVED',\
            'AUDITED', 'RETAINED', 'CREATED', 'WAITING', 'CLOSED', 'APPROVED');"
    )

    # 2. Agregar nuevos valores al enum viejo para migrar los datos actuales
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'OPEN';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'COMPLETED';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'CANCELLED';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'APPOINTMENT_ASSIGNED';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'ARCHIVED';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'AUDITED';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'RETAINED';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'CREATED';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'WAITING';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'CLOSED';"
    )
    op.execute(
        "ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'APPROVED';"
    )

    op.execute("COMMIT;")

    # 3. Cambiar valores viejos por los nuevos en los registros existentes
    op.execute(
        "UPDATE requests SET status = 'OPEN' WHERE status = 'DEFAULT';"
    )

    # 4. Cambiar el tipo de la columna en la tabla
    op.execute(
        "ALTER TABLE requests \
        ALTER COLUMN status \
        TYPE requeststatusenum_new \
        USING (status::text::requeststatusenum_new);"
    )

    # 5. Eliminar tipo viejo
    op.execute("DROP TYPE requeststatusenum;")

    # 6. Renombrar tipo nuevo
    op.execute(
        "ALTER TYPE requeststatusenum_new RENAME TO requeststatusenum;")


def downgrade() -> None:
    # Revertir valores en requeststatusenum
    # 1. Crear nuevo tipo temporal
    op.execute(
        "CREATE TYPE requeststatusenum_old AS ENUM ('APPROVED', 'DEFAULT');")

    # 2. Agregar nuevos valores al enum viejo para migrar los datos actuales
    op.execute("ALTER TYPE requeststatusenum ADD VALUE IF NOT EXISTS 'DEFAULT';")
    op.execute("COMMIT;")

    # 3. Cambiar valores viejos por los nuevos en los registros existentes
    op.execute(
        "UPDATE requests SET status = 'DEFAULT' WHERE status <> 'APPROVED';"
    )

    # 4. Cambiar el tipo de la columna en la tabla
    op.execute(
        "ALTER TABLE requests \
        ALTER COLUMN status \
        TYPE requeststatusenum_old \
        USING (status::text::requeststatusenum_old);"
    )

    # 5. Eliminar tipo viejo
    op.execute("DROP TYPE requeststatusenum;")

    # 6. Renombrar tipo nuevo
    op.execute(
        "ALTER TYPE requeststatusenum_old RENAME TO requeststatusenum;")
