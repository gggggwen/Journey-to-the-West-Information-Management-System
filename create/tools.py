from django.core.files.storage import default_storage
from io import BytesIO
from .models import Character, Calamity, Chapter, Character_Relationship, Weapon  # 假设模型在当前app中
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import connection
import os
import json
from typing import List, Dict, Any

class Query:
    def __init__(self):
        pass

    def all_calamity(self):
        """
        使用Django ORM从Calamity表中查询所有九九八十一难（id从1到81），
        返回列表，每个元素为{'title': str, 'summary': str}，按id升序排列。
        """
        calamities = Calamity.objects.filter(id__range=(1, 81)).order_by('id')
        return [{'title': calamity.title, 'summary': calamity.summary} for calamity in calamities]


    def all_character(self):
        """
        查询 Character 模型中所有角色名，返回去重后的角色名列表。
        """
        # 使用 distinct() 确保唯一性，或转换为 set
        characters = Character.objects.all().order_by('id').distinct()
        return [{'name': character.name , 'id': character.id} for character in characters]
        # 或 return list(set(Character.objects.values_list('name', flat=True)))

    def all_chaptertitle(self):
        """
        使用Django ORM从Chapter表中查询所有章节实例，
        返回列表，每个元素为{'chapter_number': int, 'title': str, 'summary': str}，按chapter_number升序排列。
        """
        chapters = Chapter.objects.all().order_by('chapter_number')
        return [{'chapter_number': chapter.chapter_number, 'title': chapter.title} for chapter in chapters]


    def single_character(self, character_id):
        """
        根据 character_id 查询单个角色详情，包括多表关联的 relationships。
        返回字典：{
            'id': int,
            'name': str,
            'intro': str,
            'ability': str,
            'image': str (图片 URL，如果存在；否则 None),
            'relationships': list[dict]  # 每个关系: {'direction': 'from'|'to', 'related_character': {'id': int, 'name': str}, 'type': str}
        }。
        如果角色不存在，抛出 ObjectDoesNotExist 异常。
        """
        try:
            # 使用 prefetch_related 预加载关系，提高效率
            character = Character.objects.prefetch_related(
                'from_relationships__to_character',
                'from_relationships__relationship_type',
                'to_relationships__from_character',
                'to_relationships__relationship_type'
            ).get(id=character_id)

            # 构建 relationships 列表
            relationships = []

            # 出关系 (from_character)
            for rel in character.from_relationships.all():
                relationships.append({
                    'direction': 'from',  # 发起方
                    'related_character': {
                        'id': rel.to_character.id,
                        'name': rel.to_character.name
                    },
                    'type': rel.relationship_type.type
                })

            # 入关系 (to_character)
            for rel in character.to_relationships.all():
                relationships.append({
                    'direction': 'to',  # 接收方
                    'related_character': {
                        'id': rel.from_character.id,
                        'name': rel.from_character.name
                    },
                    'type': rel.relationship_type.type
                })

            return {
                'id': character.id,
                'name': character.name,
                'intro': character.intro,
                'ability': character.ability,
                'image': character.image.url if character.image else None,  # 获取图片 URL
                'relationships': relationships
            }
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"未找到 ID 为 {character_id} 的角色")

    def single_chapter(self,chapter_id):
        """
        根据前端传入的chapter_id（即chapter_number），查询Chapter表中的title和summary，
        并通过Chapter_Location关联查询Location表，获取该章节发生的所有地名（location.name）。
        返回字典：{'title': str, 'summary': str, 'locations': [str, ...]}。
        如果章节不存在，抛出ObjectDoesNotExist异常。
        """
        try:
            # 查询章节，使用prefetch_related预加载关联数据以提高效率
            chapter = Chapter.objects.prefetch_related('chapter_locations__location').get(chapter_number=chapter_id)

            # 提取地名列表
            locations = [cl.location.name for cl in chapter.chapter_locations.all()]

            return {
                'title': chapter.title,
                'summary': chapter.summary,
                'locations': locations,
                'chapter_number': chapter.chapter_number,
            }
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"未找到章节号为 {chapter_id} 的章节")

    def all_relationship(self,as_dict=True):
        """
        获取 Character_Relationship 表的所有关系数据。

        参数
        ----------
        relationship_id: int, optional
            - None      → 返回全部关系（QuerySet）
            - 具体 id   → 返回单条关系（抛异常或返回 None）
        as_dict: bool, default False
            - False → 返回 ORM 对象（QuerySet / 单实例）
            - True  → 返回序列化后的 Python dict（列表或单个 dict）

        返回
        ----------
        - relationship_id 为 None 且 as_dict=False → QuerySet[Character_Relationship]
        - relationship_id 为 None 且 as_dict=True  → List[dict]
        - relationship_id 有值且 as_dict=False    → Character_Relationship 实例
        - relationship_id 有值且 as_dict=True     → dict
        """
        # 预加载外键：发起方、接收方、关系类型（以及类型表的 name 字段）
        queryset = Character_Relationship.objects.all().select_related(
            'from_character',
            'to_character',
            'relationship_type'  # Relationship_Type 模型
        ).order_by('id')

        # ---------- 全部记录 ----------
        if not as_dict:
            return queryset

        # 批量转 dict（一次性遍历，效率更高）
        return [Query._rel_to_dict(rel) for rel in queryset]

        # ------------------------------------------------------------------
        # 辅助：单条关系 → dict（统一结构，前端/模板直接使用）
        # ------------------------------------------------------------------

    def all_weapon(self)->List[dict]:
        data  = Weapon.all_weapon()
        print(data)
        return data

    def _rel_to_dict(rel: Character_Relationship) -> dict:
        """
        把 Character_Relationship 实例转成纯字典。
        """
        return {
            'id': rel.id,
            'from_character': {
                'id': rel.from_character.id,
                'name': rel.from_character.name,
            },
            'to_character': {
                'id': rel.to_character.id,
                'name': rel.to_character.name,
            },
            'relationship_type': {
                'id': rel.relationship_type.id,
                'name': getattr(rel.relationship_type, 'type', ''),
                # 如果 Relationship_Type 有其他字段可继续补充
            },
            # 如有 direction / description 等额外字段，可在此添加
        }



def check_obj_exists(name: str, table) -> bool:
    """
    检查name是否在table表中已经存在。
    """
    if  name is None :
        return False

    try:
        # 使用 filter().exists() 来检查是否存在该名称的角色
        # 这里假设 Character 模型有一个 name 字段
        return table.objects.filter(name=name).exists()
    except Exception as e:
        # 如果发生异常（比如数据库连接问题），记录错误并返回 False
        print(f"检查角色存在性时出错: {e}")
        return False

