from __future__ import annotations

import datetime
from typing import Tuple


def get_current_utc_and_local() -> Tuple[float, datetime.datetime, datetime.datetime]:
    """
    获取当前时间：
    返回 (utc_timestamp, utc_datetime, local_datetime)
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_local = datetime.datetime.now().astimezone()
    return now_utc.timestamp(), now_utc, now_local


def is_same_local_day(timestamp1: float, timestamp2: float) -> bool:
    """判断两个时间戳在本地时区是否是同一自然日"""
    if timestamp1 <= 0 or timestamp2 <= 0:
        return False
    dt1 = datetime.datetime.fromtimestamp(timestamp1).astimezone()
    dt2 = datetime.datetime.fromtimestamp(timestamp2).astimezone()
    return dt1.date() == dt2.date()


def format_duration(seconds: float) -> str:
    """把秒数格式化为友好的中文时间时长"""
    if seconds <= 0:
        return '0分钟'

    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    parts = []
    if hours > 0:
        parts.append(f'{hours}小时')
    if minutes > 0:
        parts.append(f'{minutes}分钟')
    if secs > 0 and hours == 0:
        parts.append(f'{secs}秒')

    return ''.join(parts) if parts else '不到1分钟'


def format_chinese_datetime(dt: datetime.datetime) -> str:
    """格式化具体中文时间：YYYY年MM月DD日 HH:MM:SS"""
    return dt.strftime('%Y年%m月%d日 %H:%M:%S')


def format_utc_display(dt: datetime.datetime) -> str:
    """格式化标准 UTC 时间：YYYY-MM-DD HH:MM:SS"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')
