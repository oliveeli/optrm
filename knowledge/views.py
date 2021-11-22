from django.shortcuts import render

from .models import Article,Category
from .forms import SearchForm

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class ServerListUserView(LoginRequiredMixin,generic.ListView):
    model = Article
    paginate_by = 10
    template_name = 'resourcemanager/article_list_user.html'

    def get_context_data(self, **kwargs):
        context = super(ServerListUserView, self).get_context_data(**kwargs)
        title = self.request.POST.get("title")
        content = self.request.POST.get("content")
        page_size = self.request.POST.get("page_size")
        page = self.request.POST.get("page")
        if page == None or page == "":
            page = 1
        if page_size == None or page_size == "":
            page_size = 10
        context['form'] = SearchForm({'page':page,'page_size':page_size,'title':title,'content':content})
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
        return  _do_query(self.request)
    
def _do_query(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    sql = Article.objects
    if title != None and title != "":
        sql = sql.filter(title__contains=title)
    if content != None and content != "":
        sql = sql.filter(content__contains=title)
    return sql.filter(user_group__in=request.user.groups.all()).distinct().order_by('-create_time')
