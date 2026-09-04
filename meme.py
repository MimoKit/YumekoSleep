from __future__ import annotations

import re
from typing import Optional
import httpx

from gsuid_core.logger import logger
from gsuid_core.models import Event

LOG_PREFIX = '[晚安插件]'
MEME_KEY = 'kurogames_good_night'


def get_user_avatar_url(ev: Event) -> str:
    """获取用户头像 URL"""
    user_id = str(ev.user_id).strip()

    # 1. 尝试从事件对象或 sender 中读取已有头像
    for attr in ('user_avatar', 'avatar', 'user_icon'):
        val = getattr(ev, attr, None)
        if val and isinstance(val, str) and val.startswith(('http://', 'https://')):
            return val

    sender = getattr(ev, 'sender', None)
    if isinstance(sender, dict):
        for field in ('avatar', 'user_avatar', 'user_icon'):
            val = sender.get(field)
            if val and isinstance(val, str) and val.startswith(('http://', 'https://')):
                return val

    # 2. 如果是纯数字 QQ 号，使用高清 QQ 头像 API
    if re.fullmatch(r'\d{5,12}', user_id):
        return f'https://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640'

    # 3. 兜底默认 QQ 机器人头像
    return f'https://q.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640'


async def generate_good_night_meme(avatar_url: str, base_url: str) -> Optional[bytes]:
    """请求 Meme Generator 服务生成 kurogames_good_night 表情包"""
    if not base_url:
        return None

    clean_base = base_url.rstrip('/')
    endpoint = f'{clean_base}/memes/{MEME_KEY}/'

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # 1. 下载用户头像二进制数据
            avatar_resp = await client.get(avatar_url, headers={'User-Agent': 'Mozilla/5.0'})
            if avatar_resp.status_code != 200 or not avatar_resp.content:
                logger.warning(f'{LOG_PREFIX} 下载用户头像失败, HTTP {avatar_resp.status_code}: {avatar_url}')
                return None
            avatar_bytes = avatar_resp.content

            # 2. 调用 meme_generator 生成表情包
            files = {'images': ('avatar.jpg', avatar_bytes, 'image/jpeg')}
            data = {'texts': []}
            meme_resp = await client.post(endpoint, files=files, data=data)

            if meme_resp.status_code == 200 and meme_resp.content:
                return meme_resp.content

            logger.warning(f'{LOG_PREFIX} 表情包生成接口响应异常 HTTP {meme_resp.status_code}: {meme_resp.text[:200]}')
            return None
    except Exception as exc:
        logger.error(f'{LOG_PREFIX} 请求表情包服务出错: {exc}')
        return None
