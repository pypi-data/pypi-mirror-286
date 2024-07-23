"""A simple library for talking to a Jellyfin server."""

import urllib
from dataclasses import dataclass
from typing import Any, Final, Required, TypedDict, cast

from aiohttp import ClientResponseError, ClientSession
from mashumaro.codecs.basic import BasicDecoder

from .const import ImageType, ItemType

DEFAULT_FIELDS: Final[str] = (
    "Path,Genres,SortName,Studios,Writer,Taglines,LocalTrailerCount,"
    "OfficialRating,CumulativeRunTimeTicks,ItemCounts,"
    "Metascore,AirTime,DateCreated,People,Overview,"
    "CriticRating,CriticRatingSummary,Etag,ShortOverview,ProductionLocations,"
    "Tags,ProviderIds,ParentId,RemoteTrailers,SpecialEpisodeNumbers,"
    "MediaSources,VoteCount,RecursiveItemCount,PrimaryImageAspectRatio"
)


class NotFound(Exception):
    """Raised when media cannot be found."""


class MediaStream(TypedDict, total=False):
    """Information about a Jellyfin stream."""

    Channels: int
    Codec: str


class MediaSource(TypedDict, total=False):
    """Information about a Jellyfin media source."""

    Path: str


class ArtistItem(TypedDict):
    """Information about a relationship between media and an artist."""

    Id: str
    Name: str


class UserData(TypedDict, total=False):
    """Metadata that is specific to the logged in user, like favorites."""

    IsFavorite: bool


class MediaLibrary(TypedDict, total=False):
    """JSON data describing a single media library."""

    Id: Required[str]
    Name: Required[str]
    CollectionType: str


class MediaLibraries(TypedDict):
    """JSON data describing a collection of media libraries."""

    Items: list[MediaLibrary]
    TotalRecordCount: int
    StartIndex: int


class MediaItem(TypedDict, total=False):
    """JSON data describing a single media item."""

    Id: Required[str]
    Type: ItemType
    Name: str
    MediaType: str
    IndexNumber: int
    SortName: str
    AlbumArtist: str
    Overview: str
    ProductionYear: int
    ProviderIds: dict[str, str]
    CanDownload: bool
    RunTimeTicks: int
    MediaStreams: list[MediaStream]
    AlbumId: str
    Album: str
    ParentIndexNumber: int
    ArtistItems: list[ArtistItem]
    ImageTags: dict[ImageType, str]
    BackdropImageTags: list[str]
    UserData: UserData
    AlbumArtists: list[ArtistItem]
    MediaSources: list[MediaSource]


class MediaItems(TypedDict):
    """JSON data describing a collection of media items."""

    Items: list[MediaItem]
    TotalRecordCount: int
    StartIndex: int


class Artist(MediaItem, TypedDict, total=False):
    """JSON data describing a single artist."""


class Artists(TypedDict):
    """JSON data describing a collection of artists."""

    Items: list[Artist]
    TotalRecordCount: int
    StartIndex: int


class Album(MediaItem, TypedDict, total=False):
    """JSON data describing a single album."""


class Albums(TypedDict):
    """JSON data describing a collection of albums."""

    Items: list[Album]
    TotalRecordCount: int
    StartIndex: int


class Track(MediaItem, TypedDict, total=False):
    """JSON data describing a single track."""


class Tracks(TypedDict):
    """JSON data describing a collection of tracks."""

    Items: list[Track]
    TotalRecordCount: int
    StartIndex: int


class Playlist(MediaItem, TypedDict, total=False):
    """JSON data describing a single playlist."""


class Playlists(TypedDict):
    """JSON data describing a collection of playlists."""

    Items: list[Track]
    TotalRecordCount: int
    StartIndex: int


@dataclass
class SessionConfiguration:
    """Configuration needed to connect to a Jellyfin server."""

    session: ClientSession
    url: str
    app_name: str
    app_version: str
    device_name: str
    device_id: str

    verify_ssl: bool = True

    @property
    def user_agent(self) -> str:
        """Get the user agent for this session."""
        return f"{self.app_name}/{self.app_version}"

    def authentication_header(self, api_token: str | None = None) -> str:
        """Build the Authorization header for this session."""
        params = {
            "Client": self.app_name,
            "Device": self.device_name,
            "DeviceId": self.device_id,
            "Version": self.app_version,
        }
        if api_token:
            params["Token"] = api_token
        param_line = ", ".join(f'{k}="{v}"' for k, v in params.items())
        return f"MediaBrowser {param_line}"


