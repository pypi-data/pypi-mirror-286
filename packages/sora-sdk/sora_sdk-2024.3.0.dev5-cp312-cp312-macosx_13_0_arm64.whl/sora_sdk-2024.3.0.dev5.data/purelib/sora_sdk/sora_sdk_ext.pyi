from collections.abc import Callable, Sequence
import enum
from typing import Annotated, overload

from numpy.typing import ArrayLike


class Sora:
    def __init__(self, use_hardware_encoder: bool | None = None, openh264: str | None = None) -> None: ...

    def create_connection(self, signaling_urls: list[str], role: str, channel_id: str, client_id: Optional[str] = None, bundle_id: Optional[str] = None, metadata: Optional[dict] = None, signaling_notify_metadata: Optional[dict] = None, audio_source: Optional[SoraTrackInterface] = None, video_source: Optional[SoraTrackInterface] = None, audio: Optional[bool] = None, video: Optional[bool] = None, audio_codec_type: Optional[str] = None, video_codec_type: Optional[str] = None, video_bit_rate: Optional[int] = None, audio_bit_rate: Optional[int] = None, video_vp9_params: Optional[dict] = None, video_av1_params: Optional[dict] = None, video_h264_params: Optional[dict] = None, simulcast: Optional[bool] = None, spotlight: Optional[bool] = None, spotlight_number: Optional[int] = None, simulcast_rid: Optional[str] = None, spotlight_focus_rid: Optional[str] = None, spotlight_unfocus_rid: Optional[str] = None, forwarding_filter: Optional[dict] = None, data_channels: Optional[list[dict]] = None, data_channel_signaling: Optional[bool] = None, ignore_disconnect_websocket: Optional[bool] = None, data_channel_signaling_timeout: Optional[int] = None, disconnect_wait_timeout: Optional[int] = None, websocket_close_timeout: Optional[int] = None, websocket_connection_timeout: Optional[int] = None, audio_streaming_language_code: Optional[str] = None, insecure: Optional[bool] = None, client_cert: Optional[str] = None, client_key: Optional[str] = None, proxy_url: Optional[str] = None, proxy_username: Optional[str] = None, proxy_password: Optional[str] = None, proxy_agent: Optional[str] = None) -> SoraConnection: ...

    def create_audio_source(self, channels: int, sample_rate: int) -> SoraAudioSource: ...

    def create_video_source(self) -> SoraVideoSource: ...

class SoraAudioFrame:
    def __getstate__(self) -> tuple[list[int], int, int, int, int | None]: ...

    def __setstate__(self, arg: tuple[Sequence[int], int, int, int, int | None], /) -> None: ...

    @property
    def samples_per_channel(self) -> int: ...

    @property
    def num_channels(self) -> int: ...

    @property
    def sample_rate_hz(self) -> int: ...

    @property
    def absolute_capture_timestamp_ms(self) -> int | None: ...

    def data(self) -> Annotated[ArrayLike, dict(dtype='int16', shape=(None, None))]: ...

class SoraAudioSinkImpl:
    def __init__(self, track: SoraTrackInterface, output_frequency: int = -1, output_channels: int = 0) -> None: ...

    def __del__(self) -> None: ...

    def read(self, frames: int = 0, timeout: float = 1) -> tuple: ...

    @property
    def on_data(self) -> Callable[[Annotated[ArrayLike, dict(dtype='int16', shape=(None, None))]], None]: ...

    @on_data.setter
    def on_data(self, arg: Callable[[Annotated[ArrayLike, dict(dtype='int16', shape=(None, None))]], None], /) -> None: ...

    @property
    def on_format(self) -> Callable[[int, int], None]: ...

    @on_format.setter
    def on_format(self, arg: Callable[[int, int], None], /) -> None: ...

class SoraAudioSource(SoraTrackInterface):
    @overload
    def on_data(self, data: int, samples_per_channel: int, timestamp: float) -> None: ...

    @overload
    def on_data(self, data: int, samples_per_channel: int) -> None: ...

    @overload
    def on_data(self, ndarray: Annotated[ArrayLike, dict(dtype='int16', shape=(None, None), order='C', device='cpu')], timestamp: float) -> None: ...

    @overload
    def on_data(self, ndarray: Annotated[ArrayLike, dict(dtype='int16', shape=(None, None), order='C', device='cpu')]) -> None: ...

