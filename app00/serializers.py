from rest_framework import serializers
from .models import Post, Tag
from django.contrib.auth import get_user_model
import datetime
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

# serializers.ModelSerializer.is_valid()
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) #
    tags = TagSerializer(many=True, read_only=True) #
    time = serializers.DateTimeField(read_only=True) #

    # author = serializers.RelatedField(queryset=User.objects.all())
    # author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Post
        fields = ("author", 'title', 'body', 'tags', 'time')
        # read_only_fields = ['author','tags','time'] # 왜 안되지? 된다고 했는뎅 흥

    def create(self, validated_data): # 뷰셋 perform create에서 save를 호출한다
        print('serializer: ',validated_data) # 여기에 tags가 없어! 뷰셋에서 처리했어야 했나 ?
        # validated_data['tags'] = Tag
        validated_data['time'] = datetime.datetime.now() # 그래서 여기서 넣은건가 ?
        tags_data = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            # tag = Tag.objects.create(name=tag_data['name']) # tag_data그대로 줬더니 매개2개가 왔대
            tag = Tag.objects.get(pk=tag_data['id']) # 처음에 create하다가 이건 좀 아닌거 같아서 get으로 바꿨당
            # print('태그 정보',tag_data)
            print('태그 타입', type(tag_data))
            post.tags.add(tag) ## list로 받고 append ? add ?

            # 뭘해도 post를 리턴해야지..
        return post#super().create(validated_data) # 부모에서 ManyToMany를 처리하므로 자식에서 구현 ?
    # 부모 create에서 마지막에 create한 instance를 반환하므로 여기서 생성한 post반환하면 끝나겠구나

    # 시리얼라이저 create가 호출되면, 멤버 모델을 갖는다
    # Many to Many를 처리하는데 ?
    # create 마지막에 객체를 반환하는듯 ?

