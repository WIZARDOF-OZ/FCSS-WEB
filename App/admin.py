from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin          # ← Unfold base for ALL admins
from .models import Dashboard, Banner, GalleryItem, About
from App.models import NewsletterSubscriber
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import path
from django.utils.html import format_html
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from django.conf import settings
from .models import NewsUpdate

import csv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

#   Auth        ─
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    pass

# Unfold config

class BaseAdmin(UnfoldModelAdmin):
    compressed_fields = False  # gives fields more breathing room
    warn_unsaved_changes = True


#   Existing models   ─
class CategoryAdmin(ModelAdmin):
    list_display = ('image_tag', 'title', 'add_date')
    search_fields = ('title',)


class DashboardAdmin(ModelAdmin):
    list_display = ('banner_title', 'add_date')


@admin.register(GalleryItem)
class GalleryItemAdmin(ModelAdmin):
    pass


@admin.register(About)
class AboutAdmin(ModelAdmin):
    pass


admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Banner, CategoryAdmin)


#   Brevo helpers    ─
def _send_brevo_email(to_email, subject, html_content):
    """Send a single transactional email through Brevo. Returns (success, error_msg)."""
    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        email_obj = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"email": settings.DEFAULT_FROM_EMAIL},
            subject=subject,
            html_content=html_content,
        )
        api_instance.send_transac_email(email_obj)
        return True, None
    except ApiException as e:
        return False, str(e)


def _build_newsletter_html(subject, body_html):
    """Wrap body content in the school's branded email layout."""
    return f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto; padding: 20px;">
  <div style="text-align: center; padding: 20px 0; background-color: #f8a800;">
    <img src="https://fcss-web.onrender.com/static/images/icon/school__logo-removebg-preview.png"
         alt="School Logo" style="height: 60px; margin-bottom: 8px;"><br>
    <h2 style="color: white; margin: 0;">Fatima Convent Senior Secondary School</h2>
    <p style="color: white; margin: 5px 0;">Fatima Nagar, Bongaon, Rangia, Assam</p>
  </div>
  <div style="padding: 30px; background-color: #fff; border: 1px solid #eee;">
    {body_html}
    <hr style="border:none; border-top:1px solid #eee; margin: 24px 0;">
    <p style="color: #999; font-size: 11px; margin: 0;">
      You are receiving this email because you subscribed to newsletters from
      Fatima Convent Senior Secondary School.<br>
      To unsubscribe, reply to this email with "Unsubscribe" in the subject line.
    </p>
  </div>
  <div style="text-align: center; padding: 15px; background-color: #333; color: white; font-size: 12px;">
    <p style="margin: 0;">Fatima Convent Senior Secondary School</p>
    <p style="margin: 5px 0;">📞 +91 9954950683 | ✉️ fatimaschoolrangia@gmail.com</p>
  </div>
