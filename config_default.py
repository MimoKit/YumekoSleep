from __future__ import annotations

from typing import Dict

from gsuid_core.utils.plugins_config.models import (
    GSC,
    GsBoolConfig,
    GsStrConfig,
)

CONFIG_DEFAULT: Dict[str, GSC] = {
    'EnableMeme': GsBoolConfig(
        '表情包回复',
        '开启后发送晚安/早安时会使用用户头像生成表情包并一同发出。',
        True,
    ),
    'MemeApiUrl': GsStrConfig(
        '表情包后端地址',
        'Meme Generator 服务地址，例如 http://127.0.0.1:2235 或 https://meme.nnlmc.top:2234。',
        'http://127.0.0.1:2235',
    ),
}
