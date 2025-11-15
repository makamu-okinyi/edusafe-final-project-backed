# reports/admin.py
from django.contrib import admin
from .models import Report, Evidence, ReportMessage, ForumPost, ForumReply, Resource

class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 1

# --- ADD THIS INLINE CLASS FOR MESSAGES ---
class ReportMessageInline(admin.TabularInline):
    model = ReportMessage
    fields = ('sender_type', 'message', 'created_at')
    readonly_fields = ('created_at',)
    extra = 1 # Show one extra slot to reply

    def get_formset(self, request, obj=None, **kwargs):
        """
        Default new messages added in admin to be from 'Authority'
        """
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['sender_type'].initial = ReportMessage.SenderTypeChoices.AUTHORITY
        return formset
# ---

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'category', 'school_name', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('case_id', 'school_name')
    readonly_fields = ('case_id', 'created_at', 'updated_at')
    
    # --- ADD ReportMessageInline TO THIS LIST ---
    inlines = [EvidenceInline, ReportMessageInline]

    fieldsets = (
        ('Report Information', {
            'fields': ('case_id', 'category', 'school_name', 'details')
        }),
        ('Reporter Information', {
            'fields': ('reporter_name', 'reporter_email'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
# --- Add these for the forum ---
class ForumReplyInline(admin.TabularInline):
    model = ForumReply
    fields = ('body', 'created_at')
    readonly_fields = ('created_at',)
    extra = 0 # Don't show empty slots

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'body')
    inlines = [ForumReplyInline]

@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'created_at')
    search_fields = ('body',)

    # --- ADD THIS FOR THE RESOURCES ---
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'phone', 'website')
    list_filter = ('category',)
    search_fields = ('name', 'description')