import os
import django
import json
# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jtw_info_management.settings')
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
# Setup Django
django.setup()

from create.models import *

def reinitialize_continent():
    Continent.objects.all().delete()

    continent_list = ["东胜神洲", "西牛贺洲", "南赡部洲", "北俱芦洲", "无"]
    description_list = [
        "灵秀之区，多产异宝奇珍，然无大智若愚之士。",
        "不贪不杀，养气潜灵，佛国多妖，取经终点灵山所在。",
        "善人所居，多有布施斋僧，然无大勇大猛之夫。",
        "仙人所宅，多有修真之客，然无大福大贵之神。",
        ""
    ]
    id = 1
    for continent, description in zip(continent_list, description_list):
        obj = Continent.objects.create(
            id = id ,
            name=continent,
            description=description,
        )
        id = id + 1

def reinitialize_relation_types():
    Relationship_Type.objects.all().delete()
    # 初始数据列表
    initial_realations = [
        {'type': '师徒', 'description': '师傅与徒弟之间的导师关系，强调传承与指导。'},
        {'type': '师兄弟', 'description': '同辈之间的从师关系，象征团结与互助。'},
        {'type': '夫妻', 'description': '婚姻关系，伴侣之间互相扶持、共同生活。'},
        {'type': '父子', 'description': '父亲与儿子之间的亲子关系，体现血脉传承与教育。'},
        {'type': '朋友', 'description': '非血缘的亲密友人关系，基于信任与共同兴趣。'},
        {'type': '主仆', 'description': '主人与坐骑（宠物或交通工具）之间的主仆关系，常用于游戏或幻想设定中。'},
        {'type': '君臣', 'description': '组织或团队中的层级关系，上级指导下级，下级服从上级。'},
        {'type': '拜把子', 'description': '通过结拜仪式结成的义兄弟关系，强调忠诚与生死相依。'},
        {'type': '敌对' , 'description': '反目成仇'}
        # 原“拜把子兄弟”改名为“结拜兄弟”，更简洁通用
    ]
    for realation in initial_realations:
        obj = Relationship_Type.objects.create(
            type=realation['type'],
            description=realation['description'],
        )

def reinitialize_calamity():
    Calamity.objects.all().delete()
    current_id = 1
    with open(r'C:\Users\32939\Desktop\github_repo\journey_to_the_west_info_sys\jtw_info_management\initial_data\calamity.json', 'r', encoding='utf-8') as file:
        data_dict = json.load(file)
        for data in data_dict:
            obj = Calamity.objects.create(
            id = current_id,
            title = data['title'],
            summary = data['summary'],
            )
            current_id  = current_id + 1

@transaction.atomic
def location_exists(location_name: str):
    """
    插入地点：先查询是否已存在同名Location，如果不存在则创建。
    返回:
    - 查询到的或新创建的Location实例。
    """
    # 先检查Location是否已存在
    try:
        existing_location = Location.objects.get(name=location_name)
        return True  # 已存在，直接返回
    except ObjectDoesNotExist:
        return False

@transaction.atomic
def initialize_single_location(location_name: str, continent_name: str, introduction: str) -> Location:
    """
    初始化地点：根据大陆名称查询ID，然后创建Location实例。
    异常:
    - 无（如果大陆名称不存在，将使用默认大陆“无”）。
    """
    try:
        # 先查询大陆名称对应的ID
        continent_obj = Continent.objects.get(name=continent_name)
        continent_id = continent_obj.id
    except ObjectDoesNotExist:
        # 如果大陆名称不存在，统一使用默认大陆“无”
        try:
            default_continent_obj = Continent.objects.get(name="无")
            continent_id = default_continent_obj.id
        except ObjectDoesNotExist:
            # 如果“无”大陆也不存在，创建它
            default_continent_obj = Continent.objects.create(name="无")
            continent_id = default_continent_obj.id

    # 创建Location实例，使用查询到的continent_id
    location = Location.objects.create(
        name=location_name,
        description=introduction,
        continent_id=continent_id  # 直接使用ID赋值外键
    )

    return location

