# Pydantic
from pydantic import Field
# models
from youtube_pydantic_models.base_model_config import (
    get_base_model_config
)
from youtube_pydantic_models.base_resource import (
    YoutubeBaseResource
)
from youtube_pydantic_models._parts.id import (
    SearchId
)
from youtube_pydantic_models._parts.snippet import (
    SearchSnippet
)


class YoutubeSearchResource(YoutubeBaseResource):
    model_config = get_base_model_config()

    id: SearchId | None = Field(default=None)
    snippet: SearchSnippet | None = Field(default=None)
