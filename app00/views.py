from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Post, Tag
from .serializers import PostSerializer, TagSerializer

User = get_user_model()

# ModelViewSet.create()

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
# TagSerializer.save()

    def perform_create(self, serializer):
        # self.create()
        # self.update()
        # self.retrieve()
        # self.destroy()
        # self.get_object()
        # print('view: ', serializer)  # 여기는 tag가 보인다! 추출 ? 이건 할 수 있다
        # print('serializer.data: ', serializer.data) # save()하기 전에는 serializer.data에 접근할 수 없대!
        # serializer에 접근하고 나서 save() 호출할 수 없다고 한다
        # 데베에 커밋하기 전에 데이터에 접근하고 싶다면 serializer.validated_data에서 점검해야 한다 !

        # 그럼 self.request.data를 출력해보자!
        # print('request: ', self.request.data)
        # 이게 왜 안되냐면? request.data를 시리얼라이저에 넣어서 그래
        # 그게 시리얼라이저.data가 되고 그 다음에 save를 하지 -- 아무튼 그래서 save()하기 전에는 request에서 접근못함
        author = User.objects.get(pk=self.request.data["author"])
        tags = self.request.data['tags'] # 이러면 id list ?
        # 아니@ id, name 다 들어간다 !!
        # Tag 시리얼라이저에서 id, name 모두 지정했기 때문인가 ?
        
        # self.request는 어디어 오는걸까 ?
        # APIView의 dispatch가 매개로 받아와 멤버에 저장한다
        # 그럼 dispatch는 어디서 호출되는 걸까?
        # dispatch()` is pretty much the same as Django's regular dispatch ㅋㅋ뭐래..
        # dispatch 뭐하는 애야? 매칭되는 뷰 없으면 에러 발생시키고 그런애 맞나 ?
        # tags = Tag.objects.get(pk=self.request.data["tags"]) # ??
        serializer.save(author=author, tags=tags)

        # 시리얼라이저 save를 하면 어떻게 되느냐 ?
        # save를 호출하면 validated_data를 갖고 create 또는 udate한다
        # 그래서 시리얼라이저의 create가 실행되는건가 ?

# class TagViewSet(ModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
# Create your views here.
