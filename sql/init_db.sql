create table coc_user_info(
    id varchar(32) not null comment '用户标签',
    user_name varchar(32) not null comment '用户名',
    user_grade int(11) comment '用户等级',
    clan_name varchar(32) comment '用户所在部落名称',
    clan_grade int(11) comment '部落等级',
    current_trophy int(11) comment '当前奖杯',
    current_level varchar(32) comment '当前段位',
    all_time_best int(11) comment '历史最佳',
    war_stars_won int(11) comment '胜利之星',
    troods_donated int(11) comment '近期捐赠',
    troops_received int(11) comment '近期收到',
    attacks_won int(11) comment '进攻获胜',
    defenses_won int(11) comment '防御获胜',
    create_time datetime comment '创建时间',
    update_time datetime comment '更新时间',
)


create table coc_user_date_log(
    id varchar(32) not null comment '唯一ID',
    user_id varchar(32) not null comment '用户标签',
    user_grade int(11) comment '用户等级',
    clan_name varchar(32) comment '用户所在部落名称',
    clan_grade int(11) comment '部落等级',
    current_trophy int(11) comment '当前奖杯',
    current_level varchar(32) comment '当前段位',
    all_time_best int(11) comment '历史最佳',
    war_stars_won int(11) comment '胜利之星',
    troods_donated int(11) comment '近期捐赠',
    troops_received int(11) comment '近期收到',
    attacks_won int(11) comment '进攻获胜',
    defenses_won int(11) comment '防御获胜',
    create_time datetime comment '创建时间',
    update_time datetime comment '更新时间',
)


