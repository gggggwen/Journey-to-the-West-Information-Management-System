from django.db import models
from django.contrib.auth.models import User  # 可选：关联用户
from django.utils import timezone  # 可选：时间戳


#看作一个模型,在Django的ORM中
class Character(models.Model):
    """
    角色模型：用于存储用户创建的西游记风格角色。

    字段说明：
    - id: 主键，自增整数（Django 默认 AutoField，从 1 开始自增）。显示时自动补零为 6 位（如 000001）。
    - name: 角色名称，必填。
    - image: 角色图片，支持 PNG/JPG 上传。
    - race: 种族，选择 人/妖/仙。
    - ability: 角色能力描述。
    - intro: 角色介绍。
    - organization_id: 所属组织，外键指向 Organization 模型。
    - created_at: 创建时间（自动）。
    """

    # 显式定义自增 ID 主键（Django 默认 AutoField，自增从 1 开始）
    id = models.AutoField(primary_key=True, verbose_name='ID')

    # 种族选择选项
    RACE_CHOICES = [
        ('人', '人'),
        ('妖', '妖'),
        ('仙', '仙'),
    ]

    name = models.CharField(max_length=100, verbose_name='人物名称', help_text='请输入角色名称')
    image = models.ImageField(upload_to='characters/%Y/%m/%d/', verbose_name='人物图片',
                              help_text='上传 PNG/JPG 格式图片',default=None)
    race = models.CharField(max_length=10, choices=RACE_CHOICES, verbose_name='种族', help_text='请选择人/妖/仙族')
    ability = models.CharField(max_length=200, verbose_name='能力', help_text='请输入角色能力描述')
    intro = models.TextField(verbose_name='介绍', help_text='请输入角色详细介绍')

    organization = models.CharField(max_length=100, verbose_name='组织名称', help_text='请输入组织名称',default='无组织')

    # 可选字段
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色列表'
        ordering = ['-created_at']  # 默认按创建时间降序

    def __str__(self):
        # ID 显示为 6 位补零格式（如 000001）
        formatted_id = f"{self.id:06d}"
        return f"{self.race}族 - {self.name} (ID: {formatted_id}, 组织: {self.organization})"

    @property
    def formatted_id(self):
        """属性方法：获取格式化 ID（6 位补零），可在模板中调用 {{ character.formatted_id }}"""
        return f"{self.id:06d}"

    def save(self, *args, **kwargs):
        # 可选：保存前图片处理（如缩放），需安装 Pillow
        super().save(*args, **kwargs)


class Weapon(models.Model):
    """
    武器模型：用于存储用户创建的西游记风格武器。

    字段说明：
    - id: 主键，自增整数（Django 默认 AutoField，从 1 开始自增）。显示时自动补零为 6 位（如 000001）。
    - name: 武器名称，必填。
    - image: 武器图片，支持 PNG/JPG 上传。
    - description: 武器描述。
    - owner_character: 拥有者，外键指向 Character 模型。
    - created_at: 创建时间（自动）。
    """

    # 显式定义自增 ID 主键（Django 默认 AutoField，自增从 1 开始）
    id = models.AutoField(primary_key=True, verbose_name='ID')

    name = models.CharField(max_length=100, verbose_name='武器名称', help_text='请输入武器名称')
    image = models.ImageField(upload_to='weapons/%Y/%m/%d/', verbose_name='武器图片',
                              help_text='上传 PNG/JPG 格式图片')
    description = models.TextField(verbose_name='描述', help_text='请输入武器详细描述')
    owner_character = models.ForeignKey(Character,
        on_delete=models.SET_NULL,
        verbose_name='拥有者',
        related_name='weapons',
        help_text='选择武器拥有者角色',
        null=True,
        blank=True,
        default=None)  # 显式默认 None，确保空值处理

    # 可选字段
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '武器'
        verbose_name_plural = '武器列表'
        ordering = ['-created_at']  # 默认按创建时间降序

    def __str__(self):
        # ID 显示为 6 位补零格式（如 000001）
        formatted_id = f"{self.id:06d}"
        owner_name = self.owner_character.name if self.owner_character else '未知'
        return f"{self.name} (ID: {formatted_id}) - 拥有者: {owner_name}"

    @property
    def formatted_id(self):
        """属性方法：获取格式化 ID（6 位补零），可在模板中调用 {{ weapon.formatted_id }}"""
        return f"{self.id:06d}"

    def save(self, *args, **kwargs):
        # 可选：保存前图片处理（如缩放），需安装 Pillow
        super().save(*args, **kwargs)