def initialize_location():
    with open(r"C:\Users\32939\Desktop\github_repo\journey_to_the_west_info_sys\jtw_info_management\initial_data\place.json", 'r', encoding='utf-8') as file:
        data_dict = json.load(file)
        for data in data_dict:
            print(data["地名"])
            initial_location = initialize_single_location(data["地名"], data['所属大洲'] , data['介绍'])



def initialize_location_withoutrepeat():
    with open(r"C:\Users\32939\Desktop\github_repo\journey_to_the_west_info_sys\jtw_info_management\initial_data\place.json", 'r', encoding='utf-8') as file:
        data_dict = json.load(file)
        for data in data_dict:
            if not (location_exists(data['地名'])):
                print(data["地名"])
                initial_location = initialize_single_location(data["地名"], data['所属大洲'] , data['介绍'])

def initialize_chapter():
    with open(r"C:\Users\32939\Desktop\github_repo\journey_to_the_west_info_sys\jtw_info_management\initial_data\chapter.json", 'r', encoding='utf-8') as file:
        data_dict = json.load(file)
        for data in data_dict:
                chapter = Chapter.objects.create(
                    chapter_number = data['chapter'],
                    title = data['title'],
                    summary = data['summary'],
                )
    return True


@transaction.atomic
def initial_single_chapter_location(chapter_title: str, location_list: list[str]):
    """
    为指定章节初始化地点关联：遍历地点列表，如果地点不存在则创建，建立章节-地点关联。

    参数:
    - chapter_title: 章节标题，用于查询对应的Chapter实例，必填。
    - location_list: 地点名称列表，必填。

    异常:
    - 如果章节标题不存在，将抛出ValueError。
    """
    try:
        # 获取对应章节的实例和ID
        chapter_obj = Chapter.objects.get(title=chapter_title)
        chapter_id = chapter_obj.chapter_number
    except ObjectDoesNotExist:
        raise ValueError(f"章节标题 '{chapter_title}' 不存在，请先创建对应章节。")

    # 遍历地点列表
    for loc_name in location_list:
        # 如果地点不存在则创建（description默认'暂无'，continent=None）
        location_obj, created = Location.objects.get_or_create(
            name=loc_name,
            defaults={'description': '暂无'}
        )
        location_id = location_obj.id

        # 建立章节-地点关联（使用get_or_create避免重复）
        Chapter_Location.objects.get_or_create(
            chapter=chapter_obj,
            location=location_obj
        )

def initialize_chapter_location():
    with open(r".\initial_data\chapter.json", 'r', encoding='utf-8') as file:
        data_dict = json.load(file)
        for data in data_dict:
            initial_single_chapter_location(data['title'], data['locations'])


def initialize_character():
    file_path = r".\initial_data\character.json"
    with open(file_path, 'r', encoding='utf-8') as file:
        data_dict = json.load(file)

        # 收集JSON中所有有效人物名称
        json_names = {data.get('name', '').strip() for data in data_dict if data.get('name', '').strip()}

        # 获取数据库中所有人物名称
        all_db_names = {char.name for char in Character.objects.all()}

        # 找出数据库中多余的名称（不在JSON中）
        to_delete = all_db_names - json_names

        # 先删除多余记录
        for name in to_delete:
            try:
                char = Character.objects.get(name=name)
                char.delete()
                print(f"删除不存在于JSON中的人物: {name}")
            except Exception as e:
                print(f"删除人物 {name} 时出错: {str(e)}")

        # 然后插入或跳过现有记录
        for data in data_dict:
            name = data.get('name', '').strip()
            if not name:  # 跳过空名称
                continue

            # 检查是否已存在（基于 name 字段，假设 name 是唯一标识）
            if Character.objects.filter(name=name).exists():
                print(f"跳过已存在人物: {name}")
                continue

            # 映射 JSON 字段到模型字段
            # 注意: type 假设对应 race，introduction 对应 intro
            # image 使用默认 None（JSON 中无此字段）
            # organization 默认 '无组织' 如果缺失
            race = data.get('type', '仙')  # 根据 RACE_CHOICES 选择合适默认值
            ability = data.get('ability', '')
            intro = data.get('introduction', '')  # 或 'intro'，根据 JSON 实际键调整
            organization = data.get('organization', '无组织')

            # 创建并保存新实例
            try:
                char = Character(
                    name=name,
                    race=race,
                    ability=ability,
                    intro=intro,
                    organization=organization
                    # image 默认 None，无需指定
                )
                char.save()
                print(f"成功插入新人物: {name}")
            except Exception as e:
                print(f"插入人物 {name} 时出错: {str(e)}")


