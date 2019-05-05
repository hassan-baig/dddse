from rest_framework import serializers
from . models import feedbacks, analyzedFeedbacks, wish, account, democratic, related, game
# This add serializers for Django Rest Framework API generation


class feedbacksSerializers(serializers.ModelSerializer):
    class Meta():
        model = feedbacks
        fields = ('DateTime', 'id', 'category', 'text', 'bw')


class analyzedfeedbacksSerializers(serializers.ModelSerializer):
    class Meta():
        model = analyzedFeedbacks
        fields = ('DateTime', 'id', 'fid', 'category',
                  'text', 'bw', 'related')


class wishSerializers(serializers.ModelSerializer):
    class Meta():
        model = wish
        fields = ('fid', 'id', 'category',
                  'text', 'related')


class demoSerializers(serializers.ModelSerializer):
    class Meta():
        model = democratic
        fields = ('title', 'id', 'category', 'description',
                  'dueDate', 'filePath', 'fid', 'pvotes', 'nvotes')


class accountSerializers(serializers.ModelSerializer):
    class Meta():
        model = account
        fields = ('name', 'surname', 'country',
                  'street', 'Nr', 'city', 'zipCode', 'dob', 'email', 'username', 'password')


class relatedFeedbacks(serializers.ModelSerializer):
    class Meta():
        model = related
        fields = ('followed', 'follower')


class games(serializers.ModelSerializer):
    class Meta():
        model = game
        fields = ('imagePath', 'a', 'b', 'c', 'd', 'right')