class SoraAudioStreamSinkImpl:
    def __init__(self, track: SoraTrackInterface, output_frequency: int = -1, output_channels: int = 0) -> None: ...

    def __del__(self) -> None: ...

    @property
    def on_frame(self) -> Callable[[SoraAudioFrame], None]: ...

    @on_frame.setter
    def on_frame(self, arg: Callable[[SoraAudioFrame], None], /) -> None: ...

class SoraConnection:
    def connect(self) -> None: ...

    def disconnect(self) -> None: ...

    def send_data_channel(self, label: str, data: bytes) -> bool: ...

    def get_stats(self) -> str: ...

    @property
    def on_set_offer(self) -> Callable[[str], None]: ...

    @on_set_offer.setter
    def on_set_offer(self, arg: Callable[[str], None], /) -> None: ...

    @property
    def on_disconnect(self) -> Callable[[SoraSignalingErrorCode, str], None]: ...

    @on_disconnect.setter
    def on_disconnect(self, arg: Callable[[SoraSignalingErrorCode, str], None], /) -> None: ...

    @property
    def on_notify(self) -> Callable[[str], None]: ...

    @on_notify.setter
    def on_notify(self, arg: Callable[[str], None], /) -> None: ...

    @property
    def on_push(self) -> Callable[[str], None]: ...

    @on_push.setter
    def on_push(self, arg: Callable[[str], None], /) -> None: ...

    @property
    def on_message(self) -> Callable[[str, bytes], None]: ...

    @on_message.setter
    def on_message(self, arg: Callable[[str, bytes], None], /) -> None: ...

    @property
    def on_switched(self) -> Callable[[str], None]: ...

    @on_switched.setter
    def on_switched(self, arg: Callable[[str], None], /) -> None: ...

    @property
    def on_track(self) -> Callable[[SoraMediaTrack], None]: ...

    @on_track.setter
    def on_track(self, arg: Callable[[SoraMediaTrack], None], /) -> None: ...

    @property
    def on_data_channel(self) -> Callable[[str], None]: ...

    @on_data_channel.setter
    def on_data_channel(self, arg: Callable[[str], None], /) -> None: ...

class SoraLoggingSeverity(enum.IntEnum):
    VERBOSE = 0

    INFO = 1

    WARNING = 2

    ERROR = 3

    NONE = 4

class SoraMediaTrack(SoraTrackInterface):
    @property
    def stream_id(self) -> str: ...

class SoraSignalingErrorCode(enum.IntEnum):
    CLOSE_SUCCEEDED = 0

    CLOSE_FAILED = 1

    INTERNAL_ERROR = 2

    INVALID_PARAMETER = 3

    WEBSOCKET_HANDSHAKE_FAILED = 4

    WEBSOCKET_ONCLOSE = 5

    WEBSOCKET_ONERROR = 6

    PEER_CONNECTION_STATE_FAILED = 7

    ICE_FAILED = 8

class SoraTrackInterface:
    @property
    def kind(self) -> str: ...

    @property
    def id(self) -> str: ...

    @property
    def enabled(self) -> bool: ...

    @property
    def state(self) -> SoraTrackState: ...

    def set_enabled(self, enable: bool) -> bool: ...

class SoraTrackState(enum.IntEnum):
    LIVE = 0

    ENDED = 1

class SoraVAD:
    def __init__(self) -> None: ...

    def analyze(self, frame: SoraAudioFrame) -> float: ...

class SoraVideoFrame:
    def data(self) -> Annotated[ArrayLike, dict(dtype='uint8', shape=(None, None, 3))]: ...

class SoraVideoSinkImpl:
    def __init__(self, arg: SoraTrackInterface, /) -> None: ...

    def __del__(self) -> None: ...

    @property
    def on_frame(self) -> Callable[[SoraVideoFrame], None]: ...

    @on_frame.setter
    def on_frame(self, arg: Callable[[SoraVideoFrame], None], /) -> None: ...

class SoraVideoSource(SoraTrackInterface):
    @overload
    def on_captured(self, ndarray: Annotated[ArrayLike, dict(dtype='uint8', shape=(None, None, 3), order='C', device='cpu')]) -> None: ...

    @overload
    def on_captured(self, ndarray: Annotated[ArrayLike, dict(dtype='uint8', shape=(None, None, 3), order='C', device='cpu')], timestamp: float) -> None: ...

    @overload
    def on_captured(self, ndarray: Annotated[ArrayLike, dict(dtype='uint8', shape=(None, None, 3), order='C', device='cpu')], timestamp_us: int) -> None: ...

def enable_libwebrtc_log(arg: SoraLoggingSeverity, /) -> None: ...