def initialize_character_relationship():
    with open(r".\initial_data\character.json", 'r', encoding='utf-8') as file:
        data_dict = json.load(file)


def initialize_weapon():
    """
    从 weapon.json 文件初始化武器数据。
    假设 JSON 是列表格式，每个元素是一个字典，包含 'name', 'introduction', 'owner'。
    如果拥有者为空或不存在于 Character 中，或武器已存在（基于名称），则跳过插入并打印记录。
    """
    file_path = r".\initial_data\weapon.json"
    skipped_count = 0
    inserted_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data_list = json.load(file)

        # 假设 data_list 是列表形式
        if not isinstance(data_list, list):
            print("警告: JSON 数据不是列表格式，跳过处理。")
            return

        for data in data_list:
            try:
                owner_name = data.get("owner", "").strip()
                weapon_name = data.get("name")

                if not weapon_name:
                    print(f"跳过武器: 缺少武器名称 - {data}")
                    skipped_count += 1
                    continue

                # 检查拥有者是否为空
                if not owner_name:
                    print(f"跳过武器: 拥有者为空 - {data}")
                    skipped_count += 1
                    continue

                # 查询 Character 中是否存在该拥有者
                try:
                    owner_character = Character.objects.get(name=owner_name)
                except Character.DoesNotExist:
                    print(f"跳过武器{weapon_name}: 拥有者 '{owner_name}' 在 Character 中不存在 -")
                    skipped_count += 1
                    continue

                # 检查武器是否已存在（基于名称）
                if Weapon.objects.filter(name=weapon_name).exists():
                    print(f"跳过武器: 武器 '{weapon_name}' 已存在 ")
                    skipped_count += 1
                    continue

                # 创建 Weapon 实例
                weapon = Weapon(
                    name=weapon_name,
                    description=data["introduction"],
                    owner_character=owner_character,
                    # image: 初始化时不设置，默认为 None 或空文件
                    # created_at: 默认使用 timezone.now()
                )

                # 保存到数据库
                weapon.save()
                print(f"成功插入武器: {weapon_name}，拥有者: {owner_name}, 拥有者ID: {owner_character.id}")
                inserted_count += 1

            except KeyError as e:
                print(f"跳过武器: JSON 项缺少键 {e} - {data}")
                skipped_count += 1
            except Exception as e:
                print(f"跳过武器: 处理项时出错 {e} - {data}")
                skipped_count += 1

        print(f"处理完成: 成功插入 {inserted_count} 条武器，跳过 {skipped_count} 条。")

    except FileNotFoundError:
        print(f"错误: 文件未找到 - {file_path}")
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败 - {e}")
    except Exception as e:
        print(f"错误: 初始化武器时发生未知异常 - {e}")

def build_single_relationship(from_character, to_character, rel_type):
    """
    1.首先需要判断两角色是否存在,若不存在则不插入
    2.判断关系类型是否存在,不存在创建该关系类型后再插入
    3.若都存在则直接插入
    """
    try:
        # 1. 判断发起方角色是否存在
        from_char = Character.objects.get(name=from_character)
    except ObjectDoesNotExist:
        print(f"发起方角色 '{from_character}' 不存在，跳过插入关系。")
        return

    try:
        # 1. 判断接收方角色是否存在
        to_char = Character.objects.get(name=to_character)
    except ObjectDoesNotExist:
        print(f"接收方角色 '{to_character}' 不存在，跳过插入关系。")
        return

    try:
        # 2. 判断关系类型是否存在
        rel_type_obj = Relationship_Type.objects.get(type=rel_type)
    except ObjectDoesNotExist:
        # 创建关系类型
        rel_type_obj = Relationship_Type.objects.create(
            type=rel_type,
            description=''  # 默认空描述
        )
        print(f"创建新关系类型: {rel_type}")

    # 3. 插入关系
    relationship = Character_Relationship(
        from_character=from_char,
        to_character=to_char,
        relationship_type=rel_type_obj
    )
    relationship.save()
    print(f"成功插入关系: {from_character} → {to_character} ({rel_type})")


