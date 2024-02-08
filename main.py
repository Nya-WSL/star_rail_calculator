'''
Author: Nya-WSL
Copyright © 2024 by Nya-WSL All Rights Reserved. 
Date: 2024-01-30 22:01:29
LastEditors: 狐日泽
LastEditTime: 2024-02-08 15:38:20
'''

import json
from nicegui import ui

### 读取数据库 ###

### 角色数据 ###
with open("data/l2d.json", "r", encoding="utf-8") as f:
    l2d_data = json.load(f)

### 武器数据 ###
with open("data/weapon.json", "r", encoding="utf-8") as f:
    weapon_data = json.load(f)

l2d_key = []
weapon_key = []

for key,value in l2d_data.items():
    l2d_key.append(key)
for key,value in weapon_data.items():
    weapon_key.append(key)

def update_value():
    base_l2d_atk_input.set_value(l2d_data[l2d_select.value]["base_l2d_atk"])
    harmony_atk_input.set_value(l2d_data[l2d_select.value]["harmony_atk"])
    base_weapon_atk_input.set_value(weapon_data[weapon_select.value]["base_weapon_atk"])

def start():
    base_l2d_atk = base_l2d_atk_input.value # 角色基础攻击
    base_weapon_atk = base_weapon_atk_input.value # 武器基础攻击
    base_atk = int(base_l2d_atk + base_weapon_atk) # 基础攻击总和

    ### 攻击加成 ###
    relics_atk = relics_atk_input.value # 遗器 固定
    relics_atk_percent = relics_atk_percent_input.value # 遗器 百分比
    harmony_atk = harmony_atk_input.value # 行迹
    l2d_atk = l2d_atk_input.value # 角色加成 固定
    l2d_atk_percent = l2d_atk_percent_input.value # 角色加成 百分比
    add_atk = base_atk * (relics_atk_percent + harmony_atk + l2d_atk_percent) + relics_atk + l2d_atk

    ### 倍率 ###
    l2d_percent = l2d_percent_input.value

    ### 暴击 ###
    crit_dmg = crit_dmg_input.value
    crit_percent = crit_percent_input.value
    if crit_percent >= 100.00:
        crit_percent == 100.00

    ### 增伤 ###
    dmg_boost = dmg_boost_input.value

    ### 易伤 ###
    increased_dmg = increased_dmg_input.value

    ### 防御 ###
    reduse_def = reduse_def_input.value # 角色对怪物减防
    l2d_level = l2d_level_input.value
    enemy_level = enemy_level_input.value # 怪物等级

    enemy_defense = (enemy_level * 10 + 200) * (1.00 - reduse_def) # 怪物防御
    defense = (l2d_level * 10 + 200) / (l2d_level * 10 + 200 + enemy_defense)

    ### 抗性 ###
    weakness = weakness_check.value # 弱点
    attribute_res = attribute_res_check.value # 属性抗性
    res_value = 0.00 # 抗性
    res_pen = res_pen_input.value # 抗性穿透

    if attribute_res == True:
        res_value = 0.40
    else:
        if weakness == True:
            res_value = 0.20

    res = res_value - res_pen

    ### 弱点击破 ###
    toughness = toughness_check.value
    toughness_dmg = 1.00
    if toughness == True:
        toughness_dmg = 0.90

    ### 伤害 ###
    damage = (base_atk + add_atk) * l2d_percent * (1 + dmg_boost) * (1 + increased_dmg) * defense * (1.00 - res) * toughness_dmg
    crit_damage = (base_atk + add_atk) * l2d_percent * (1 + dmg_boost) * (1 + increased_dmg) * defense * (1.00 - res) * toughness_dmg * (1.00 + crit_dmg)
    wish_damage = damage * (1.00 - crit_percent)

    ### 更新UI ###
    damage_badge.set_visibility(True)
    crit_damage_badge.set_visibility(True)
    wish_damage_badge.set_visibility(True)
    res_badge.set_text(res)
    toughness_dmg_badge.set_text(toughness_dmg)
    damage_badge.set_text(damage)
    crit_damage_badge.set_text(crit_damage)
    wish_damage_badge.set_text(wish_damage)

    ### debug ###
    # print(base_atk)
    # print(add_atk)
    # print(l2d_percent)
    # print(dmg_boost)
    # print(increased_dmg)
    # print(enemy_defense)
    # print(defense)
    # print(res)
    # print(toughness_dmg)
    # print(crit_dmg)
    # print(crit_percent)
    # print(wish_damage)
    # print(relics_atk_percent)
    # print(harmony_atk)
    # print(l2d_atk_percent)
    # print(relics_atk_percent + harmony_atk + l2d_atk_percent)

