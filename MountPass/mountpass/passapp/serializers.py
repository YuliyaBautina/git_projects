from models import Coord, Level, PerevalAdded, Images, MyUser

from drf_writable_nested import WritableNestedModelSerializer

from rest_framework import serializers


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImagesSerializer(serializers.ModelSerializer):
    image = serializers.URLField()

    class Meta:
        model = Images
        fields = ['image', 'title']


class MyUserSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        self.is_valid()
        user = MyUser.objects.filter(email=self.validated_data.get('email'))

        if user.exists():
            return user.first()
        else:
            new_user = MyUser.objects.create(
                email=self.validated_data.get('email'),
                phone=self.validated_data.get('phone'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
            )
            return new_user

    class Meta:
        model = Users
        fields = ['email', 'phone', 'fam', 'name', 'otc']


class PerevalSerializer(WritableNestedModelSerializer):
    user = UsersSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect',
                  'add_time', 'status', 'user', 'coords', 'level', 'images']
        read_only_fields = ['status']

    def validate(self, data):
        if self.instance:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.email != data_user['email'],
                instance_user.phone != data_user['phone'],
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],

            ]
            if data_user and any(validating_user_fields):
                raise serializers.ValidationError('Rejected: user data cannot be modified')
            elif self.instance.status != data.get('status'):
                raise serializers.ValidationError('Rejected: status cannot be modified')
            elif self.instance.status != data.get('add_time'):
                raise serializers.ValidationError('Rejected: add_time cannot be modified')
        return data