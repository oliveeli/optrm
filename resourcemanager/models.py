from django.db import models
from django.urls import reverse 
import uuid 
from datetime import date
from django.contrib.auth.models import Group


class ServerGroup(models.Model):
    name = models.CharField(max_length=210)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "服务器分组"
        verbose_name_plural = "服务器分组"


class OperatingSystem(models.Model):
    name = models.CharField(max_length=220)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "操作系统"
        verbose_name_plural = "操作系统"


class Component(models.Model):
    name = models.CharField('名称',max_length=100)
    version = models.CharField('版本',max_length=10)
    def __str__(self):
        return self.name + ':' + self.version

    class Meta:
        verbose_name = "组件"
        verbose_name_plural = "组件"

class Port(models.Model):
    port = models.IntegerField("端口",unique=True)
    description = models.TextField('说明', max_length=512, blank=True, null=True )

    def __str__(self):
        return str(self.port)

    class Meta:
        verbose_name = "端口"
        verbose_name_plural = "端口"


class ComponentInstance(models.Model):
    component = models.ForeignKey(Component,  on_delete=models.CASCADE, null=True, verbose_name="组件")
    server = models.ForeignKey('Server',  on_delete=models.CASCADE, null=True)
    port = models.ManyToManyField(Port, blank=True, verbose_name="端口")

    def port_list(self):
        return ', '.join([str(a.port) for a in self.port.all()])
    

    class Meta:
        verbose_name = "组件实例"
        verbose_name_plural = "组件实例"


class BizSystem(models.Model):
    name = models.CharField(max_length=240)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "业务系统"
        verbose_name_plural = "业务系统"

class UserAndPassword(models.Model):
    name = models.CharField('名称',max_length=128, null=True, blank=False )
    user_name = models.CharField('账号',max_length=24)
    password = models.CharField('密码',max_length=64)

    def name_str(self):
        if self.name == None or self.name == '':
            return self.id
        else:
            return self.name

    name_str.short_description = '名称'

    def __str__(self):
        if self.name == None or self.name == '':
            return self.user_name + '/' + self.password
        else:
            return self.name

    class Meta:
        verbose_name = "账号密码"
        verbose_name_plural = "账号密码"

class Server(models.Model):
    name = models.CharField('名称',max_length=200)
    ip_address = models.CharField("IP地址",max_length=200)
    cpu_cores = models.IntegerField("CPU核数")
    memory_size = models.IntegerField("内存大小(G)")
    disc_sys_size = models.IntegerField("系统磁盘大小(G)")
    disc_biz_size = models.IntegerField("业务磁盘大小(G)", blank=True, null=True)

    operating_system = models.ForeignKey(OperatingSystem, blank=True, on_delete=models.SET_NULL, null=True,  verbose_name="操作系统")
    summary = models.TextField("备注", blank=True, null=True, max_length=1000)
    group = models.ManyToManyField(ServerGroup, blank=True, verbose_name="服务器分组")
    biz_system = models.ManyToManyField(BizSystem, blank=True, verbose_name="业务系统")
    user_group = models.ManyToManyField(Group, blank=True, verbose_name="授权用户组")

    remote_connect_ip = models.CharField("远程连接IP", blank=True, null=True, max_length=64)
    remote_connect_port = models.CharField("远程连接端口", blank=True, null=True, max_length=20)

    def cpu_cores_text(self):
        return str(self.cpu_cores) + '核'
    
    def memory_size_text(self):
        return str(self.memory_size) + 'G'
    
    def disc_sys_size_text(self):
        return str(self.disc_sys_size) + 'G'

    def disc_biz_size_text(self):
        if self.disc_biz_size != None:
            return str(self.disc_biz_size) + 'G'

    def groups_list(self):
        return ', '.join([a.name for a in self.group.all()])

    def biz_system_list(self):
        return ', '.join([a.name for a in self.biz_system.all()])
    
    def user_group_list(self):
        return ', '.join([a.name for a in self.user_group.all()])
    
    def remote_access_address(self):
        rs = ''
        if self.remote_connect_ip != None:
            rs += self.remote_connect_ip
        if self.remote_connect_port != None:
            rs += self.remote_connect_port
        return rs

    cpu_cores_text.short_description = 'CPU'
    memory_size_text.short_description = '内存'
    disc_sys_size_text.short_description = '系统盘'
    disc_biz_size_text.short_description = '业务盘'
    groups_list.short_description = "所属分组"
    biz_system_list.short_description = "所属业务系统"
    user_group_list.short_description = '授权组'

    def component_instance_list(self):
        return ComponentInstance.objects.filter(server=self)

    class Meta:
        verbose_name = "服务器"
        verbose_name_plural = "服务器"

    def get_absolute_url(self):
        return reverse('server-detail', args=[str(self.id)])

class ServerConnection(models.Model):
    user_and_password = models.ForeignKey(UserAndPassword, on_delete=models.CASCADE, null=True, verbose_name="账号密码")
    user_group = models.ManyToManyField(Group, blank=True, verbose_name="授权用户组")
    server = models.ForeignKey(Server, on_delete=models.CASCADE, null=True,  verbose_name="服务器")

    class Meta:
        verbose_name = "服务器连接"
        verbose_name_plural = "服务器连接"