### 窗体UI ###
with ui.header().classes(replace='row items-center') as header:
    with ui.tabs() as tabs:
        ui.tab('计算器')
        ui.tab('角色')
        ui.tab('光锥')

with ui.tab_panels(tabs, value='计算器').classes('w-full'):
    with ui.tab_panel('计算器'):
        with ui.row():
            l2d_select = ui.select(label="角色", options=l2d_key, value=l2d_key[0], on_change=lambda: update_value())
            weapon_select = ui.select(label="武器", options=weapon_key, value=weapon_key[0], on_change=lambda: update_value())
        with ui.row():
            ui.badge("攻击")
            with ui.column():
                base_l2d_atk_input = ui.number(label="角色基础攻击", value=l2d_data[l2d_select.value]["base_l2d_atk"])
                base_weapon_atk_input = ui.number(label="武器基础攻击", value=weapon_data[weapon_select.value]["base_weapon_atk"])
                relics_atk_input = ui.number(label="遗器固定加成", value=0)
                relics_atk_percent_input = ui.number(label="遗器百分比加成", value=0.00)
                harmony_atk_input = ui.number(label="行迹加成", value=l2d_data[l2d_select.value]["harmony_atk"])
                l2d_atk_input = ui.number(label="角色固定加成", value=0)
                l2d_atk_percent_input = ui.number(label="角色百分比加成", value=0.00)

            ui.badge("倍率")
            with ui.column():
                l2d_percent_input = ui.number(label="角色攻击倍率", value=0.00)

            ui.badge("暴击")
            with ui.column():
                crit_dmg_input = ui.number(label="暴击伤害", value=0)
                crit_percent_input = ui.number(label="暴击率", value=0.00)

            ui.badge("增伤&易伤")
            with ui.column():
                dmg_boost_input = ui.number(label="增伤", value=0.00)
                increased_dmg_input = ui.number(label="易伤", value=0.00)

            ui.badge("防御")
            with ui.column():
                reduse_def_input = ui.number(label="角色减防", value=0.00)
                l2d_level_input = ui.number(label="角色等级", value=0)
                enemy_level_input = ui.number(label="怪物等级", value=0)

            ui.badge("抗性&击破")
            with ui.column():
                weakness_check = ui.checkbox("无弱点")
                attribute_res_check = ui.checkbox("属性抗性")
                toughness_check = ui.checkbox("未击破")
                res_pen_input = ui.number("抗性穿透", value=0.00)
                with ui.row():
                    ui.label("抗性")
                    res_badge = ui.badge(0, outline=True)
                    ui.label("击破")
                    toughness_dmg_badge = ui.badge(0, outline=True)

        with ui.card():
            with ui.row():
                ui.button("计算", on_click=lambda: start())
                ui.label("基础伤害")
                damage_badge = ui.badge(0, outline=True)
                damage_badge.set_visibility(False)

                ui.label("暴击伤害")
                crit_damage_badge = ui.badge(0, outline=True)
                crit_damage_badge.set_visibility(False)

                ui.label("期望伤害")
                wish_damage_badge = ui.badge(0, outline=True)
                wish_damage_badge.set_visibility(False)

port = 3334
verison = "1.0.0"
ui.run(port=port, title=f"崩坏：星穹铁道伤害计算器v{verison}", window_size=[1600, 900], native=True, show=False, reload=True, language="zh-CN")