from tests.youtube_client_for_testing import YoutubeClientForTesting


class TestGetChannel(YoutubeClientForTesting):
    def test_get_available_channel(self):
        channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
        channel = self.client.get_channel(
            id=channel_id,
            part="snippet, contentDetails, statistics, topicDetails, status, brandingSettings, contentOwnerDetails"
        )
        data = channel.model_dump(
            by_alias=True,
            exclude_none=True
        )

        assert data['id'] == channel_id
        assert data['snippet']
        assert data['contentDetails']
        assert data['statistics']
        assert data['topicDetails']
        assert data['status']
        assert data['brandingSettings']
        assert data['contentOwnerDetails']
