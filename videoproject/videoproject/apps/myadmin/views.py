from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import *
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView  # 呈现给定模板，其中包含在URL中捕获的参数的上下文。

from comment.models import Comment
from video.models import Video, Classification
from videoproject.utils.pagenation import get_page_list
from videoproject.utils.public import SuperUserRequiredMixin, AdminUserRequiredMixin, ajax_required
from .forms import UserLoginForm, VideoPublishForm, VideoEditForm, ClassificationAddForm, ClassificationEditForm
from .models import MyChunkedUpload


# Create your views here.
def login(request):
    """
    管理员登陆
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.is_staff:
                # 通过if user is not None and user.is_staff来判断管理员，如果是管理员，则auth_login登录并redirect跳转到主页
                auth_login(request, user)
                return redirect('myadmin:index')
            else:
                form.add_error('', '请输入管理员账号')
    else:
        form = UserLoginForm()
    return render(request, 'myadmin/login.html', {'form': form})


def logout(request):
    """
    管理员登出
    :param request:
    :return:
    """
    auth_logout(request)
    return redirect('myadmin:login')


class AddVideoView(SuperUserRequiredMixin, TemplateView):
    """
    展示上传视频页面
    """
    template_name = 'myadmin/video_add.html'


class MyChunkedUploadView(ChunkedUploadView):
    model = MyChunkedUpload
    field_name = 'the_file'


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):
    model = MyChunkedUpload

    def on_completion(self, uploaded_file, request):
        print('uploaded--->', uploaded_file.name)
        pass

    def get_response_data(self, chunked_upload, request):
        video = Video.objects.create(file=chunked_upload.file)
        return {'code': 0, 'video_id': video.id, 'msg': 'success'}


class VideoPublishView(SuperUserRequiredMixin, generic.UpdateView):
    """
    视频发布视图
    """
    model = Video
    form_class = VideoPublishForm
    template_name = 'myadmin/video_publish.html'

    def get_context_data(self, **kwargs):
        # 视频分类是通过get_context_data()带过来的
        context = super(VideoPublishView, self).get_context_data(**kwargs)
        clf_list = Classification.objects.all().values()
        clf_data = {'clf_list': clf_list}
        context.update(clf_data)
        return context

    def get_success_url(self):
        return reverse('myadmin:video_publish_success')


class VideoPublishSuccessView(generic.TemplateView):
    """
    视频发布成功回调页面
    """
    template_name = 'myadmin/video_publish_success.html'


class VideoListView(AdminUserRequiredMixin, generic.ListView):
    model = Video
    template_name = 'myadmin/video_list.html'
    context_object_name = 'video_list'
    paginate_by = 10
    q = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return Video.objects.get_search_list(self.q)


class VideoEditView(SuperUserRequiredMixin, generic.UpdateView):
    """
    视频编辑
    """
    model = Video
    form_class = VideoEditForm
    template_name = 'myadmin/video_edit.html'

    def get_context_data(self, **kwargs):
        context = super(VideoEditView, self).get_context_data(**kwargs)
        clf_list = Classification.objects.all().values()
        clf_data = {'clf_list': clf_list}
        context.update(clf_data)
        return context

    def get_success_url(self):
        messages.success(self.request, "保存成功")
        return reverse('myadmin:video_edit', kwargs={'pk': self.kwargs['pk']})


@ajax_required
@require_http_methods(["POST"])
def video_delete(request):
    """
    后台删除视频
    :param request:
    :return:
    """
    if not request.user.is_superuser:
        return JsonResponse({"code": 1, "msg": "无删除权限"})
    video_id = request.POST['video_id']
    instance = Video.objects.get(id=video_id)
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})


class ClassificationListView(AdminUserRequiredMixin, generic.ListView):
    """
    分类列表
    """
    model = Classification
    template_name = 'myadmin/classification_list.html'
    context_object_name = 'classification_list'
    paginate_by = 10
    q = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ClassificationListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return Classification.objects.filter(title__contains=self.q)


class ClassificationAddView(SuperUserRequiredMixin, generic.View):
    """
    增加分类
    """

    def get(self, request):
        form = ClassificationAddForm()
        return render(self.request, 'myadmin/classification_add.html', {'form': form})

    def post(self, request):
        form = ClassificationAddForm(data=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return render(self.request, 'myadmin/classification_add_success.html')
        return render(self.request, 'myadmin/classification_add.html', {'form': form})


@ajax_required
@require_http_methods(["POST"])
def classification_delete(request):
    """
    删除分类
    :param request:
    :return:
    """
    if not request.user.is_superuser:
        return JsonResponse({"code": 1, "msg": "无删除权限"})
    classification_id = request.POST['classification_id']
    instance = Classification.objects.get(id=classification_id)
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})


class ClassificationEditView(SuperUserRequiredMixin, generic.UpdateView):
    """
    编辑视频分类
    """
    model = Classification
    form_class = ClassificationEditForm
    template_name = 'myadmin/classification_edit.html'

    def get_success_url(self):
        messages.success(self.request, "保存成功")
        return reverse('myadmin:classification_edit', kwargs={'pk': self.kwargs['pk']})


class CommentListView(AdminUserRequiredMixin, generic.ListView):
    """
    获取评论列表
    """
    model = Comment
    template_name = 'myadmin/comment_list.html'
    context_object_name = 'comment_list'
    paginate_by = 10
    q = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context

    def get_queryset(self):
        self.q = self.request.GET.get("q", "")
        return Comment.objects.filter(content__contains=self.q).order_by('-timestamp')


@ajax_required
@require_http_methods(["POST"])
def comment_delete(request):
    """
    删除评论
    :param request:
    :return:
    """
    if not request.user.is_superuser:
        return JsonResponse({"code": 1, "msg": "无删除权限"})
    comment_id = request.POST['comment_id']
    instance = Comment.objects.get(id=comment_id)
    instance.delete()
    return JsonResponse({"code": 0, "msg": "success"})
