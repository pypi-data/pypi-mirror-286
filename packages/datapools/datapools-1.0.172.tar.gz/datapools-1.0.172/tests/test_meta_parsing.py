import sys
import os
from pathlib import Path

from .fixtures import *
from datapools.worker.plugins.base_plugin import BasePlugin, BaseTag


def get_data_abs_path(name):
    base_path = Path(__file__).parent
    return (base_path / f"data/{name}").resolve()


def get_content(name):
    with open(get_data_abs_path(name), "rb") as f:
        return f.read()


def test_image_datetime_parsing():
    assert BasePlugin.parse_image_datetime(get_content("empty_meta.jpg")) is None
    assert BasePlugin.parse_image_datetime(get_content("with_createdate.jpg")) == 1721901600  # 2024-07-25 10:00:00


def test_image_copyright_parsing():
    assert BasePlugin.parse_image_tag(get_content("empty_meta.jpg")) is None

    tag = BasePlugin.parse_image_tag(get_content("with_copyright.jpg"))
    assert isinstance(tag, BaseTag)
    assert str(tag) == "asd"
    assert tag.is_keepout() is False


def test_audio_datetime_parsing():
    assert BasePlugin.parse_audio_datetime(get_content("empty_meta.mp3")) is None
    assert BasePlugin.parse_audio_datetime(get_content("with_datetime.mp3")) == 1721901600  # 2024-07-25 10:00:00


def test_audio_tag_parsing():
    assert BasePlugin.parse_audio_tag(get_content("empty_meta.mp3")) is None
    tag = BasePlugin.parse_audio_tag(get_content("with_copyright.mp3"))
    assert isinstance(tag, BaseTag)
    assert str(tag) == "asd"
    assert tag.is_keepout() is False
