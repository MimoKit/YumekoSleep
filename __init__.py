from __future__ import annotations

import datetime
import random
from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.segment import MessageSegment
from gsuid_core.sv import Plugins, SV

from .gn_config import GoodNightConfig
from .meme import get_good_night_meme, get_user_avatar_url
from .models import GoodNightRecord
from .utils import (
    format_chinese_datetime,
    format_duration,
    get_current_utc_and_local,
    is_same_local_day,
)

LOG_PREFIX = '[梦境沉沦]'

Plugins(name='YumekoSleep', force_prefix=[''], allow_empty_prefix=True)
sv = SV('梦境沉沦/早晚安记录')

# 鸣潮日系唯美风格的晚安寄语池
NIGHT_WISHES = [
    '今天在索拉里斯的冒险辛苦啦，今晚请安心歇息吧～',
    '今夜声骸平息，愿你的梦境如今汐大人的流云般宁静。',
    '风歇月明，让疲惫随潮水褪去，漂泊者，晚安～',
    '星月低垂，万物安眠。把今日的回响收好，好好睡一觉吧！',
    '黑石平原的夜风吹不散好梦，今晚就好好卸下防备休息吧～',
    '晚安，愿明日初阳升起时，索拉里斯大地再次为你共鸣。',
]

# 鸣潮日系唯美风格的早安寄语池
MORNING_WISHES_NORMAL = [
    '索拉里斯的朝阳已经升起，新的一天继续并肩前行吧！',
    '清晨的潮汐带来全新的回响，今天的冒险也要全力以赴哦～',
    '醒来啦？深呼吸，伸个懒腰，今天也是充满共鸣的一天！',
    '晨光洒在黑石平原上，漂泊者，整装待发迎接今日的委托吧！',
    '早安！休息得不错呢，愿今天的探索好运连连～',
]

# 睡太久（超过11小时）的趣味寄语
MORNING_WISHES_LONG = [
    '哇，睡了这么久，是陷入了时间的声骸回溯里了吗～',
    '沉睡的漂泊者终于苏醒啦，精力条已经完全回满！',
    '看来昨晚的冒险真的很累呢，能补足精神真是太好啦～',
]

# 睡太短（少于4小时）的关切寄语
MORNING_WISHES_SHORT = [
    '才睡了这么一会儿呀，漂泊者要注意休息，别太勉强自己哦！',
    '怎么这么快就醒啦？索拉里斯的冒险很长，可千万别累坏了～',
    '这么早就开始行动了吗？今天记得找机会小憩一下哦！',
]

# 关闭鸣潮风格时使用的朴素固定文案
FIXED_NIGHT_WISH = '晚安，祝你好梦～'
FIXED_MORNING_WISH = '早安！新的一天开始了，祝你今天一切顺利。'


def _theme_enabled() -> bool:
    return bool(GoodNightConfig.get_config('EnableThemeWishes').data)


@sv.on_fullmatch(('晚安', '睡觉啦', '睡觉了', '睡了', '去睡了', '安安', 'gn'), block=True)
async def handle_good_night(bot: Bot, ev: Event):
    user_id = str(ev.user_id).strip()
    group_id = str(ev.group_id or 'direct').strip()
    bot_id = str(ev.bot_id).strip()

    ts, now_utc, now_local = get_current_utc_and_local()
    local_str = format_chinese_datetime(now_local)

    # 检查用户今天是否已经打卡过晚安且尚未醒来（醒来后允许当晚重新入睡）
    record = await GoodNightRecord.get_record(bot_id, user_id)
    if (
        record
        and record.sleep_timestamp > 0
        and record.is_sleeping
        and is_same_local_day(record.sleep_timestamp, ts)
    ):
        last_sleep_dt = format_chinese_datetime(
            datetime.datetime.fromtimestamp(record.sleep_timestamp).astimezone()
        )
        logger.info(f'{LOG_PREFIX} 用户 {user_id} 今日已打卡入梦 ({last_sleep_dt})，拦截重复打卡')
        if _theme_enabled():
            reply_text = (
                f'漂泊者，你今天已经打卡过入梦啦～\n'
                f'上次打卡时间：{last_sleep_dt}\n'
                f'不能贪睡重打哦，先好好休息或等起床吧！'
            )
        else:
            reply_text = (
                f'你今天已经打过晚安卡啦～\n'
                f'上次打卡时间：{last_sleep_dt}\n'
                f'明天起床后再打早安卡哦！'
            )
        await bot.send(reply_text)
        return

    logger.info(f'{LOG_PREFIX} 用户 {user_id} (群: {group_id}, Bot: {bot_id}) 打卡入梦, 时间: {local_str}')

    await GoodNightRecord.set_sleep(bot_id, user_id, group_id, ts)

    other_sleeping_count = await GoodNightRecord.count_other_sleeping(bot_id, user_id)

    if _theme_enabled():
        if other_sleeping_count > 0:
            companion_text = f'此刻还有 {other_sleeping_count} 位漂泊者与你一同入梦。'
        else:
            companion_text = '今夜你是第一位踏入梦乡的漂泊者。'
        wish = random.choice(NIGHT_WISHES)
        reply_text = (
            f'晚安，漂泊者～\n'
            f'{wish}\n'
            f'{companion_text}\n'
            f'入睡时间：{local_str}'
        )
    else:
        if other_sleeping_count > 0:
            companion_text = f'当前还有 {other_sleeping_count} 人尚未起床。'
        else:
            companion_text = '今晚还没有人打卡晚安。'
        reply_text = (
            f'晚安～\n'
            f'{FIXED_NIGHT_WISH}\n'
            f'{companion_text}\n'
            f'入睡时间：{local_str}'
        )

    # 1. 先发送文本回复
    await bot.send(reply_text)

    # 2. 如果开启了表情包，单独发送表情包图片消息
    enable_meme = GoodNightConfig.get_config('EnableMeme').data
    meme_url = GoodNightConfig.get_config('MemeApiUrl').data

    if enable_meme and meme_url:
        logger.info(f'{LOG_PREFIX} 为用户 {user_id} 请求生成晚安表情包...')
        avatar = get_user_avatar_url(ev)
        meme_bytes = await get_good_night_meme(bot_id, user_id, avatar, meme_url)
        if meme_bytes:
            logger.info(f'{LOG_PREFIX} 用户 {user_id} 晚安表情包生成成功，独立发出')
            await bot.send(MessageSegment.image(meme_bytes))
        else:
            logger.warning(f'{LOG_PREFIX} 用户 {user_id} 晚安表情包生成失败或为空')


