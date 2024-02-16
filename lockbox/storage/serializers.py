from rest_framework import serializers

from storage.models import File, FileChunk


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"
        read_only_fields = File.readonly_fields


class FileChunkSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileChunk
        fields = "__all__"
        read_only_fields = FileChunk.readonly_fields

    def validate(self, data):
        data = super().validate(data)
        file = File.objects.get(lid=data["file"])

        if data["size"] > file.max_size_chunk_bytes:
            detail = f"'size' param is larger than max chunk size for file, {data["size"]} > {file.max_size_chunk_bytes}"
            raise serializers.ValidationError(detail)
        return data
