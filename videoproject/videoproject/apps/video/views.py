from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from video.models import Video, Classification
from django.shortcuts import get_object_or_404
from videoproject.utils import pagenation
from videoproject.utils.public import ajax_required
from .forms import CommentForm
from django.views.decorators.http import require_http_methods


# Create your views here.


class IndexView(generic.ListView):
    model = Video
    template_name = 'video/index.html'  # 告诉ListView要使用我们已经创建的模版文件
    context_object_name = 'video_list'  # 上下文变量名，告诉ListView，在前端模版文件中，可以使用该变量名来展现数据

    paginate_by = 12  # 分页每页显示12条
    c = None

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        ListView视图类中的一个函数，在 get_context_data() 函数中，可以传一些额外内容到模板。因此我们可以使用该函数来传递分类数据
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = pagenation.get_page_list(paginator, page)
        classification_list = Classification.objects.filter(status=True).values()
        context['c'] = self.c
        context['classification_list'] = classification_list
        context['page_list'] = page_list
        return context

    def get_queryset(self):
        self.c = self.request.GET.get("c", None)
        if self.c:
            classification = get_object_or_404(Classification, pk=self.c)  # 获取视频类别
            return classification.video_set.all().order_by('-create_time')
        else:
            return Video.objects.filter(status=0).order_by('-create_time')


class SearchListView(generic.ListView):
    model = Video
    template_name = 'video/search.html'
    context_object_name = 'video_list'
    paginate_by = 8
    q = ''

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return Video.objects.filter(title__contains=self.q).filter(status=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = pagenation.get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context


class VideoDetailView(generic.DetailView):
    """
    视频详情页
    """
    model = Video
    template_name = 'video/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.increase_view_count()  # 调用自增函数
        return obj

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        context['form'] = form
        return context


@ajax_required
# 验证request必须是post请求
@require_http_methods(["POST"])
def like(request):
    if not request.user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    video_id = request.POST['video_id']
    video = Video.objects.get(pk=video_id)
    user = request.user
    video.switch_like(user)
    return JsonResponse({"code": 0, "likes": video.count_likers(), "user_liked": video.user_liked(user)})


@ajax_required
@require_http_methods(["POST"])
def collect(request):
    if not request.user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    video_id = request.POST['video_id']
    video = Video.objects.get(pk=video_id)
    user = request.user
    video.switch_collect(user)
    return JsonResponse({"code": 0, "collects": video.count_collecters(), "user_collected": video.user_collected(user)})
