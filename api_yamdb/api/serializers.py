from rest_framework import serializers

from titles.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    def validate(self, attrs):
        if not (1 <= attrs.get('score') <= 10):
            raise serializers.ValidationError(
                'Score must be an integer value between 1 and 10.')
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date')
