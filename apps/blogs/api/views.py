# from rest_framework import generics, status, permissions
# from .serializers import TagSerializer, PostSerializer, PostCreateSerializer
# from ..models import Tag, Post
# from rest_framework.response import Response
#
#
# class TagListView(generics.ListAPIView):
#     # http://127.0.0.1:8000/blog/api/tag/list/
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#
#
# class TagCreateView(generics.CreateAPIView):
#     # http://127.0.0.1:8000/blog/api/tag/create/
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class TagRUDView(generics.RetrieveUpdateDestroyAPIView):
#     # http://127.0.0.1:8000/blog/api/tag/rud/<int:pk>/
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class PostListView(generics.ListAPIView):
#     # http://127.0.0.1:8000/blog/api/post/list/
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class PostCreateView(generics.CreateAPIView):
#     # http://127.0.0.1:8000/blog/api/post/create/
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class PostRUDView(generics.RetrieveUpdateDestroyAPIView):
#     # http://127.0.0.1:8000/blog/api/post/rud/<int:pk>/
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (permissions.IsAuthenticated,)




