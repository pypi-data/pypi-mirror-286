# Pydantic
from pydantic import Field
# models
from models.base_model_config import get_base_model_config
from models.resources.base_resource import YoutubeBaseResource
from models.part.snippet import VideoSnippet
from models.part.content_details import VideoContentDetails
from models.part.status import VideoStatus
from models.part.statistics import VideoStatistics
from models.part.player import VideoPlayer
from models.part.topic_details import VideoTopicDetails
from models.part.recording_details import BaseRecordingDetails
from models.part.file_details import BaseFileDetails
from models.part.processing_details import BaseProcessingDetails
from models.part.suggestions import BaseSuggestions
from models.part.live_streaming_details import BaseLiveStreamingDetails
from models.subpart.localization import Localization


class YoutubeVideoResource(YoutubeBaseResource):
    model_config = get_base_model_config()

    id: str | None = Field(default=None)
    snippet: VideoSnippet | None = Field(default=None)
    content_details: VideoContentDetails | None = Field(default=None)
    status: VideoStatus | None = Field(default=None)
    statistics: VideoStatistics | None = Field(default=None)
    player: VideoPlayer | None = Field(default=None)
    topic_details: VideoTopicDetails | None = Field(default=None)
    recording_details: BaseRecordingDetails | None = Field(default=None)
    file_details : BaseFileDetails | None = Field(default=None)
    processing_details: BaseProcessingDetails | None = Field(default=None)
    suggestions: BaseSuggestions | None = Field(default=None)
    live_streaming_details: BaseLiveStreamingDetails | None = Field(default=None)
    localizations: dict[str, Localization] | None = Field(default=None)
