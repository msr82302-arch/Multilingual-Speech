from rest_framework import serializers
from django.contrib.auth.models import User, Group


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=["Student", "Professor"])

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        role = validated_data.pop("role")

        user = User.objects.create_user(**validated_data)

        group = Group.objects.get(name=role)
        user.groups.add(group)

        return user