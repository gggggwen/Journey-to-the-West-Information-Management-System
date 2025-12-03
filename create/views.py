from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import transaction
from .models import Character, Weapon # 假设您的 Character 模型已定义

def main_page(request):
    return render(request, "main_page.html")

def check_obj_exists(name: str, table) -> bool:
    """
    检查角色是否在角色表中已经存在。
    """
    try:
        # 使用 filter().exists() 来检查是否存在该名称的角色
        # 这里假设 Character 模型有一个 name 字段
        return table.objects.filter(name=name).exists()
    except Exception as e:
        # 如果发生异常（比如数据库连接问题），记录错误并返回 False
        print(f"检查角色存在性时出错: {e}")
        return False

def process_character_submission(request):
    """
    处理表单提交数据并存入数据库。
    Args:
        request: Django HttpRequest 对象，包含 POST 和 FILES 数据。

    Returns:
        HttpResponseRedirect: 重定向到成功页面，或渲染表单页面（带错误）。

    假设：
    - Character 模型有字段：name (CharField), image (ImageField), race (CharField), ability (TextField), intro (TextField)。
    - 已安装 Pillow (pip install Pillow) 支持图像处理。
    - 图片处理省略：直接保存文件（可扩展为 resize/crop 等）。
    - 使用事务确保原子性。
    """
    if request.method != 'POST':
        # 非 POST 请求，返回空表单（或重定向）
        messages.info(request, '请使用表单提交数据。')
        return redirect('create_character')  # 假设 URL 名

    with transaction.atomic():  # 原子事务：成功全保存，失败全回滚
        try:
            # 提取非文件字段（忽略 CSRF，Django 中间件已验证）
            name = request.POST.get('name', '').strip()
            race = request.POST.get('race', '').strip()
            ability = request.POST.get('ability', '').strip()
            intro = request.POST.get('intro', '').strip()

            # 提取文件（图片处理省略：直接保存原文件）
            image = request.FILES.get('image')
            organization = request.POST.get('organization', '').strip()

            # 基本验证（可扩展为 Form 验证）
            if not all([name, race, ability, intro]):
                raise ValueError('所有文本字段不能为空。')
            if not image:
                raise ValueError('图片文件必填。')
            if not image.content_type.startswith('image/'):
                raise ValueError('上传文件必须是图片格式。')

            # 创建并保存模型实例
            character = Character.objects.create(
                name=name,  # e.g., '孙悟空'
                race=race,  # e.g., '妖'
                ability=ability,  # e.g., '金箍棒'
                intro=intro,  # e.g., '大闹天宫的齐天大圣...'
                image=image ,  # e.g., 'wukong.jpg' 二进制数据自动保存到 MEDIA_ROOT
                organization= organization
            )

            # 添加成功日志：打印到控制台（调试用）
            print(f"成功创建角色: {name} (ID: {character.id}, 种族: {race}, 创建时间: {character.created_at})")

            # 图片处理示例（省略核心，但可添加）：
            # from PIL import Image
            # if image:
            #     pil_image = Image.open(image)
            #     pil_image.thumbnail((200, 200))  # 缩略图
            #     pil_image.save(character.image.path, 'JPEG', quality=85)

            messages.success(request, f'角色 "{name}" 创建成功！ID: {character.id}')
            return redirect('create_character')  # 重定向避免重复提交

        except ValueError as ve:
            messages.error(request, f'验证失败：{str(ve)}')
        except Exception as e:
            messages.error(request, f'保存失败：{str(e)}')
            # 可记录日志：import logging; logger.error(f"Form error: {e}")

    # 失败时重渲染表单（保留数据）
    return render(request, 'create_character.html', {
        'name': request.POST.get('name', ''),
        'race': request.POST.get('race', ''),
        'ability': request.POST.get('ability', ''),
        'intro': request.POST.get('intro', ''),
        'image_error': '图片处理失败' if 'image' in locals() else None
    })


