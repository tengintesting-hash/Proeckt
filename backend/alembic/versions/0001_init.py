from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False, unique=True),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("avatar_url", sa.String(length=255), nullable=True),
        sa.Column("bio", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_users_telegram_id", "users", ["telegram_id"], unique=True)

    op.create_table(
        "channels",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("handle", sa.String(length=64), nullable=False, unique=True),
        sa.Column("avatar_url", sa.String(length=255), nullable=False),
        sa.Column("banner_url", sa.String(length=255), nullable=False),
        sa.Column("bio", sa.String(length=255), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("subscribers_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_channels_owner_id", "channels", ["owner_id"], unique=False)
    op.create_index("ix_channels_handle", "channels", ["handle"], unique=True)

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("channel_id", sa.Integer(), sa.ForeignKey("channels.id"), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("media_url", sa.String(length=255), nullable=True),
        sa.Column("media_type", sa.String(length=32), nullable=True),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("is_repost", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("original_post_id", sa.Integer(), sa.ForeignKey("posts.id"), nullable=True),
        sa.Column("likes_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("dislikes_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("comments_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reposts_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("nsfw_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("uniqueness_score", sa.Float(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_posts_channel_id", "posts", ["channel_id"], unique=False)

    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "reactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("reaction", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("post_id", "user_id", name="uix_post_user"),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("channel_id", sa.Integer(), sa.ForeignKey("channels.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("channel_id", "user_id", name="uix_channel_user"),
    )

    op.create_table(
        "reposts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("channel_id", sa.Integer(), sa.ForeignKey("channels.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "ad_campaigns",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("ad_type", sa.String(length=16), nullable=False),
        sa.Column("media_url", sa.String(length=255), nullable=True),
        sa.Column("cta_text", sa.String(length=64), nullable=True),
        sa.Column("cta_url", sa.String(length=255), nullable=True),
        sa.Column("emoji", sa.String(length=16), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("impressions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "ad_impressions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("campaign_id", sa.Integer(), sa.ForeignKey("ad_campaigns.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("clicked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "ai_thresholds",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("text_threshold", sa.Float(), nullable=False, server_default="0.6"),
        sa.Column("media_threshold", sa.Float(), nullable=False, server_default="0.6"),
        sa.Column("uniqueness_threshold", sa.Float(), nullable=False, server_default="0.7"),
    )


def downgrade() -> None:
    op.drop_table("ai_thresholds")
    op.drop_table("ad_impressions")
    op.drop_table("ad_campaigns")
    op.drop_table("reposts")
    op.drop_table("subscriptions")
    op.drop_table("reactions")
    op.drop_table("comments")
    op.drop_index("ix_posts_channel_id", table_name="posts")
    op.drop_table("posts")
    op.drop_index("ix_channels_handle", table_name="channels")
    op.drop_index("ix_channels_owner_id", table_name="channels")
    op.drop_table("channels")
    op.drop_index("ix_users_telegram_id", table_name="users")
    op.drop_table("users")
