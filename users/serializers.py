from rest_framework import serializers
from .models import User, Level
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        self.user = User.objects.filter(phone_number=attrs['phone_number']).first()
        if not self.user:
            raise serializers.ValidationError("Пользователь с таким номером телефона не найден.")

        if not self.user.check_password(attrs['password']):
            raise serializers.ValidationError("Неверный пароль.")

        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        return token

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'level', 'elo')
        read_only_fields = ('id', 'level', 'elo')

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone_number')

class LevelSerializer(serializers.ModelSerializer):
    theory_file = serializers.SerializerMethodField()

    class Meta:
        model = Level
        fields = ('id', 'name', 'description', 'bonus', 'theory_file')

    def get_theory_file(self, obj):
        if obj.theory_file:
            return self.context['request'].build_absolute_uri(obj.theory_file.url)
        return None

class LevelTheorySerializer(serializers.ModelSerializer):
    theory_file = serializers.SerializerMethodField()

    class Meta:
        model = Level
        fields = ('id', 'name', 'theory_file')

    def get_theory_file(self, obj):
        if obj.theory_file:
            return self.context['request'].build_absolute_uri(obj.theory_file.url)
        return None