@sv.on_fullmatch(('早安', '起床啦', '起床了', '醒了', '早呀', '早上好', 'gm'), block=True)
async def handle_good_morning(bot: Bot, ev: Event):
    user_id = str(ev.user_id).strip()
    group_id = str(ev.group_id or 'direct').strip()
    bot_id = str(ev.bot_id).strip()

    ts, now_utc, now_local = get_current_utc_and_local()
    local_str = format_chinese_datetime(now_local)

    logger.info(f'{LOG_PREFIX} 用户 {user_id} (群: {group_id}, Bot: {bot_id}) 打卡苏醒')

    record = await GoodNightRecord.get_record(bot_id, user_id)

    # 今天已经打卡过早安，拦截重复打卡
    if (
        record
        and record.last_wake_timestamp > 0
        and is_same_local_day(record.last_wake_timestamp, ts)
    ):
        last_wake_dt = format_chinese_datetime(
            datetime.datetime.fromtimestamp(record.last_wake_timestamp).astimezone()
        )
        logger.info(f'{LOG_PREFIX} 用户 {user_id} 今日已打卡苏醒 ({last_wake_dt})，拦截重复打卡')
        if _theme_enabled():
            reply_text = (
                f'漂泊者，你今天已经打卡过苏醒啦～\n'
                f'上次打卡时间：{last_wake_dt}\n'
                f'新的一天已经开始，今晚也要好好休息哦！'
            )
        else:
            reply_text = (
                f'你今天已经打过早安卡啦～\n'
                f'上次打卡时间：{last_wake_dt}\n'
                f'晚上记得再来打晚安卡哦！'
            )
        await bot.send(reply_text)
        return

    # 情况 2：昨晚没有晚安记录，不带任何时间信息
    if not record or record.sleep_timestamp <= 0:
        logger.info(f'{LOG_PREFIX} 用户 {user_id} 未找到昨晚入梦记录，回复默认问候')
        if _theme_enabled():
            reply_text = '早上好，漂泊者！新的一天也要元气满满哦～昨晚没有找到你的入睡打卡记录呢。'
        else:
            reply_text = '早上好！昨晚没有找到你的晚安打卡记录。'
        await bot.send(reply_text)
        return

    # 情况 1：正常记录睡眠时间，早安不带表情包
    sleep_seconds = ts - record.sleep_timestamp
    if sleep_seconds < 0:
        sleep_seconds = 0

    duration_str = format_duration(sleep_seconds)

    await GoodNightRecord.set_wake(bot_id, user_id, group_id, ts)
    logger.info(f'{LOG_PREFIX} 用户 {user_id} 睡眠结束，共计睡眠: {duration_str}')

    # 根据开关选择鸣潮风格寄语或固定文案
    if _theme_enabled():
        # 根据睡眠时长动态匹配鸣潮风格早安寄语
        if sleep_seconds >= 11 * 3600:
            wish = random.choice(MORNING_WISHES_LONG)
        elif sleep_seconds < 4 * 3600:
            wish = random.choice(MORNING_WISHES_SHORT)
        else:
            wish = random.choice(MORNING_WISHES_NORMAL)
        reply_text = (
            f'早安，漂泊者！\n'
            f'你一共睡了 {duration_str}。\n'
            f'{wish}\n'
            f'起床时间：{local_str}'
        )
    else:
        reply_text = (
            f'早安！\n'
            f'你一共睡了 {duration_str}。\n'
            f'{FIXED_MORNING_WISH}\n'
            f'起床时间：{local_str}'
        )

    await bot.send(reply_text)
