from __future__ import annotations

import hashlib
import re
import time
from pathlib import Path
from typing import Optional
import httpx

from gsuid_core.logger import logger
from gsuid_core.models import Event

LOG_PREFIX = '[晚安插件]'
MEME_KEY = 'kurogames_good_night'

# 表情包本地缓存：按「用户 + 头像内容哈希」缓存，3 天内不重新生成，超期自动清理
# QQ 头像 URL 固定不变（换头像后 URL 相同），因此必须按图片内容而非 URL 区分
CACHE_DIR = Path(__file__).parent / 'meme_cache'
CACHE_TTL_SECONDS = 3 * 24 * 3600


def _content_hash(content: bytes) -> str:
    return hashlib.sha1(content).hexdigest()[:16]


def _cache_path(bot_id: str, user_id: str, avatar_bytes: bytes) -> Path:
    safe_bot = re.sub(r'[^A-Za-z0-9_-]', '_', bot_id)
    safe_user = re.sub(r'[^A-Za-z0-9_-]', '_', user_id)
    return CACHE_DIR / f'{safe_bot}_{safe_user}_{_content_hash(avatar_bytes)}.png'


def get_cached_meme(bot_id: str, user_id: str, avatar_bytes: bytes) -> Optional[bytes]:
    """读取未过期的用户缓存表情（按头像内容区分），过期或不存在返回 None"""
    path = _cache_path(bot_id, user_id, avatar_bytes)
    if not path.is_file():
        return None
    age = time.time() - path.stat().st_mtime
    if age > CACHE_TTL_SECONDS:
        return None
    return path.read_bytes()


def save_cached_meme(bot_id: str, user_id: str, avatar_bytes: bytes, content: bytes) -> None:
    """把生成的表情写入本地缓存"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _cache_path(bot_id, user_id, avatar_bytes).write_bytes(content)


def cleanup_expired_cache() -> None:
    """清理超过缓存期限的表情文件"""
    if not CACHE_DIR.is_dir():
        return
    now = time.time()
    for path in CACHE_DIR.glob('*.png'):
        try:
            if now - path.stat().st_mtime > CACHE_TTL_SECONDS:
                path.unlink()
        except OSError as exc:
            logger.warning(f'{LOG_PREFIX} 清理缓存文件失败 {path}: {exc}')


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


async def get_good_night_meme(
    bot_id: str, user_id: str, avatar_url: str, base_url: str
) -> Optional[bytes]:
    """下载头像后按内容哈希查缓存：命中则不请求生成服务，未命中才生成并写缓存"""
    if not base_url:
        return None

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # 1. 下载用户头像二进制数据（QQ 头像 URL 固定，必须下载后按内容区分）
            avatar_resp = await client.get(
                avatar_url, headers={'User-Agent': 'Mozilla/5.0'}
            )
            if avatar_resp.status_code != 200 or not avatar_resp.content:
                logger.warning(
                    f'{LOG_PREFIX} 下载用户头像失败, HTTP {avatar_resp.status_code}: {avatar_url}'
                )
                return None
            avatar_bytes = avatar_resp.content

            # 2. 按头像内容哈希查 3 天内缓存，命中则直接返回（不调用生成服务）
            cached = get_cached_meme(bot_id, user_id, avatar_bytes)
            if cached is not None:
                logger.info(f'{LOG_PREFIX} 用户 {user_id} 命中晚安表情包本地缓存')
                return cached

            # 3. 缓存未命中，调用 meme_generator 生成表情包
            clean_base = base_url.rstrip('/')
            endpoint = f'{clean_base}/memes/{MEME_KEY}/'
            files = {'images': ('avatar.jpg', avatar_bytes, 'image/jpeg')}
            data = {'texts': []}
            meme_resp = await client.post(endpoint, files=files, data=data)

            if meme_resp.status_code != 200 or not meme_resp.content:
                logger.warning(
                    f'{LOG_PREFIX} 表情包生成接口响应异常 HTTP {meme_resp.status_code}: '
                    f'{meme_resp.text[:200]}'
                )
                return None

            save_cached_meme(bot_id, user_id, avatar_bytes, meme_resp.content)
            cleanup_expired_cache()
            return meme_resp.content
    except Exception as exc:
        logger.error(f'{LOG_PREFIX} 请求表情包服务出错: {exc}')
        return None
