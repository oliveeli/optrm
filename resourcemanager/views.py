from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.template import loader

from .models import Component,ComponentInstance,Server,ServerConnection,BizSystem,OperatingSystem,ServerGroup
from .forms import SearchForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.db.models import Q


def _check_permission(server_groups,user_groups):
    for a in user_groups:
        if a in server_groups:
            return True
    return False

def _quer_server_list(request):
    query = request.POST.get("query")
    server_group = request.POST.get("server_group")
    biz_system = request.POST.get("biz_system")
    component = request.POST.get("component")
    sql = Server.objects
    if query != None and query != "":
        sql = sql.filter(Q(name__contains=query) | Q(ip_address__contains=query))
    if server_group != None and server_group != "":
        sql = sql.filter(group__exact=server_group)
    if biz_system != None and biz_system != "":
        sql = sql.filter(biz_system__exact=biz_system)
    component_ids = set(())
    if component != None and component != "":
        ci = ComponentInstance.objects.filter(component__exact=component).distinct().distinct()
        added = False
        for c in ci:
            component_ids.add(c.server.id)
            added = True
        if added == True:
            sql = sql.filter(id__in=component_ids)
        else:
            return Server.objects.get_queryset().none()
    return sql.filter(user_group__in=request.user.groups.all()).distinct().order_by('ip_address_int')

@login_required
def server_detail(request, server_id):
    serv = Server.objects.get(pk=server_id)
    # 检查用户是否有权限查看该服务器详情
    permit = _check_permission(serv.user_group.all(),request.user.groups.all())
    if permit == False:
        return HttpResponse('你没有权限查看该服务器')
    
    pwd = ServerConnection.objects.filter(server=server_id).filter(user_group__in=request.user.groups.all()).distinct()
    return render(request, 'resourcemanager/server_detail.html', {'server': serv,'server_passwords':pwd})

class ServerDetailView(LoginRequiredMixin,generic.DetailView):
    model = Server

@login_required
def update_ips(request):
    
    servers = Server.objects.filter(ip_address_int__exact=0).distinct().all()
    for s in servers:
        print("ips = " + s.ip_address)
        s.save()
        
    return HttpResponse('success')

@login_required
def server_list_download(request):
    # Create the HttpResponse object with the appropriate CSV header.
    queryset = _quer_server_list(request)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="server-list.csv"'},
    )

    csv_data = (
        ('名称','IP地址', 'CPU','内存','系统盘大小','业务盘大小','操作系统','服务器分组','业务系统','远程连接IP','远程连接端口','对应端口','备注'),
    )

    for data in queryset:
        csv_data += ((data.name,data.ip_address,data.cpu_cores_text,data.memory_size_text,data.disc_sys_size_text,data.disc_biz_size_text,data.operating_system,data.groups_list,data.biz_system_list,data.remote_connect_ip,data.remote_connect_port,data.remote_connect_origin_port,data.summary),)

    t = loader.get_template('resourcemanager/my_template_name.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response    

class ServerListUserView(LoginRequiredMixin,generic.ListView):
    model = Server
    paginate_by = 10
    template_name = 'resourcemanager/server_list_user.html'

    def get_context_data(self, **kwargs):
        context = super(ServerListUserView, self).get_context_data(**kwargs)
        query = self.request.POST.get("query")
        server_group = self.request.POST.get("server_group")
        biz_system = self.request.POST.get("biz_system")
        component = self.request.POST.get("component")
        page_size = self.request.POST.get("page_size")
        page = self.request.POST.get("page")
        if page == None or page == "":
            page = 1
        if page_size == None or page_size == "":
            page_size = 10
        context['form'] = SearchForm({'page':page,'page_size':page_size,'query':query,'server_group':server_group,'biz_system':biz_system,'component':component})
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
    
    def get_queryset(self):
        if not self.request.GET._mutable:
            self.request.GET._mutable = True
        pagesize = self.request.POST.get("page_size")
        if pagesize != None and pagesize != "":
            self.paginate_by = pagesize
        else:
            self.paginate_by = 10
        page = self.request.POST.get("page")
        self.request.GET['page'] = page
        return  _quer_server_list(self.request)
        # query = self.request.POST.get("query")
        # server_group = self.request.POST.get("server_group")
        # biz_system = self.request.POST.get("biz_system")
        # component = self.request.POST.get("component")
        # sql = Server.objects
        # if query != None and query != "":
        #     sql = sql.filter(Q(name__contains=query) | Q(ip_address__contains=query))
        # if server_group != None and server_group != "":
        #     sql = sql.filter(group__exact=server_group)
        # if biz_system != None and biz_system != "":
        #     sql = sql.filter(biz_system__exact=biz_system)
        # component_ids = set(())
        # if component != None and component != "":
        #     ci = ComponentInstance.objects.filter(component__exact=component).distinct().distinct()
        #     added = False
        #     for c in ci:
        #         component_ids.add(c.server.id)
        #         added = True
        #     if added == True:
        #         sql = sql.filter(id__in=component_ids)
        
        # return sql.filter(user_group__in=self.request.user.groups.all()).distinct().order_by('name')