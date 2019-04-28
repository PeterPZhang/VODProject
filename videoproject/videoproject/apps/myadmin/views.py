from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import *
from django.views import generic
from django.views.generic import TemplateView  # 呈现给定模板，其中包含在URL中捕获的参数的上下文。

from video.models import Video, Classification
from videoproject.utils.public import SuperUserRequiredMixin
from .forms import UserLoginForm, VideoPublishForm
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
