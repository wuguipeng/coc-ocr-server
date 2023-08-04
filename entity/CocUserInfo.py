from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
Base = declarative_base()

class CocUserInfo(Base):
    __tablename__ = 'coc_user_info'

    id = Column(String(32), primary_key=True, nullable=False, comment='用户标签')
    user_name = Column(String(32), nullable=False, comment='用户名')
    user_grade = Column(Integer, comment='用户等级')
    user_position = Column(String(32), comment='职位')
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
    update_time = Column(DateTime, comment='更新时间')
    
    def __str__(self):
        return f"CocUserInfo(id={self.id}, user_name={self.user_name}, user_grade={self.user_grade}, " + \
        f"user_position={self.user_position}, clan_name={self.clan_name}, clan_grade={self.clan_grade}, " + \
        f"current_trophy={self.current_trophy}, current_level={self.current_level}, all_time_best={self.all_time_best}, " + \
        f"war_stars_won={self.war_stars_won}, troops_donated={self.troops_donated}, troops_received={self.troops_received}, " + \
        f"attacks_won={self.attacks_won}, defenses_won={self.defenses_won}, create_time={self.create_time}, " + \
        f"update_time={self.update_time})"