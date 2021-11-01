from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

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


class ServerListUserView(LoginRequiredMixin,generic.ListView):
    model = Server
    paginate_by = 10
    template_name = 'resourcemanager/server_list_user.html'

    def get_context_data(self, **kwargs):
        context = super(ServerListUserView, self).get_context_data(**kwargs)
        query = self.request.POST.get("query")
        server_group = self.request.POST.get("server_group")
        biz_system = self.request.POST.get("biz_system")
        context['form'] = SearchForm({'query':query,'server_group':server_group,'biz_system':biz_system})
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
    
    def get_queryset(self):
        query = self.request.POST.get("query")
        server_group = self.request.POST.get("server_group")
        biz_system = self.request.POST.get("biz_system")
        sql = Server.objects
        if query != None and query != "":
            sql = sql.filter(Q(name__contains=query) | Q(ip_address__contains=query))
        if server_group != None and server_group != "":
            sql = sql.filter(group__exact=server_group)
        if biz_system != None and biz_system != "":
            sql = sql.filter(biz_system__exact=biz_system)

        return sql.filter(user_group__in=self.request.user.groups.all()).distinct().order_by('name')