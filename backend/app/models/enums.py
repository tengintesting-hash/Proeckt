import enum


class Role(str, enum.Enum):
    user = "USER"
    channel_owner = "CHANNEL_OWNER"
    channel_moderator = "CHANNEL_MODERATOR"
    moderator = "MODERATOR"
    admin = "ADMIN"


class PostStatus(str, enum.Enum):
    pending_ai_check = "pending_ai_check"
    published = "published"
    pending_review = "pending_review"
    blocked = "blocked"


class PostCategory(str, enum.Enum):
    casino = "casino"
    sport = "sport"
    gambling = "gambling"
    news = "news"
    other = "other"


class ReactionType(str, enum.Enum):
    like = "like"
    dislike = "dislike"


class FeedType(str, enum.Enum):
    recommended = "recommended"
    new = "new"
    popular = "popular"


class AdType(str, enum.Enum):
    banner = "banner"
    video = "video"


class ModerationDecision(str, enum.Enum):
    safe = "SAFE"
    review = "REVIEW"
    block = "BLOCK"