def process_weapon_submission(request):
    """
    处理武器表单提交数据并存入数据库。
    Args:
        request: Django HttpRequest 对象，包含 POST 和 FILES 数据。

    Returns:
        HttpResponseRedirect: 重定向到成功页面，或渲染表单页面（带错误）。

    假设：
    - Weapon 模型有字段：name (CharField), image (ImageField), description (TextField), owner_character (ForeignKey to Character)。
    - 已安装 Pillow (pip install Pillow) 支持图像处理。
    - 拥有者通过名称查找现有 Character 实例。
    - 图片处理省略：直接保存文件（可扩展为 resize/crop 等）。
    - 使用事务确保原子性。
    """
    if request.method != 'POST':
        # 非 POST 请求，返回空表单（或重定向）
        messages.info(request, '请使用表单提交数据。')
        return redirect('create_weapon')  # 假设 URL 名

    with transaction.atomic():  # 原子事务：成功全保存，失败全回滚
        try:
            # 提取非文件字段（忽略 CSRF，Django 中间件已验证）
            name = request.POST.get('name', '').strip()
            owner = request.POST.get('owner', '').strip()
            description = request.POST.get('description', '').strip()

            # 提取文件（图片处理省略：直接保存原文件）
            image = request.FILES.get('image')

            # 基本验证（可扩展为 Form 验证）
            if not all([name, owner, description]):
                raise ValueError('所有文本字段不能为空。')
            if not image:
                raise ValueError('图片文件必填。')
            if not image.content_type.startswith('image/'):
                raise ValueError('上传文件必须是图片格式。')

            # 查找拥有者角色
            try:
                owner_character = Character.objects.get(name=owner)
            except Character.DoesNotExist:
                raise ValueError(f'拥有者角色 "{owner}" 不存在，请先创建该角色。')

            # 创建并保存模型实例
            weapon = Weapon.objects.create(
                name=name,  # e.g., '金箍棒'
                description=description,  # e.g., '如意金箍棒，能大能小...'
                image=image,  # e.g., 'ruyi.jpg' 二进制数据自动保存到 MEDIA_ROOT
                owner_character=owner_character
            )

            # 添加成功日志：打印到控制台（调试用）
            print(f"成功创建武器: {name} (ID: {weapon.id}, 拥有者: {owner}, 创建时间: {weapon.created_at})")

            # 图片处理示例（省略核心，但可添加）：
            # from PIL import Image
            # if image:
            #     pil_image = Image.open(image)
            #     pil_image.thumbnail((200, 200))  # 缩略图
            #     pil_image.save(weapon.image.path, 'JPEG', quality=85)

            messages.success(request, f'武器 "{name}" 创建成功！ID: {weapon.id}，拥有者: {owner}')
            return redirect('create_weapon')  # 重定向避免重复提交

        except ValueError as ve:
            messages.error(request, f'验证失败：{str(ve)}')
        except Exception as e:
            messages.error(request, f'保存失败：{str(e)}')
            # 可记录日志：import logging; logger.error(f"Form error: {e}")

    # 失败时重渲染表单（保留数据）
    return render(request, 'create_weapon.html', {
        'name': request.POST.get('name', ''),
        'owner': request.POST.get('owner', ''),
        'description': request.POST.get('description', ''),
        'image_error': '图片处理失败' if 'image' in locals() else None
    })

# Create your views here.
def get_page_create_main(request):
    return render(request, "create_mainpage.html",)

def get_page_create_character(request):
    return render(request, "create_character.html",)

def get_page_create_weapon(request):
    return render(request, "create_weapon.html",)

def create_character_submit(request):
    if check_obj_exists(request.POST['name'],Character):
        print("用户输入的人物已经存在", request.POST['name'] )
        messages.error(request, '人物名称已存在，请重新输入！')  # 添加错误消息
        return redirect('create_character')  # 重定向回创建页面

    res = process_character_submission(request)
    return res

def create_weapon_submit(request):
    if(check_obj_exists(request.POST['name'],Weapon)):
        print("用户输入的武器已经存在", request.POST['name'] )
        messages.error(request, '武器名称已存在，请重新输入！')  # 添加错误消息
        return redirect('create_weapon')  # 重定向回创建页面

    if not (check_obj_exists(request.POST['owner'],Character)):
        print("该拥有者不存在", request.POST['owner'] )
        messages.error(request, '拥有者不存在, 请重新输入! ')
        return redirect('create_weapon')


    res = process_weapon_submission(request)
    return res