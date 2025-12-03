from create.models import Weapon, Character
from django.shortcuts import redirect, render
from django.contrib import messages
from create import tools

from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse

def main_page(request):
    return render(request, "main_page.html")

def process_delete(name, table, request):
    """
    处理角色删除请求，根据名称查找并删除 Character 实例。
    由于外键（如 Weapon 的 owner_character）设置为 on_delete=models.CASCADE，
    删除角色时会自动级联删除所有相关武器实例。

    Args:
        name (str): 角色名称。

    Returns:
        HttpResponseRedirect: 重定向到角色列表页面，或渲染错误页面。
    """
    if not name.strip():
        messages.error(request, '名称不能为空！')  # 假设 request 来自视图上下文
        return redirect('delete_character' if table==Character else 'delete_weapon')  # 假设 URL 名

    try:
        # 根据名称查找角色（假设名称唯一；若不唯一，可添加更多过滤）
        obj = table.objects.get(name=name.strip())

        # 删除角色实例（触发 CASCADE：自动删除所有 owner_character=character 的 Weapon）
        deleted_count, _ = obj.delete()  # 返回 (deleted, details) 元组

        # 记录删除日志（可选，打印到控制台）
        print(f"成功删除角色: {name} (ID: {obj.id})，级联删除了 {deleted_count} 个相关记录")

        messages.success(request, f'角色 "{name}" 删除成功！已级联删除 {deleted_count} 个相关记录。')
        return redirect('delete_character' if table==Character else 'delete_weapon')  # 重定向到列表页，避免重复提交

    except table.tDoesNotExist:
        messages.error(request, f'未找到名称为 "{name}" 的角色！')
        return redirect('delete_character' if table==Character else 'delete_weapon')

    except Exception as e:
        messages.error(request, f'删除失败：{str(e)}')
        print(f'删除失败：{str(e)}')
        # 可记录日志：import logging; logger.error(f"Delete error: {e}")
        return redirect('delete_character' if table==Character else 'delete_weapon')

# Create your views here.
def get_page_delete_main(request):
    return render(request, "delete_mainpage.html",)

def get_page_delete_character(request):
    # 查询所有存在的角色名称，作为下拉选项（优化：只取 name 字段的列表）
    characters = list(Character.objects.values_list('name', flat=True).distinct())
    context = {'characters': characters}
    return render(request, 'delete_character.html', context)  # 替换为你的模板路径

def get_page_delete_weapon(request):
    characters = list(Character.objects.values_list('name', flat=True).distinct())
    context = {'characters': characters}
    return render(request, "delete_weapon.html")


def delete_character_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            messages.error(request, '请选择角色名称！')
            return redirect('delete_character')

        if not tools.check_obj_exists(name, Character):
            print(f"该人物不存在: {name}")
            messages.error(request, '角色不存在，请重新选择！')
            return redirect('delete_character')

        # 由于设置了 on_delete=CASCADE，角色删除时相应武器也会被删除
        res = process_delete(name, Character, request)
        return res
    else:  # GET 请求，显示表单
        # 查询所有存在的角色名称，作为下拉选项（优化：只取 name 字段的列表）
        characters = list(Character.objects.values_list('name', flat=True).distinct())
        context = {'characters': characters}
        return render(request, 'delete_character.html', context)  # 替换为你的模板路径


def delete_weapon_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            messages.error(request, '请选择武器名称！')
            return redirect('delete_weapon')

        if not tools.check_obj_exists(name, Weapon):
            print(f"该武器不存在: {name}")
            messages.error(request, '武器不存在，请重新选择！')
            return redirect('delete_weapon')

        # 由于设置了 on_delete=CASCADE，武器删除时相关关联也会被处理
        res = process_delete(name, Weapon, request)
        return res
    else:  # GET 请求，显示表单
        # 查询所有存在的武器名称，作为下拉选项（优化：只取 name 字段的列表）
        weapons = list(Weapon.objects.values_list('name', flat=True).distinct())
        context = {'weapons': weapons}
        return render(request, 'delete_weapon.html', context)  # 替换为你的模板路径
