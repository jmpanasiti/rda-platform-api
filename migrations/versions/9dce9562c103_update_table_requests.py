"""update table requests

Revision ID: 9dce9562c103
Revises: 491427851fe3
Create Date: 2023-08-23 10:48:54.989549

"""
# import sqlalchemy as sa
from alembic import op
# from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9dce9562c103'
down_revision = '491427851fe3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Cambiar valores de enum requesttirereasonenum
    # 1. Crear nuevo tipo temporal
    op.execute(
        "CREATE TYPE requesttirereasonenum_new AS ENUM ('WEARING', 'KILOMETERS');")

    # 2. Agregar nuevos valores al enum viejo para migrar los datos actuales
    op.execute(
        "ALTER TYPE requesttirereasonenum ADD VALUE IF NOT EXISTS 'WEARING';")
    op.execute(
        "ALTER TYPE requesttirereasonenum ADD VALUE IF NOT EXISTS 'KILOMETERS';")
    op.execute("COMMIT;")

    # 3. Cambiar valores viejos por los nuevos en los registros existentes
    op.execute(
        "UPDATE requests SET tire_reason = 'KILOMETERS' WHERE tire_reason = 'KMS';")
    op.execute(
        "UPDATE requests SET tire_reason = 'WEARING' WHERE tire_reason = 'DES';")

    # 4. Cambiar el tipo de la columna en la tabla
    op.execute(
        "ALTER TABLE requests \
        ALTER COLUMN tire_reason \
        TYPE requesttirereasonenum_new \
        USING (tire_reason::text::requesttirereasonenum_new);"
    )

    # 5. Eliminar tipo viejo
    op.execute("DROP TYPE requesttirereasonenum;")

    # 6. Renombrar tipo nuevo
    op.execute(
        "ALTER TYPE requesttirereasonenum_new RENAME TO requesttirereasonenum;")

    # Cambiar valores de enum requestvertypeenum
    # 1. Crear nuevo tipo temporal
    op.execute(
        "CREATE TYPE requestvertypeenum_new \
        AS ENUM ('VTV', 'POLICE_VERIFICATION', 'VEHICLE_ENGRAVING', 'CRISTALS_ENGRAVING');"
    )

    # 2. Agregar nuevos valores al enum viejo para migrar los datos actuales
    op.execute(
        "ALTER TYPE requestvertypeenum ADD VALUE IF NOT EXISTS 'POLICE_VERIFICATION';")
    op.execute(
        "ALTER TYPE requestvertypeenum ADD VALUE IF NOT EXISTS 'VEHICLE_ENGRAVING';")
    op.execute(
        "ALTER TYPE requestvertypeenum ADD VALUE IF NOT EXISTS 'CRISTALS_ENGRAVING';")
    op.execute("COMMIT;")

    # 3. Cambiar valores viejos por los nuevos en los registros existentes
    op.execute(
        "UPDATE requests SET verification_type = 'POLICE_VERIFICATION' WHERE verification_type = 'POL';")
    op.execute(
        "UPDATE requests SET verification_type = 'VEHICLE_ENGRAVING' WHERE verification_type = 'AUT';")
    op.execute(
        "UPDATE requests SET verification_type = 'CRISTALS_ENGRAVING' WHERE verification_type = 'CRI';")

    # 4. Cambiar el tipo de la columna en la tabla
    op.execute(
        "ALTER TABLE requests \
        ALTER COLUMN verification_type \
        TYPE requestvertypeenum_new \
        USING (verification_type::text::requestvertypeenum_new);"
    )

    # 5. Eliminar tipo viejo
    op.execute("DROP TYPE requestvertypeenum;")

    # 6. Renombrar tipo nuevo
    op.execute("ALTER TYPE requestvertypeenum_new RENAME TO requestvertypeenum;")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    # Revertir valores en requesttirereasonenum
    # 1. Crear nuevo tipo temporal
    op.execute("CREATE TYPE requesttirereasonenum_old AS ENUM ('DES', 'KMS');")

    # 2. Agregar nuevos valores al enum viejo para migrar los datos actuales
    op.execute("ALTER TYPE requesttirereasonenum ADD VALUE IF NOT EXISTS 'DES';")
    op.execute("ALTER TYPE requesttirereasonenum ADD VALUE IF NOT EXISTS 'KMS';")
    op.execute("COMMIT;")

    # 3. Cambiar valores viejos por los nuevos en los registros existentes
    op.execute(
        "UPDATE requests SET tire_reason = 'KMS' WHERE tire_reason = 'KILOMETERS';")
    op.execute(
        "UPDATE requests SET tire_reason = 'DES' WHERE tire_reason = 'WEARING';")

    # 4. Cambiar el tipo de la columna en la tabla
    op.execute(
        "ALTER TABLE requests \
        ALTER COLUMN tire_reason \
        TYPE requesttirereasonenum_old \
        USING (tire_reason::text::requesttirereasonenum_old);"
    )

    # 5. Eliminar tipo viejo
    op.execute("DROP TYPE requesttirereasonenum;")

    # 6. Renombrar tipo nuevo
    op.execute(
        "ALTER TYPE requesttirereasonenum_old RENAME TO requesttirereasonenum;")

    # Revertir valores en requestvertypeenum
    # 1. Crear nuevo tipo temporal
    op.execute(
        "CREATE TYPE requestvertypeenum_old AS ENUM ('VTV', 'POL', 'AUT', 'CRI');")

    # 2. Agregar nuevos valores al enum viejo para migrar los datos actuales
    op.execute("ALTER TYPE requestvertypeenum ADD VALUE IF NOT EXISTS 'POL';")
    op.execute("ALTER TYPE requestvertypeenum ADD VALUE IF NOT EXISTS 'AUT';")
    op.execute("ALTER TYPE requestvertypeenum ADD VALUE IF NOT EXISTS 'CRI';")
    op.execute("COMMIT;")

    # 3. Cambiar valores viejos por los nuevos en los registros existentes
    op.execute(
        "UPDATE requests \
        SET verification_type = 'POL' \
        WHERE verification_type = 'POLICE_VERIFICATION';"
    )
    op.execute(
        "UPDATE requests \
        SET verification_type = 'AUT' \
        WHERE verification_type = 'VEHICLE_ENGRAVING';"
    )
    op.execute(
        "UPDATE requests \
        SET verification_type = 'CRI' \
        WHERE verification_type = 'CRISTALS_ENGRAVING';"
    )

    # 4. Cambiar el tipo de la columna en la tabla
    op.execute(
        "ALTER TABLE requests \
        ALTER COLUMN verification_type \
        TYPE requestvertypeenum_old USING (verification_type::text::requestvertypeenum_old);"
    )

    # 5. Eliminar tipo viejo
    op.execute("DROP TYPE requestvertypeenum;")

    # 6. Renombrar tipo nuevo
    op.execute("ALTER TYPE requestvertypeenum_old RENAME TO requestvertypeenum;")

    # ### end Alembic commands ###
