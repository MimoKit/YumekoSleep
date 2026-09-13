from __future__ import annotations

from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.segment import MessageSegment

from .gn_config import GoodNightConfig

LOG_PREFIX = '[梦境沉沦]'


async def send_waves_stamina_if_available(bot: Bot, ev: Event) -> bool:
    """若存在 XutheringWavesUID 插件且当前打卡用户已绑定账号，则额外发送鸣潮体力图。

    此功能完全解耦，未安装插件、未绑定账号、或获取失败时均静默跳过，绝不影响主打卡流程。
    """
    try:
        # 1. 检查配置项开关
        enable_waves = GoodNightConfig.get_config('EnableWavesStamina').data
        if not enable_waves:
            return False

        # 2. 动态安全导入 XutheringWavesUID 模块
        try:
            from gsuid_core.plugins.XutheringWavesUID.XutheringWavesUID.utils.database.models import (
                WavesBind,
            )
            from gsuid_core.plugins.XutheringWavesUID.XutheringWavesUID.wutheringwaves_stamina.draw_waves_stamina import (
                draw_stamina_img,
            )
        except (ImportError, ModuleNotFoundError):
            logger.debug(f'{LOG_PREFIX} 未检测到 XutheringWavesUID 插件，跳过鸣潮体力推送')
            return False
        except Exception as e:
            logger.warning(f'{LOG_PREFIX} 导入 XutheringWavesUID 异常: {e}')
            return False

        # 3. 获取用户标识并检查是否存在绑定
        try:
            from gsuid_core.plugins.XutheringWavesUID.XutheringWavesUID.utils.at_help import (
                ruser_id,
            )

            target_user = ruser_id(ev)
        except Exception:
            target_user = str(ev.user_id).strip()

        bot_id = str(ev.bot_id).strip()

        uid = await WavesBind.get_uid_by_game(target_user, bot_id)
        if not uid:
            logger.debug(
                f'{LOG_PREFIX} 用户 {target_user} 未在 XutheringWavesUID 绑定鸣潮UID，跳过体力图'
            )
            return False

        # 4. 用户已绑定，生成并发送体力图
        logger.info(
            f'{LOG_PREFIX} 检测到用户 {target_user} 绑定了鸣潮UID({uid})，开始生成体力图...'
        )
        img_res = await draw_stamina_img(bot, ev)

        if isinstance(img_res, (bytes, bytearray)):
            await bot.send(MessageSegment.image(img_res))
            logger.info(f'{LOG_PREFIX} 成功向用户 {target_user} 发送鸣潮体力图')
            return True
        elif isinstance(img_res, str):
            logger.warning(
                f'{LOG_PREFIX} 用户 {target_user} 鸣潮体力图生成未成功 (返回: {img_res})，静默跳过'
            )
            return False
        else:
            logger.warning(
                f'{LOG_PREFIX} 用户 {target_user} 鸣潮体力图返回未知类型: {type(img_res)}'
            )
            return False

    except Exception as e:
        logger.exception(f'{LOG_PREFIX} 发送鸣潮体力图过程发生异常: {e}')
        return False
