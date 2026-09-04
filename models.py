from __future__ import annotations

from typing import Optional
from sqlmodel import Field, select
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession

from gsuid_core.server import on_core_start_before
from gsuid_core.utils.database.base_models import (
    BaseModel,
    engine,
    with_read_session,
    with_session,
)
from gsuid_core.webconsole.mount_app import GsAdminModel, PageSchema, site


class GoodNightRecord(BaseModel, table=True):
    """用户早晚安睡眠记录表"""

    __table_args__ = (
        UniqueConstraint('bot_id', 'user_id'),
        {'extend_existing': True},
    )

    group_id: str = Field(default='direct', title='群号')
    sleep_timestamp: float = Field(default=0.0, title='晚安UTC时间戳')
    is_sleeping: bool = Field(default=False, title='是否处于睡眠状态')
    last_wake_timestamp: float = Field(default=0.0, title='上次早安UTC时间戳')

    @classmethod
    @with_read_session
    async def get_record(
        cls, session: AsyncSession, bot_id: str, user_id: str
    ) -> Optional['GoodNightRecord']:
        """根据 bot_id 和 user_id 获取记录"""
        stmt = (
            select(cls)
            .where(cls.bot_id == bot_id)
            .where(cls.user_id == user_id)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    @with_session
    async def set_sleep(
        cls, session: AsyncSession, bot_id: str, user_id: str, group_id: str, timestamp: float
    ) -> 'GoodNightRecord':
        """记录晚安时间"""
        record = await cls.get_record(bot_id, user_id)
        if record:
            record.group_id = group_id
            record.sleep_timestamp = timestamp
            record.is_sleeping = True
            session.add(record)
            return record

        record = cls(
            bot_id=bot_id,
            user_id=user_id,
            group_id=group_id,
            sleep_timestamp=timestamp,
            is_sleeping=True,
            last_wake_timestamp=0.0,
        )
        session.add(record)
        return record

    @classmethod
    @with_session
    async def set_wake(
        cls, session: AsyncSession, bot_id: str, user_id: str, group_id: str, timestamp: float
    ) -> Optional['GoodNightRecord']:
        """唤醒（早安）并更新状态"""
        record = await cls.get_record(bot_id, user_id)
        if not record:
            return None
        record.group_id = group_id
        record.is_sleeping = False
        record.last_wake_timestamp = timestamp
        session.add(record)
        return record


@on_core_start_before(priority=-70)
async def _ensure_good_night_table() -> None:
    """初始化建表"""
    async with engine.begin() as conn:
        await conn.run_sync(
            GoodNightRecord.metadata.create_all,
            tables=[GoodNightRecord.metadata.tables['goodnightrecord']],
            checkfirst=True,
        )


@site.register_admin
class GoodNightRecordAdmin(GsAdminModel):
    pk_name = 'id'
    page_schema = PageSchema(
        label='早晚安打卡记录',
        icon='fa fa-moon-o',
    )  # type: ignore

    model = GoodNightRecord
