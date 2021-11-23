from django.shortcuts import render

from .models import Article,Category
from .forms import SearchForm

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template import Context, Template

@login_required
def article_detail(request, article_id):
    artic = Article.objects.get(pk=article_id)
    # 检查用户是否有权限查看该服务器详情
    # permit = _check_permission(artic.user_group.all(),request.user.groups.all())
    # if permit == False:
    #     return HttpResponse('你没有权限查看该服务器')
    
    return render(request, 'knowledge/article_detail.html', {'article': artic})

    #   <li><span>Folder 1</span>
    #     <ul>
    #       <li><span>Item 1.1</span></li>
    #     </ul>
    #   </li>
# item_template = Template("<li><span>{{ name }}</span>{{ child }}</li>")
# item_template = Template("<ul><li><span>{{ name }}</span>{{ child }}</li></ul>")
item_template = '<li><a href="javascript:goto_category(%s)">%s</a>%s</li>'
item_template_selected = '<li><a id="tree_selected" href="javascript:goto_category(%s)">%s</a>%s</li>'

def _get_child(selected_category_id,id):
    categorys = Category.objects.filter(parent_id=id).order_by('tree_id')
    if categorys == None or categorys.count() == 0:
        return ''
    else:
        html = '<ul>'
        for c in categorys:
            child = _get_child(selected_category_id,c.id)
            if c.id == selected_category_id:
                html += item_template_selected % (c.id, c.name, child)
            else:
                html += item_template % (c.id, c.name, child)
        html += '</ul>'
        return html
            
    
def _get_tree_html(selected_category_id):

    if selected_category_id!=None and selected_category_id != '':
        selected_category_id = int(selected_category_id)
    else:
        selected_category_id = -100
    print("------------------")
    print(selected_category_id)
    category_root = Category.objects.filter(level=0).order_by('tree_id')
    html = ''
    for c in category_root:
        child = _get_child(selected_category_id,c.id)
        if c.id == selected_category_id:
            html += item_template_selected % (c.id, c.name, child)
        else:
            html += item_template % (c.id, c.name, child)
    return html

class ArticleListUserView(LoginRequiredMixin,generic.ListView):
    model = Article
    paginate_by = 10
    template_name = 'knowledge/article_list_user.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleListUserView, self).get_context_data(**kwargs)
        title = self.request.POST.get("title")
        content = self.request.POST.get("content")
        page_size = self.request.POST.get("page_size")
        page = self.request.POST.get("page")
        category = self.request.POST.get("category")
        if page == None or page == "":
            page = 1
        if page_size == None or page_size == "":
            page_size = "10"
        context['form'] = SearchForm({'page':page,'page_size':page_size,'title':title,'content':content,'category':category})
        
        context['category_html'] = _get_tree_html(category)
        
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
    category = request.POST.get("category")
    sql = Article.objects
    if category != None and category != "":
        # category_ids = 
        categorys = Category.objects.get(pk=int(category)).get_descendants(include_self=True)
        if categorys != None and categorys.count() != 0:
            category_ids = set(())
            for c in categorys:
                category_ids.add(c.id)
            sql = sql.filter(category__in=category_ids)
    if title != None and title != "":
        sql = sql.filter(title__contains=title)
    if content != None and content != "":
        sql = sql.filter(content__contains=title)
    return sql.filter(user_group__in=request.user.groups.all()).distinct().order_by('-create_time')
