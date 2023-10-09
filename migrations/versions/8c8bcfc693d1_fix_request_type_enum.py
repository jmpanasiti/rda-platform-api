"""Fix request type enum

Revision ID: 8c8bcfc693d1
Revises: 4be7ca93c654
Create Date: 2023-09-14 17:01:18.764136

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '8c8bcfc693d1'
down_revision = '4be7ca93c654'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Crear nuevo tipo temporal
    op.execute(
        "CREATE TYPE requesttypeenum_new AS ENUM ('PREVENTIVE', 'CORRECTIVE', 'VERIFICATIONS', 'TIRES');"
    )

    # 2. Agregar nuevos valores al enum viejo para migrar los datos actuales
    op.execute(
        "ALTER TYPE requesttypeenum ADD VALUE IF NOT EXISTS 'PREVENTIVE';"
    )
    op.execute(
        "ALTER TYPE requesttypeenum ADD VALUE IF NOT EXISTS 'CORRECTIVE';"
    )
    op.execute(
        "ALTER TYPE requesttypeenum ADD VALUE IF NOT EXISTS 'VERIFICATIONS';"
    )
    op.execute(
        "ALTER TYPE requesttypeenum ADD VALUE IF NOT EXISTS 'TIRES';"
    )
    op.execute("COMMIT;")

    # 3. Cambiar valores viejos por los nuevos en los registros existentes
    op.execute(
        "UPDATE requests SET type = 'PREVENTIVE' WHERE type = 'PRE';"
    )
    op.execute(
        "UPDATE requests SET type = 'CORRECTIVE' WHERE type = 'COR';"
    )
    op.execute(
        "UPDATE requests SET type = 'VERIFICATIONS' WHERE type = 'VER';"
    )
    op.execute(
        "UPDATE requests SET type = 'TIRES' WHERE type = 'GOM';"
    )

    # 4. Cambiar el tipo de la columna en la tabla
    op.execute(
        "ALTER TABLE requests \
        ALTER COLUMN type \
        TYPE requesttypeenum_new \
        USING (type::text::requesttypeenum_new);"
    )

    # 5. Eliminar tipo viejo
    op.execute("DROP TYPE requesttypeenum;")

    # 6. Renombrar tipo nuevo
    op.execute(
        "ALTER TYPE requesttypeenum_new RENAME TO requesttypeenum;")


def downgrade() -> None:
    # Revertir valores en requesttypeenum
    # 1. Crear nuevo tipo temporal
    op.execute(
        "CREATE TYPE requesttypeenum_old AS ENUM ('PRE', 'COR', 'VER', 'GOM');")

    # 2. Agregar nuevos valores al enum viejo para migrar los datos actuales
    op.execute("ALTER TYPE requesttypeenum ADD VALUE IF NOT EXISTS 'PRE';")
    op.execute("ALTER TYPE requesttypeenum ADD VALUE IF NOT EXISTS 'COR';")
    op.execute("ALTER TYPE requesttypeenum ADD VALUE IF NOT EXISTS 'VER';")
    op.execute("ALTER TYPE requesttypeenum ADD VALUE IF NOT EXISTS 'GOM';")
    op.execute("COMMIT;")

    # 3. Cambiar valores viejos por los nuevos en los registros existentes
    op.execute(
        "UPDATE requests SET type = 'PRE' WHERE type = 'PREVENTIVE';"
    )
    op.execute(
        "UPDATE requests SET type = 'COR' WHERE type = 'CORRECTIVE';"
    )
    op.execute(
        "UPDATE requests SET type = 'VER' WHERE type = 'VERIFICATIONS';"
    )
    op.execute(
        "UPDATE requests SET type = 'GOM' WHERE type = 'TIRES';"
    )

    # 4. Cambiar el tipo de la columna en la tabla
    op.execute(
        "ALTER TABLE requests \
        ALTER COLUMN type \
        TYPE requesttypeenum_old \
        USING (type::text::requesttypeenum_old);"
    )

    # 5. Eliminar tipo viejo
    op.execute("DROP TYPE requesttypeenum;")

    # 6. Renombrar tipo nuevo
    op.execute(
        "ALTER TYPE requesttypeenum_old RENAME TO requesttypeenum;")
