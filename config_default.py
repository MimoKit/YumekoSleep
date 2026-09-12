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
        '开启后发送晚安时会使用用户头像生成表情包并一同发出（默认关闭）。',
        False,
    ),
    'MemeApiUrl': GsStrConfig(
        '表情包后端地址',
        'Meme Generator 服务地址，例如 http://127.0.0.1:2235 或 https://meme.nnlmc.top:2234。',
        'http://127.0.0.1:2235',
    ),
    'EnableThemeWishes': GsBoolConfig(
        '鸣潮风格文案',
        '开启后晚安/早安使用鸣潮风格随机寄语；关闭后使用朴素固定文案。',
        True,
    ),
}