def build_single_relationship(from_character, to_character, rel_type):
    """
    1.首先需要判断两角色是否存在,若不存在则不插入
    2.判断关系类型是否存在,不存在创建该关系类型后再插入
    3.若都存在则直接插入
    """
    try:
        # 1. 判断发起方角色是否存在
        from_char = Character.objects.get(name=from_character)
    except ObjectDoesNotExist:
        print(f"发起方角色 '{from_character}' 不存在，跳过插入关系。")
        return

    try:
        # 1. 判断接收方角色是否存在
        to_char = Character.objects.get(name=to_character)
    except ObjectDoesNotExist:
        print(f"接收方角色 '{to_character}' 不存在，跳过插入关系。")
        return

    try:
        # 2. 判断关系类型是否存在
        rel_type_obj = Relationship_Type.objects.get(type=rel_type)
    except ObjectDoesNotExist:
        # 创建关系类型
        rel_type_obj = Relationship_Type.objects.create(
            type=rel_type,
            description=''  # 默认空描述
        )
        print(f"创建新关系类型: {rel_type}")

    # 检查关系是否已存在（基于发起方、接收方及关系类型）
    if Character_Relationship.objects.filter(
            from_character=from_char,
            to_character=to_char,
            relationship_type=rel_type_obj
    ).exists():
        print(f"跳过关系: 该关系已存在 - {from_character} → {to_character} ({rel_type})")
        return

    # 3. 插入关系
    relationship = Character_Relationship(
        from_character=from_char,
        to_character=to_char,
        relationship_type=rel_type_obj
    )
    relationship.save()
    print(f"成功插入关系: {from_character} → {to_character} ({rel_type})")


def build_relationship_from_characters():
    """
    从 character.json 文件构建人物关系。
    JSON 数据结构为列表，每个元素是一个字典，包含 'name', 'superiors' (dict: superior_name: rel_type), 'subordinates' (dict: subordinate_name: rel_type)。
    对于 superiors: 调用 build_single_relationship(superior_name, current_name, rel_type)。
    对于 subordinates: 调用 build_single_relationship(current_name, subordinate_name, rel_type)。
    """
    file_path = r".\initial_data\character.json"
    processed_count = 0
    skipped_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 假设 data 是列表形式
        if not isinstance(data, list):
            print("警告: JSON 数据不是列表格式，跳过处理。")
            return

        for char_data in data:
            try:
                char_name = char_data.get('name')
                if not char_name:
                    print(f"跳过人物: 缺少人物名称 - {char_data}")
                    skipped_count += 1
                    continue

                # 处理 superiors
                superiors = char_data.get('superiors', {})
                for sup_name, rel_type_name in superiors.items():
                    build_single_relationship(sup_name, char_name, rel_type_name)
                    processed_count += 1

                # 处理 subordinates
                subordinates = char_data.get('subordinates', {})
                for sub_name, rel_type_name in subordinates.items():
                    build_single_relationship(char_name, sub_name, rel_type_name)
                    processed_count += 1

            except Exception as e:
                print(f"处理人物时出错: {e} - {char_data}")
                skipped_count += 1

        print(f"处理完成: 总处理 {processed_count} 个关系，跳过/出错 {skipped_count} 个。")

    except FileNotFoundError:
        print(f"错误: 文件未找到 - {file_path}")
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败 - {e}")
    except Exception as e:
        print(f"错误: 构建关系时发生未知异常 - {e}")


if __name__ == '__main__':
    #reinitialize_continent()  #非自增 重新创建大洲
    #reinitialize_relation_types()
    #reinitialize_calamity()   #非自增
    #initialize_location_withoutrepeat()
    #initialize_chapter()       #非自增

    #initialize_chapter_location() #自增, 但避免重复
    initialize_character()
    #initialize_weapon()
    #build_relationship_from_characters()
