import sqlalchemy as sa
from app.db import metadata

prompts = sa.Table(
    "prompts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("act_ru", sa.String, nullable=False),
    sa.Column("prompt_ru", sa.Text, nullable=False),
    sa.Column("act_en", sa.String, nullable=False),
    sa.Column("prompt_en", sa.Text, nullable=False),
)