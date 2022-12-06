from rest_framework.serializers import ModelSerializer
from taggit.serializers import TagListSerializerField

from notesapp.models import Note


class NoteSerializer(ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Note
        fields = '__all__'
