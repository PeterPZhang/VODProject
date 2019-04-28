# Create your models here.
from chunked_upload.models import ChunkedUpload


# Create your models here.
class MyChunkedUpload(ChunkedUpload):
    pass


# Override the default ChunkedUpload to make the `user` field nullable
MyChunkedUpload._meta.get_field('user').null = True
