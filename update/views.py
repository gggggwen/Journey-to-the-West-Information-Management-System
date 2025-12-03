from create.models import Location, Character, Weapon
import base64  # 用于base64编码
from django.shortcuts import render, redirect  # Django渲染模板
from django.contrib import messages  # 用于添加消息提示
from django.core.files.storage import default_storage  # 默认存储，用于读取文件

def main_page(request):
    return render(request, "main_page.html")
# Create your views here.
def get_page_update_main(request):
    return render(request,"update_mainpage.html")

def get_page_update_character(request):
    characters = list(Character.objects.values_list('name', flat=True).distinct())
    context = {'characters': characters}
    return render(request,"update_character.html",context)

def update_character_img(request):
    # 初始化变量
    character_name = None
    if request.method == 'POST':
        # 从POST请求中获取角色名称
        character_name = request.POST.get('character')
        print("角色名称", character_name)
        new_image = request.FILES.get('new_image')

        if character_name:
            try:
                # 根据角色名称查询Character对象
                character_obj = Character.objects.get(name=character_name)
                updated = False
                if new_image:
                    # 如果有新图片，更新到数据库
                    character_obj.image = new_image
                    character_obj.save()
                    updated = True
                    # 添加成功消息
                    messages.success(request, f'角色 {character_name} 的图片已更新成功。')
                    # 后台打印更新信息
                    print(f"后台: 角色 {character_name} 图片已更新。")
            except Character.DoesNotExist:
                # 处理角色不存在的错误
                messages.error(request, '角色未找到。')
                character_name = None
            except Exception as e:
                # 其他异常处理
                messages.error(request, f'更新失败：{str(e)}')
                print(f"后台错误: {str(e)}")
    # 为后台提供角色选择选项(数据库中select所有角色名)
    characters = list(Character.objects.values_list('name', flat=True).distinct())
    # 如果是GET请求或无character，character_name为None
    # 构建上下文字典
    context = {
        'character': character_name,
        'characters': characters,
    }
    # 渲染模板并返回响应（模板需包含messages显示）
    return render(request, "update_character_img.html", context)

def update_character_introduction(request):
    if request.method == 'POST':
        character_name = request.POST.get('name')
        introduction = request.POST.get('introduction')
        if character_name and introduction:
            try:
                character_obj = Character.objects.get(name=character_name)
                character_obj.intro = introduction
                character_obj.save()
                # 添加成功消息
                messages.success(request, f'角色 {character_name} 的介绍已更新成功。')
                # 后台打印更新信息
                print(f"后台: 角色 {character_name} 介绍已更新。")
            except Character.DoesNotExist:
                # 处理角色不存在的错误
                messages.error(request, '角色未找到。')
            except Exception as e:
                # 其他异常处理
                messages.error(request, f'更新失败：{str(e)}')
                print(f"后台错误: {str(e)}")
    # 为后台提供角色选择选项(数据库中select所有角色名)
    characters = list(Character.objects.values_list('name', flat=True).distinct())
    # 构建上下文字典
    context = {
        'characters': characters,
    }
    # 渲染模板并返回响应（模板需包含messages显示）
    return render(request, "update_character_introduction.html", context)


def get_page_update_weapon(request):
    weapons = list(Weapon.objects.values_list('name', flat=True).distinct())
    context = {'weapons': weapons}
    return render(request, "update_weapon.html",context)

def update_weapon_submit(request):
    weapons = list(Weapon.objects.values_list('name', flat=True).distinct())
    context = {'weapons': weapons}
    return render(request, "update_weapon.html", context)

def get_page_update_location(request):
    locations = list(Location.objects.values_list('name', flat=True).distinct())
    context = {'locations': locations}
    return render(request, "update_location_info.html", context)

def update_location_submit(request):
    locations = list(Location.objects.values_list('name', flat=True).distinct())
    context = {'locations': locations}
    return render(request, "update_location_info.html", context)