</body>
</html>
"""


#   Newsletter Admin   
# FIX 1: Inherit from Unfold's ModelAdmin so the Unfold theme + templates work.
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ModelAdmin):   # ← was admin.ModelAdmin
    # Custom changelist template adds the "Compose Newsletter" button in the
    # object-tools area (top-right), consistent with Unfold's layout.
    change_list_template = 'admin/newsletter_subscriber_changelist.html'

    list_display    = ['email', 'subscribed_at', 'is_active', 'status_badge']
    list_filter     = ['is_active']
    search_fields   = ['email']
    readonly_fields = ['subscribed_at']
    ordering        = ['-subscribed_at']
    list_per_page   = 25

    actions = [
        'send_email_to_selected',
        'deactivate_selected',
        'activate_selected',
        'export_as_csv',
    ]

    #   Coloured status badge                         
    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#28a745;color:#fff;padding:2px 10px;'
                'border-radius:12px;font-size:11px;">Active</span>'
            )
        return format_html(
            '<span style="background:#dc3545;color:#fff;padding:2px 10px;'
            'border-radius:12px;font-size:11px;">Inactive</span>'
        )
    status_badge.short_description = 'Status'

    #   Extra URLs    
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'compose/',
                self.admin_site.admin_view(self.compose_email_view),
                name='newsletter_compose',
            ),
        ]
        return custom + urls

    #   Compose page (send to ALL active, or a session-stored selection)   
    def compose_email_view(self, request):
        # Are we in "selection" mode? Read IDs stored by send_email_to_selected.
        is_selection  = request.GET.get('selection') == '1'
        selected_ids  = request.session.get('newsletter_selected_ids', []) if is_selection else []

        if is_selection and selected_ids:
            qs = NewsletterSubscriber.objects.filter(id__in=selected_ids)
        else:
            qs = None   # means "all active" on send

        if request.method == 'POST':
            subject      = request.POST.get('subject', '').strip()
            body_html    = request.POST.get('body_html', '').strip()
            preview_only = request.POST.get('preview_only')

            if not subject or not body_html:
                messages.error(request, 'Subject and body are both required.')
                return HttpResponseRedirect(request.path)

            full_html = _build_newsletter_html(subject, body_html)

            if preview_only:
                return render(request, 'admin/newsletter_preview.html', {
                    'preview_html': full_html,
                    'subject': subject,
                    'body_html': body_html,
                    'title': 'Email Preview',
                    'opts': self.model._meta,
                })

            # Determine recipient set
            if qs is not None:
                subscribers = qs
            else:
                subscribers = NewsletterSubscriber.objects.filter(is_active=True)

            total   = subscribers.count()
            success = 0
            failed  = []

            for sub in subscribers:
                ok, err = _send_brevo_email(sub.email, subject, full_html)
                if ok:
                    success += 1
                else:
                    failed.append(sub.email)

            # Clear session selection after sending
            if is_selection:
                request.session.pop('newsletter_selected_ids', None)

            if failed:
                messages.warning(
                    request,
                    f'Sent to {success}/{total} subscribers. '
                    f'Failed: {", ".join(failed[:5])}{"…" if len(failed) > 5 else ""}',
                )
            else:
                messages.success(
                    request,
                    f'Newsletter sent successfully to {success} subscriber(s)!'
                )
            return HttpResponseRedirect('../')

        # GET — render compose form
        if qs is not None:
            active_count = qs.filter(is_active=True).count()
            total_count  = qs.count()
        else:
            active_count = NewsletterSubscriber.objects.filter(is_active=True).count()
            total_count  = NewsletterSubscriber.objects.count()

        context = {
            'title': 'Compose Newsletter',
            'opts': self.model._meta,
            'active_count': active_count,
            'total_count':  total_count,
            'is_selection': is_selection,
            'selected_ids': selected_ids,
        }
        return render(request, 'admin/newsletter_compose.html', context)

    #   Bulk action: send email to selected                 ─
    # FIX 2: Bulk actions cannot return a rendered page directly — Django ignores
    # the return value unless it's an HttpResponse.  Store selected IDs in the
    # session and redirect to the compose page, which reads them back.
    def send_email_to_selected(self, request, queryset):
        selected_ids = list(queryset.values_list('id', flat=True))
        request.session['newsletter_selected_ids'] = selected_ids
        # Redirect to the dedicated compose URL; compose_email_view handles the rest.
        return HttpResponseRedirect('compose/?selection=1')
    send_email_to_selected.short_description = '📧 Send email to selected subscribers'

    #   Compose page also handles "selection" mode              ─
    # (Override already present above — we patch compose_email_view to read session)

    #   Bulk: deactivate                           ─
    def deactivate_selected(self, request, queryset):
        count = queryset.update(is_active=False)
        messages.success(request, f'{count} subscriber(s) deactivated.')
    deactivate_selected.short_description = '🔴 Deactivate selected subscribers'

    #   Bulk: activate  
    def activate_selected(self, request, queryset):
        count = queryset.update(is_active=True)
        messages.success(request, f'{count} subscriber(s) activated.')
    activate_selected.short_description = '🟢 Activate selected subscribers'

    #   Bulk: export CSV                           ─
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="newsletter_subscribers.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Subscribed At', 'Is Active'])
        for sub in queryset:
            writer.writerow([sub.email, sub.subscribed_at.strftime('%Y-%m-%d %H:%M'), sub.is_active])
        return response
    export_as_csv.short_description = '📥 Export selected as CSV'

    #   Inject "Compose Newsletter" button on changelist           
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['compose_url']    = 'compose/'
        extra_context['active_count']   = NewsletterSubscriber.objects.filter(is_active=True).count()
        extra_context['inactive_count'] = NewsletterSubscriber.objects.filter(is_active=False).count()
        return super().changelist_view(request, extra_context=extra_context)
    


# New&Update
@admin.register(NewsUpdate)
class NewsUpdateAdmin(BaseAdmin):
    list_display = ['title', 'date', 'is_active']
    list_editable = ['is_active']
    list_display_links = ['title'] 