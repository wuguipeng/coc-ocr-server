from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import uuid

from entity.CocUserInfo import CocUserInfo
Base = declarative_base()

class CocUserDateLog(Base):
    __tablename__ = 'coc_user_date_log'

    id = Column(String(32), primary_key=True, nullable=False, comment='唯一ID')
    user_id = Column(String(32), nullable=False, comment='用户标签')
    user_grade = Column(Integer, comment='用户等级')
    clan_name = Column(String(32), comment='用户所在部落名称')
    clan_grade = Column(Integer, comment='部落等级')
    current_trophy = Column(Integer, comment='当前奖杯')
    current_level = Column(String(32), comment='当前段位')
    all_time_best = Column(Integer, comment='历史最佳')
    war_stars_won = Column(Integer, comment='胜利之星')
    troops_donated = Column(Integer, comment='近期捐赠')
    troops_received = Column(Integer, comment='近期收到')
    attacks_won = Column(Integer, comment='进攻获胜')
    defenses_won = Column(Integer, comment='防御获胜')
    create_time = Column(DateTime, comment='创建时间')

    def __init__(self,user_info :CocUserInfo):
        self.id = str(uuid.uuid4()).replace("-", "")
        self.user_id = user_info.id
        self.user_grade = user_info.user_grade
        self.clan_name = user_info.clan_name
        self.clan_grade = user_info.clan_grade
        self.current_trophy = user_info.current_trophy
        self.current_level = user_info.current_level
        self.all_time_best = user_info.all_time_best
        self.war_stars_won = user_info.war_stars_won
        self.troops_donated = user_info.troops_donated
        self.troops_received = user_info.troops_received
        self.attacks_won = user_info.attacks_won
        self.defenses_won = user_info.defenses_won
        if user_info.create_time is None:
            self.create_time = user_info.update_time
        else:
            self.create_time = user_info.create_time