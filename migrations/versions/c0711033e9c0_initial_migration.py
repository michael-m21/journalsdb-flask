"""initial migration

Revision ID: c0711033e9c0
Revises: 
Create Date: 2021-01-30 11:23:51.223110

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c0711033e9c0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "continents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "currency",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("symbol", sa.String(length=3), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol"),
    )
    op.create_table(
        "issn_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("issn_l", sa.String(length=9), nullable=False),
        sa.Column("issn", sa.String(length=9), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "issn_metadata",
        sa.Column("issn_l", sa.String(), nullable=False),
        sa.Column(
            "issn_org_issns", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "crossref_issns", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "issn_org_raw_api", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "crossref_raw_api", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("issn_l"),
    )
    op.create_index(
        "idx_crossref_issns",
        "issn_metadata",
        ["crossref_issns"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        "idx_issn_org_issns",
        "issn_metadata",
        ["issn_org_issns"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_table(
        "issn_temp",
        sa.Column("issn", sa.String(length=9), nullable=False),
        sa.Column("issn_l", sa.String(length=9), nullable=False),
        sa.PrimaryKeyConstraint("issn", "issn_l"),
    )
    op.create_index(op.f("ix_issn_temp_issn_l"), "issn_temp", ["issn_l"], unique=False)
    op.create_table(
        "issn_to_issnl",
        sa.Column("issn", sa.String(length=9), nullable=False),
        sa.Column("issn_l", sa.String(length=9), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("issn", "issn_l"),
    )
    op.create_index(
        op.f("ix_issn_to_issnl_issn_l"), "issn_to_issnl", ["issn_l"], unique=False
    )
    op.create_table(
        "publishers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("synonyms", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("uuid", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("iso", sa.String(length=2), nullable=False),
        sa.Column("iso3", sa.String(length=3), nullable=False),
        sa.Column("continent_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["continent_id"],
            ["continents.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("iso"),
        sa.UniqueConstraint("iso3"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(
        op.f("ix_countries_continent_id"), "countries", ["continent_id"], unique=False
    )
    op.create_table(
        "imprints",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("publisher_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["publisher_id"],
            ["publishers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "linked_issn_l",
        sa.Column("issn_l_primary", sa.String(), nullable=False),
        sa.Column("issn_l_secondary", sa.String(), nullable=False),
        sa.Column("reason", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["issn_l_primary"],
            ["issn_metadata.issn_l"],
        ),
        sa.ForeignKeyConstraint(
            ["issn_l_secondary"],
            ["issn_metadata.issn_l"],
        ),
        sa.PrimaryKeyConstraint("issn_l_primary", "issn_l_secondary"),
    )
    op.create_table(
        "mini_bundles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("issn", sa.Text(), nullable=True),
        sa.Column("publisher_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["publisher_id"],
            ["publishers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "regions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("publisher_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["publisher_id"],
            ["publishers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "apc_price",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("currency_id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=True),
        sa.Column("region_id", sa.Integer(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
        ),
        sa.ForeignKeyConstraint(
            ["currency_id"],
            ["currency.id"],
        ),
        sa.ForeignKeyConstraint(
            ["region_id"],
            ["regions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_apc_price_country_id"), "apc_price", ["country_id"], unique=False
    )
    op.create_index(
        op.f("ix_apc_price_currency_id"), "apc_price", ["currency_id"], unique=False
    )
    op.create_index(
        op.f("ix_apc_price_region_id"), "apc_price", ["region_id"], unique=False
    )
    op.create_index(op.f("ix_apc_price_year"), "apc_price", ["year"], unique=False)
    op.create_table(
        "journals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("issn_l", sa.String(length=9), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("issns", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("synonyms", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("publisher_id", sa.Integer(), nullable=True),
        sa.Column("internal_publisher_id", sa.Text(), nullable=True),
        sa.Column("imprint_id", sa.Integer(), nullable=True),
        sa.Column("discount_waiver_exception", sa.Boolean(), nullable=False),
        sa.Column("uuid", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["imprint_id"],
            ["imprints.id"],
        ),
        sa.ForeignKeyConstraint(
            ["publisher_id"],
            ["publishers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("issn_l"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_index(
        op.f("ix_journals_publisher_id"), "journals", ["publisher_id"], unique=False
    )
    op.create_table(
        "region_countries",
        sa.Column("region_id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
        ),
        sa.ForeignKeyConstraint(
            ["region_id"],
            ["regions.id"],
        ),
        sa.PrimaryKeyConstraint("region_id", "country_id"),
    )
    op.create_table(
        "subscription_price",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("currency_id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=True),
        sa.Column("region_id", sa.Integer(), nullable=True),
        sa.Column("fte_from", sa.Integer(), nullable=True),
        sa.Column("fte_to", sa.Integer(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
        ),
        sa.ForeignKeyConstraint(
            ["currency_id"],
            ["currency.id"],
        ),
        sa.ForeignKeyConstraint(
            ["region_id"],
            ["regions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_subscription_price_country_id"),
        "subscription_price",
        ["country_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_subscription_price_currency_id"),
        "subscription_price",
        ["currency_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_subscription_price_region_id"),
        "subscription_price",
        ["region_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_subscription_price_year"), "subscription_price", ["year"], unique=False
    )
    op.create_table(
        "author_permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("journal_id", sa.Integer(), nullable=True),
        sa.Column("has_policy", sa.Boolean(), nullable=True),
        sa.Column(
            "version_archivable", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "archiving_locations_allowed",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("post_print_embargo", sa.Integer(), nullable=True),
        sa.Column(
            "licence_allowed", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("deposit_statement_required", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("journal_id"),
    )
    op.create_table(
        "extension_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("journal_id", sa.Integer(), nullable=False),
        sa.Column("month", sa.DateTime(), nullable=False),
        sa.Column("requests", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_extension_requests_journal_id"),
        "extension_requests",
        ["journal_id"],
        unique=False,
    )
    op.create_table(
        "journal_apc_price",
        sa.Column("journal_id", sa.Integer(), nullable=False),
        sa.Column("apc_price_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["apc_price_id"],
            ["apc_price.id"],
        ),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.PrimaryKeyConstraint("journal_id", "apc_price_id"),
    )
    op.create_table(
        "journal_metadata",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("journal_id", sa.Integer(), nullable=False),
        sa.Column("author_page_url", sa.Text(), nullable=True),
        sa.Column("editorial_page_url", sa.Text(), nullable=True),
        sa.Column("twitter_id", sa.Text(), nullable=True),
        sa.Column("wikidata_id", sa.Text(), nullable=True),
        sa.Column("society_journal", sa.Boolean(), nullable=True),
        sa.Column("society_journal_name", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "journal_mini_bundle_price",
        sa.Column("mini_bundle_id", sa.Integer(), nullable=False),
        sa.Column("subscription_price_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mini_bundle_id"],
            ["mini_bundles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["subscription_price_id"],
            ["subscription_price.id"],
        ),
        sa.PrimaryKeyConstraint("mini_bundle_id", "subscription_price_id"),
    )
    op.create_table(
        "journal_subjects",
        sa.Column("journal_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["subjects.id"],
        ),
        sa.PrimaryKeyConstraint("journal_id", "subject_id"),
    )
    op.create_table(
        "journal_subscription_price",
        sa.Column("journal_id", sa.Integer(), nullable=False),
        sa.Column("subscription_price_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.ForeignKeyConstraint(
            ["subscription_price_id"],
            ["subscription_price.id"],
        ),
        sa.PrimaryKeyConstraint("journal_id", "subscription_price_id"),
    )
    op.create_table(
        "mini_bundle_journals",
        sa.Column("mini_bundle_id", sa.Integer(), nullable=False),
        sa.Column("journal_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.ForeignKeyConstraint(
            ["mini_bundle_id"],
            ["mini_bundles.id"],
        ),
        sa.PrimaryKeyConstraint("mini_bundle_id", "journal_id"),
    )
    op.create_table(
        "open_access_publishing",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("journal_id", sa.Integer(), nullable=True),
        sa.Column("num_dois", sa.Integer(), nullable=True),
        sa.Column("num_open", sa.Integer(), nullable=True),
        sa.Column("open_rate", sa.Float(), nullable=True),
        sa.Column("num_green", sa.Integer(), nullable=True),
        sa.Column("green_rate", sa.Float(), nullable=True),
        sa.Column("num_bronze", sa.Integer(), nullable=True),
        sa.Column("bronze_rate", sa.Float(), nullable=True),
        sa.Column("num_hybrid", sa.Integer(), nullable=True),
        sa.Column("hybrid_rate", sa.Float(), nullable=True),
        sa.Column("num_gold", sa.Integer(), nullable=True),
        sa.Column("gold_rate", sa.Float(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "open_access_status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("journal_id", sa.Integer(), nullable=True),
        sa.Column("is_in_doaj", sa.Boolean(), nullable=True),
        sa.Column("is_hybrid_journal", sa.Boolean(), nullable=True),
        sa.Column("is_gold_journal", sa.Boolean(), nullable=True),
        sa.Column("is_diamond_oa", sa.Boolean(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "repositories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("journal_id", sa.Integer(), nullable=False),
        sa.Column("endpoint_id", sa.Text(), nullable=False),
        sa.Column("repository_name", sa.Text(), nullable=True),
        sa.Column("institution_name", sa.Text(), nullable=True),
        sa.Column("home_page", sa.Text(), nullable=True),
        sa.Column("pmh_url", sa.Text(), nullable=True),
        sa.Column("num_articles", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["journal_id"],
            ["journals.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_repositories_journal_id"), "repositories", ["journal_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_repositories_journal_id"), table_name="repositories")
    op.drop_table("repositories")
    op.drop_table("open_access_status")
    op.drop_table("open_access_publishing")
    op.drop_table("mini_bundle_journals")
    op.drop_table("journal_subscription_price")
    op.drop_table("journal_subjects")
    op.drop_table("journal_mini_bundle_price")
    op.drop_table("journal_metadata")
    op.drop_table("journal_apc_price")
    op.drop_index(
        op.f("ix_extension_requests_journal_id"), table_name="extension_requests"
    )
    op.drop_table("extension_requests")
    op.drop_table("author_permissions")
    op.drop_index(op.f("ix_subscription_price_year"), table_name="subscription_price")
    op.drop_index(
        op.f("ix_subscription_price_region_id"), table_name="subscription_price"
    )
    op.drop_index(
        op.f("ix_subscription_price_currency_id"), table_name="subscription_price"
    )
    op.drop_index(
        op.f("ix_subscription_price_country_id"), table_name="subscription_price"
    )
    op.drop_table("subscription_price")
    op.drop_table("region_countries")
    op.drop_index(op.f("ix_journals_publisher_id"), table_name="journals")
    op.drop_table("journals")
    op.drop_index(op.f("ix_apc_price_year"), table_name="apc_price")
    op.drop_index(op.f("ix_apc_price_region_id"), table_name="apc_price")
    op.drop_index(op.f("ix_apc_price_currency_id"), table_name="apc_price")
    op.drop_index(op.f("ix_apc_price_country_id"), table_name="apc_price")
    op.drop_table("apc_price")
    op.drop_table("regions")
    op.drop_table("mini_bundles")
    op.drop_table("linked_issn_l")
    op.drop_table("imprints")
    op.drop_index(op.f("ix_countries_continent_id"), table_name="countries")
    op.drop_table("countries")
    op.drop_table("subjects")
    op.drop_table("publishers")
    op.drop_index(op.f("ix_issn_to_issnl_issn_l"), table_name="issn_to_issnl")
    op.drop_table("issn_to_issnl")
    op.drop_index(op.f("ix_issn_temp_issn_l"), table_name="issn_temp")
    op.drop_table("issn_temp")
    op.drop_index("idx_issn_org_issns", table_name="issn_metadata")
    op.drop_index("idx_crossref_issns", table_name="issn_metadata")
    op.drop_table("issn_metadata")
    op.drop_table("issn_history")
    op.drop_table("currency")
    op.drop_table("continents")
    # ### end Alembic commands ###