class Connection:
    """A connection to a Jellyfin server."""

    def __init__(self, session_config: SessionConfiguration, user_id: str, access_token: str):
        """Initialise the connection instance."""
        self._session_config = session_config
        self._session = session_config.session
        self.base_url = session_config.url.rstrip("/")
        self._user_id = user_id
        self._access_token = access_token

        # These will go away when we transition to dataclasses
        self._artists_decoder = BasicDecoder(Artists)
        self._artist_decoder = BasicDecoder(Artist)
        self._albums_decoder = BasicDecoder(Albums)
        self._album_decoder = BasicDecoder(Album)
        self._tracks_decoder = BasicDecoder(Tracks)
        self._track_decoder = BasicDecoder(Track)
        self._playlists_decoder = BasicDecoder(Playlists)
        self._playlist_decoder = BasicDecoder(Playlist)

    async def _get_json(self, url: str, params: dict[str, str | int]) -> dict[str, Any]:
        try:
            resp = await self._session.get(
                f"{self.base_url}{url}",
                params=params,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": self._session_config.user_agent,
                    "Authorization": self._session_config.authentication_header(self._access_token),
                },
                ssl=self._session_config.verify_ssl,
                raise_for_status=True,
            )
        except ClientResponseError as e:
            if e.status == 404:
                raise NotFound("Resource not found")
            raise

        return cast(dict[str, Any], await resp.json())

    async def get_media_folders(self, fields: str | None = None) -> MediaLibraries:
        """Fetch a list of media libraries."""
        params: dict[str, str | int] = {}
        if fields:
            params["fields"] = fields
        resp = await self._get_json("/Items", params=params)
        return cast(MediaLibraries, resp)

    async def artists(
        self,
        library_id: str | None = None,
        search_term: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[str] | None = None,
        enable_user_data: bool = False,
    ) -> Artists:
        """Fetch a list of artists."""
        params: dict[str, str | int] = {
            "recursive": "true",
        }

        if library_id:
            params["parentId"] = library_id

        if search_term:
            params["searchTerm"] = search_term

        if start_index:
            params["startIndex"] = start_index

        if limit:
            params["limit"] = limit

        if enable_user_data:
            params["enableUserData"] = "true"

        if fields:
            params["fields"] = ",".join(fields)

        resp = await self._get_json(
            "/Artists",
            params=params,
        )
        return self._artists_decoder.decode(resp)

    async def albums(
        self,
        library_id: str | None = None,
        search_term: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[str] | None = None,
        enable_user_data: bool = False,
    ) -> Albums:
        """Return all library matching query."""
        params: dict[str, str | int] = {
            "includeItemTypes": "MusicAlbum",
            "recursive": "true",
        }

        if library_id:
            params["parentId"] = library_id

        if search_term:
            params["searchTerm"] = search_term

        if start_index:
            params["startIndex"] = start_index

        if limit:
            params["limit"] = limit

        if enable_user_data:
            params["enableUserData"] = "true"

        if fields:
            params["fields"] = ",".join(fields)

        resp = await self._get_json(
            "/Items",
            params=params or {},
        )
        return self._albums_decoder.decode(resp)

    async def tracks(
        self,
        library_id: str | None = None,
        search_term: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[str] | None = None,
        enable_user_data: bool = False,
    ) -> Tracks:
        """Return all library matching query."""
        params: dict[str, str | int] = {
            "includeItemTypes": "Audio",
            "recursive": "true",
        }

        if library_id:
            params["parentId"] = library_id

        if search_term:
            params["searchTerm"] = search_term

        if start_index:
            params["startIndex"] = start_index

        if limit:
            params["limit"] = limit

        if enable_user_data:
            params["enableUserData"] = "true"

        if fields:
            params["fields"] = ",".join(fields)

        resp = await self._get_json(
            "/Items",
            params=params or {},
        )
        return self._tracks_decoder.decode(resp)

    async def playlists(
        self,
        library_id: str | None = None,
        search_term: str | None = None,
        start_index: int | None = None,
        limit: int | None = None,
        fields: list[str] | None = None,
        enable_user_data: bool = False,
    ) -> Playlists:
        """Return all library matching query."""
        params: dict[str, str | int] = {
            "includeItemTypes": "Playlist",
            "recursive": "true",
        }

        if library_id:
            params["parentId"] = library_id

        if search_term:
            params["searchTerm"] = search_term

        if start_index:
            params["startIndex"] = start_index

        if limit:
            params["limit"] = limit

        if enable_user_data:
            params["enableUserData"] = "true"

        if fields:
            params["fields"] = ",".join(fields)

        resp = await self._get_json(
            "/Items",
            params=params or {},
        )
        return self._playlists_decoder.decode(resp)

    async def get_artist(self, artist_id: str) -> Artist:
        """Fetch all data for a single artist."""
        artist = self._artist_decoder.decode(
            await self._get_json(
                f"/Users/{self._user_id}/Items/{artist_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            ),
        )
        if artist["Type"] != ItemType.MusicArtist:
            raise NotFound(artist_id)
        return artist

    async def get_album(self, album_id: str) -> Album:
        """Fetch all data for a single album."""
        album = self._album_decoder.decode(
            await self._get_json(
                f"/Users/{self._user_id}/Items/{album_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            )
        )
        if album["Type"] != ItemType.MusicAlbum:
            raise NotFound(album_id)
        return album

    async def get_track(self, track_id: str) -> Track:
        """Fetch all data for a single track."""
        track = self._track_decoder.decode(
            await self._get_json(
                f"/Users/{self._user_id}/Items/{track_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            ),
        )
        if track["Type"] != ItemType.Audio:
            raise NotFound(track_id)
        return track

    async def get_playlist(self, playlist_id: str) -> Playlist:
        """Fetch all data for a single playlist."""
        playlist = self._playlist_decoder.decode(
            await self._get_json(
                f"/Users/{self._user_id}/Items/{playlist_id}",
                params={
                    "Fields": DEFAULT_FIELDS,
                },
            ),
        )
        if playlist["Type"] != ItemType.Playlist:
            raise NotFound(playlist_id)
        return playlist

    async def get_suggested_tracks(self) -> Tracks:
        """Return suggested tracks."""
        return self._tracks_decoder.decode(
            await self._get_json(
                "/Items/Suggestions",
                {
                    "mediaType": "Audio",
                    "type": "Audio",
                    "limit": 50,
                    "enableUserData": "true",
                },
            )
        )

    async def get_similar_tracks(
        self,
        track_id: str,
        limit: int | None = None,
        fields: list[str] | None = None,
    ) -> Tracks:
        """Return similar tracks."""
        params: dict[str, str | int] = {}

        if limit:
            params["limit"] = limit

        if fields:
            params["fields"] = ",".join(fields)

        resp = await self._get_json(
            f"/Items/{track_id}/Similar",
            params=params or {},
        )
        return self._tracks_decoder.decode(resp)

    def _build_url(self, url: str, params: dict[str, str | int]) -> str:
        assert url.startswith("/")

        if "api_key" not in params:
            params["api_key"] = self._access_token

        encoded = urllib.parse.urlencode(params)

        return f"{self.base_url}{url}?{encoded}"

    def artwork(
        self,
        item_id: str,
        image_type: ImageType,
        max_width: int | None = None,
        extension: str | None = None,
        index: int | None = None,
    ) -> str:
        """Given a TrackId, return a URL to some artwork."""
        params: dict[str, str | int] = {}
        if max_width:
            params["maxWidth"] = max_width
        if extension:
            params["format"] = extension
        if index is None:
            return self._build_url(f"/Items/{item_id}/Images/{image_type!s}", params)
        return self._build_url(f"/Items/{item_id}/Images/{image_type!s}/{index}", params)

    def audio_url(
        self,
        item_id: str,
        container: str | None = None,
        audio_codec: str | None = None,
        max_streaming_bitrate: int = 140000000,
    ) -> str:
        """Given a TrackId, return a URL to stream from."""
        params: dict[str, str | int] = {
            "UserId": self._user_id,
            "DeviceId": self._session_config.device_id,
            "MaxStreamingBitrate": max_streaming_bitrate,
        }

        if container:
            params["Container"] = container

        if audio_codec:
            params["AudioCodec"] = audio_codec

        return self._build_url(f"/Audio/{item_id}/universal", params)


async def authenticate_by_name(
    session_config: SessionConfiguration, username: str, password: str = ""
) -> Connection:
    """Authenticate against a server with a username and password and return a connection."""
    session = ClientSession(
        base_url=session_config.url,
    )
    async with session:
        res = await session.post(
            "/Users/AuthenticateByName",
            json={"Username": username, "Pw": password},
            headers={
                "Content-Type": "application/json",
                "User-Agent": session_config.user_agent,
                "Authorization": session_config.authentication_header(),
            },
            raise_for_status=True,
        )
        user_session = await res.json()

    user = user_session["User"]

    return Connection(session_config, user["Id"], user_session["AccessToken"])