class Continent(models.Model):
    """
    大陆模型：用于存储西游记风格的大陆信息。

    字段说明：
    - id: 主键，自增整数（Django 默认 AutoField，从 1 开始自增）。显示时自动补零为 6 位（如 000001）。
    - name: 大陆名称，必填。
    - created_at: 创建时间（自动）。
    """

    # 显式定义自增 ID 主键（Django 默认 AutoField，自增从 1 开始）
    id = models.IntegerField(primary_key=True, verbose_name='ID',default=5)

    name = models.CharField(max_length=100, verbose_name='大陆名称', help_text='请输入大陆名称', unique=True)
    description = models.CharField(max_length=200 , verbose_name='描述' , help_text='请输入描述', blank=True)
    # 可选字段
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '大陆'
        verbose_name_plural = '大陆列表'
        ordering = ['-created_at']  # 默认按创建时间降序

    def __str__(self):
        # ID 显示为 6 位补零格式（如 000001）
        formatted_id = f"{self.id:06d}"
        return f"{self.name} (ID: {formatted_id})"

    @property
    def formatted_id(self):
        """属性方法：获取格式化 ID（6 位补零），可在模板中调用 {{ continent.formatted_id }}"""
        return f"{self.id:06d}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Character_Relationship(models.Model):
    """
    人物-人物关系模型：用于存储角色之间的关系。

    字段说明：
    - id: 主键，自增整数。
    - from_character_id: 关系发起方，外键指向 Character 模型。
    - to_character_id: 关系接收方，外键指向 Character 模型。
    - relationship_type_id: 关系类型，外键指向 Relationship_Type 模型。
    """

    # 显式定义自增 ID 主键
    id = models.AutoField(primary_key=True, verbose_name='关系 ID')

    # 关系发起方，外键指向 Character 模型
    from_character = models.ForeignKey(
        'Character',
        on_delete=models.CASCADE,
        related_name='from_relationships',
        verbose_name='关系发起方 ID',
        help_text='关系发起方（from_person_id）',
        default=None
    )

    # 关系接收方，外键指向 Character 模型
    to_character = models.ForeignKey(
        'Character',
        on_delete=models.CASCADE,
        related_name='to_relationships',
        verbose_name='关系接收方 ID',
        help_text='关系接收方（to_person_id）',
        default=None
    )

    # 关系类型，外键指向 Relationship_Type 模型
    relationship_type = models.ForeignKey(
        'Relationship_Type',
        on_delete=models.CASCADE,
        verbose_name='关系类型 ID',
        help_text='关系类型',
    )

    class Meta:
        verbose_name = '人物关系'
        verbose_name_plural = '人物关系列表'

    def __str__(self):
        return f"{self.from_character.name} → {self.to_character.name} ({self.relationship_type})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Location(models.Model):
    """
    地点模型：用于存储西游记风格的地点信息。

    字段说明：
    - id: 主键，自增整数（Django 默认 AutoField，从 1 开始自增）。显示时自动补零为 6 位（如 000001）。
    - name: 地点名称，必填。
    - description: 地点描述。
    - continent_id: 所属大陆，外键指向 Continent 模型。
    - created_at: 创建时间（自动）。
    """

    # 显式定义自增 ID 主键（Django 默认 AutoField，自增从 1 开始）
    id = models.AutoField(primary_key=True, verbose_name='ID')

    name = models.CharField(max_length=100, verbose_name='地点名称', help_text='请输入地点名称')
    description = models.TextField(verbose_name='描述', help_text='请输入地点详细描述', default="暂无")

    # 所属大陆，外键指向 Continent 模型
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, verbose_name='所属大陆',
                                     related_name='locations', help_text='选择地点所属大陆', null=True, blank=True)

    # 可选字段
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '地点'
        verbose_name_plural = '地点列表'
        ordering = ['-created_at']  # 默认按创建时间降序

    def __str__(self):
        # ID 显示为 6 位补零格式（如 000001）
        formatted_id = f"{self.id:06d}"
        continent_name = self.continent.name if self.continent else '无大陆'
        return f"{self.name} (ID: {formatted_id}, 大陆: {continent_name})"

    @property
    def formatted_id(self):
        """属性方法：获取格式化 ID（6 位补零），可在模板中调用 {{ location.formatted_id }}"""
        return f"{self.id:06d}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Chapter(models.Model):
    chapter_number = models.IntegerField(primary_key=True, verbose_name='回合号')
    title = models.CharField(max_length=255, verbose_name='回目标题')
    summary = models.TextField(verbose_name='大致内容')

    class Meta:
        db_table = 'chapter'
        verbose_name = '章节'
        verbose_name_plural = '章节'

    def __str__(self):
        return f'{self.chapter_number}: {self.title}'


class Chapter_Location(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')

    chapter = models.ForeignKey(
        'Chapter',
        on_delete=models.CASCADE,
        verbose_name='章节',
        related_name='chapter_locations'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
        verbose_name='地点',
        related_name='chapter_locations'
    )


    class Meta:
        db_table = 'chapter_location'
        verbose_name = '章节地点关联'
        verbose_name_plural = '章节地点关联列表'
        unique_together = ('chapter', 'location')  # 防止重复关联
        ordering = ['chapter__chapter_number', 'location__name']

    def __str__(self):
        return f"{self.chapter.title} - {self.location.name}"

class Calamity(models.Model):
    id = models.IntegerField(primary_key=True, default=82, verbose_name='磨难编号')
    title = models.CharField(max_length=255, verbose_name='标题')
    summary = models.TextField(verbose_name='大致内容')

    class Meta:
        db_table = 'calamity'
        verbose_name = '磨难'
        verbose_name_plural = '磨难'

    def __str__(self):
        return self.title


class Relationship_Type(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='关系id')
    type = models.CharField(max_length=100, verbose_name='关系名')
    description = models.TextField(verbose_name='描述', blank=True, null=True,default='')

    class Meta:
        db_table = 'relationship_type'
        verbose_name = '关系类型'
        verbose_name_plural = '关系类型'

    def __str__(self):
        return self.type
