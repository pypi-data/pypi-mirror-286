from Grindr.client.web.web_base import ClientRoute, URLTemplate, BodyParams
from Grindr.client.web.web_settings import GRINDR_V3_1


class SetSendReactionRouteBody(BodyParams):
    conversationId: str
    messageId: str
    reactionType: int = 1


class SetProfileDetailsRoute(
    ClientRoute[
        "POST",
        URLTemplate(GRINDR_V3_1, "/me/profile"),
        None,
        SetSendReactionRouteBody,
        None
    ]
):
    """
    Set profile details

    """

