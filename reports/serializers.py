# reports/serializers.py
from rest_framework import serializers
from .models import Report, ReportMessage, Evidence, ForumPost, ForumReply, Resource


class ReportCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new report.
    """
    class Meta:
        model = Report
        fields = ['category', 'school_name', 'details', 'reporter_name', 'reporter_email']
    
    def create(self, validated_data):
        report = Report.objects.create(**validated_data)  # type: ignore[attr-defined]  # pylint: disable=no-member
        
        # Handle file uploads from request.FILES
        # FormData sends multiple files with the same key name
        request = self.context.get('request')
        if request and hasattr(request, 'FILES'):
            files = request.FILES.getlist('evidence_files')
            for file in files:
                Evidence.objects.create(report=report, file=file)  # type: ignore[attr-defined]  # pylint: disable=no-member
        
        return report


class ReportStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying report status and details.
    """
    class Meta:
        model = Report
        fields = ['case_id', 'category', 'school_name', 'details', 'reporter_name', 
                  'reporter_email', 'status', 'created_at', 'updated_at']
        read_only_fields = ['case_id', 'status', 'created_at', 'updated_at']


# --- ADD THESE NEW SERIALIZERS ---

class ReportMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying messages.
    """
    class Meta:
        model = ReportMessage
        fields = ['id', 'sender_type', 'message', 'created_at']


class ReportMessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new message from the user.
    """
    class Meta:
        model = ReportMessage
        fields = ['message']  # User only needs to send the message text


# --- FORUM SERIALIZERS ---

class ForumReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumReply
        fields = ['id', 'body', 'created_at']


class ForumPostSerializer(serializers.ModelSerializer):
    # This serializer is for the *list* of posts (no replies)
    reply_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'body', 'created_at', 'reply_count']


class ForumPostDetailSerializer(serializers.ModelSerializer):
    # This one is for a *single* post, and it includes the replies
    replies = ForumReplySerializer(many=True, read_only=True)

    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'body', 'created_at', 'replies']


class ForumReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumReply
        fields = ['body']  # User only needs to send the body

        # --- ADD THIS NEW SERIALIZER ---
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'category', 'phone', 'website']
        # ... (Your existing serializers) ...

# --- ADD THIS NEW SERIALIZER ---
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'category', 'phone', 'website']