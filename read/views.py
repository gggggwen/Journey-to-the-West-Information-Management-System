from django.shortcuts import render
from create.tools import Query

#全局变量
Query = Query()

def main_page(request):
    return render(request, "main_page.html")

# Create your views here.
def get_page_read_main(request):
    return render(request,"read_mainpage.html")

def get_page_read_calamity(request):
    """
    渲染九九八十一难页面。
    从Calamity表查询所有难关数据，并传递给模板。
    """
    calamities = Query.all_calamity()  # 假设返回列表，每个元素为{'title': str, 'summary': str}
    return render(request, "read_calamity.html", {'calamities': calamities})


def get_page_read_character(request):
    characters = Query.all_character()
    print(characters)
    return render(request,"read_character.html",{'characters': characters})

def read_single_character(request, id):
    print(id)
    character = Query.single_character(id)
    print(character['image'])
    return render(request,"read_single_character.html",{'character': character})


def get_page_read_chapter(request):
    chapters = Query.all_chaptertitle()
    #print(chapters)
    return render(request, "read_chapter.html", {'chapters': chapters})

def read_single_chapter(request,chapter_number: int):
    chapter =Query.single_chapter(chapter_number)
    print(chapter)
    return render(request, "read_single_chapter.html",{'chapter': chapter})

def get_page_read_relationship(request):
    """
    1.获取Character_Relationship所有实例
    """
    data = Query.all_relationship()
    print(data)
    new_data = rm_repeated_relationship(data)
    print(new_data)
    return render(request,"read_relationship.html",{"relationships" : new_data})

def rm_repeated_relationship(data):
    """
    检测并删除对称重复的关系（即 A→B 和 B→A 同时存在的情况）
    """
    if not data:
        return data, []
    # 用来快速判断“反向关系是否已存在”
    seen_pairs = set()
    # 最终保留的关系
    cleaned = []
    # 被删除的关系 id
    removed = []

    for item in data:
        fid = item['from_character']['id']
        tid = item['to_character']['id']
        rel_id = item['id']

        # 构造两个方向的“标准化键”：始终让较小的 ID 在前
        forward = (min(fid, tid), max(fid, tid))
        backward = (max(fid, tid), min(fid, tid))  # 其实和 forward 一样

        key = forward  # 只需要一个方向的键即可

        if key in seen_pairs:
            # 已经出现过反向关系 → 当前这条是重复的，丢弃
            removed.append(rel_id)
            continue
        else:
            # 第一次遇到这个无向对，直接保留
            seen_pairs.add(key)
            cleaned.append(item)

    print(f"检测到 {len(removed)} 条对称重复关系，已自动移除（保留 id 较小的那条）")
    print("被移除的关系 ID：", removed)

    return cleaned



