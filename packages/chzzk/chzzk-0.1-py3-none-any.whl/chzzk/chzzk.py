import http.client
from json import loads
import asyncio


class BaseLive:
    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path
        self._data = self._fetch_data()

    def _fetch_data(self) -> dict:
        connection = None
        try:
            connection = http.client.HTTPSConnection(self.url)
            connection.request("GET", self.path)
            response = connection.getresponse()

            if response.status == 200:
                data = loads(response.read().decode())
                return data['content']
            else:
                print(f"Error: {response.status} - {response.reason}")
                return {}

        except Exception as e:
            print(f"Exception occurred: {e}")
            return {}

        finally:
            if connection is not None:
                connection.close()

    def live_status(self) -> bool:
        status = self._data.get('status', '')
        return status == "OPEN"

    def _get_live_data_if_open(self, key: str):
        if self.live_status():
            return self._data.get(key)
        else:
            print("Error: This stream is offline")
            return None

    def _get_fetch_live_data_if_close(self, key: str):
        if not self.live_status():
            return self._data.get(key)
        else:
            print("Error: This stream is online")
            return None


class Live(BaseLive):
    def __init__(self, channel_id: str):
        url = "api.chzzk.naver.com"
        path = f"/service/v3/channels/{channel_id}/live-detail"
        super().__init__(url, path)

    def title(self) -> str:
        return self._get_live_data_if_open('liveTitle')

    def category(self) -> str:
        return self._get_live_data_if_open('liveCategoryValue')

    def tags(self) -> list:
        return self._get_live_data_if_open('tags')

    def id(self) -> int:
        return self._get_live_data_if_open('liveId')

    def concurrent_view_count(self) -> int:
        return self._get_live_data_if_open('concurrentUserCount')

    def accumulate_view_count(self) -> int:
        return self._get_live_data_if_open('accumulateCount')

    def clip_active(self) -> bool:
        return self._get_live_data_if_open('clipActive')

    def type(self) -> str:
        return self._get_live_data_if_open('categoryType')

    def default_thumbnail_url(self) -> str:
        return self._get_live_data_if_open('defaultThumbnailImageUrl')

    def image_url(self) -> str:
        return self._get_live_data_if_open('liveImageUrl')

    def adult(self) -> bool:
        return self._get_live_data_if_open('adult')

    class Date:
        def __init__(self, outer_instance: 'Live'):
            self.outer_instance = outer_instance

        def open_date(self) -> str:
            return self.outer_instance._get_live_data_if_open('openDate')

        def open_day(self) -> str:
            date = self.open_date()
            return date.split()[0] if date else ''

        def open_time(self) -> str:
            date = self.open_date()
            return date.split()[1] if date else ''


class Fetch_Live(BaseLive):
    def __init__(self, channel_id: str):
        url = "api.chzzk.naver.com"
        path = f"/service/v3/channels/{channel_id}/live-detail"
        super().__init__(url, path)

    def title(self) -> str:
        return self._get_fetch_live_data_if_close('liveTitle')

    def category(self) -> str:
        return self._get_fetch_live_data_if_close('liveCategoryValue')

    def tags(self) -> list:
        return self._get_fetch_live_data_if_close('tags')

    def id(self) -> int:
        return self._get_fetch_live_data_if_close('liveId')

    def concurrent_view_count(self) -> int:
        return self._get_fetch_live_data_if_close('concurrentUserCount')

    def accumulate_view_count(self) -> int:
        return self._get_fetch_live_data_if_close('accumulateCount')

    def clip_active(self) -> bool:
        return self._get_fetch_live_data_if_close('clipActive')

    def type(self) -> str:
        return self._get_fetch_live_data_if_close('categoryType')

    def default_thumbnail_url(self) -> str:
        return self._get_fetch_live_data_if_close('defaultThumbnailImageUrl')

    def image_url(self) -> str:
        return self._get_fetch_live_data_if_close('liveImageUrl')

    def adult(self) -> bool:
        return self._get_fetch_live_data_if_close('adult')

    class Date:
        def __init__(self, outer_instance: 'Fetch_Live'):
            self.outer_instance = outer_instance

        def open_date(self) -> str:
            return self.outer_instance._get_fetch_live_data_if_close('openDate')

        def open_day(self) -> str:
            date = self.open_date()
            return date.split()[0] if date else ''

        def open_time(self) -> str:
            date = self.open_date()
            return date.split()[1] if date else ''


class Channel(BaseLive):
    def __init__(self, channel_id: str):
        url = "api.chzzk.naver.com"
        path = f"/service/v1/channels/{channel_id}"
        super().__init__(url, path)

    def id(self) -> int:
        return self._data.get('channelId', 0)

    def description(self) -> str:
        return self._data.get('channelDescription', '')

    def follower(self) -> int:
        return self._data.get('followerCount', 0)

    def image_url(self) -> str:
        return self._data.get('channelImageUrl', '')

    def name(self) -> str:
        return self._data.get('channelName', '')

    def subscript(self) -> bool:
        return self._data.get('subscriptionAvailability', False)

    def type(self) -> str:
        return self._data.get('channelType', '')

    def ad_monetization(self) -> bool:
        return self._data.get('adMonetizationAvailability', False)

    def verified(self) -> bool:
        return self._data.get('verifiedMark', False)


class Chzzk:
    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        self.live = Live(channel_id)
        self.fetch_live = Fetch_Live(channel_id)
        self.channel = Channel(channel_id)

    def get_live(self) -> Live:
        return self.live

    def get_fetch_live(self) -> Fetch_Live:
        return self.fetch_live

    def get_channel(self) -> Channel:
        return self.channel
