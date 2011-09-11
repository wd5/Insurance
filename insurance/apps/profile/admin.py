# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from profile.forms import AdminUserBlockForm
from profile.forms import AdminUserForm
from profile.models import UserProfile,Persona

csrf_protect_m = method_decorator(csrf_protect)



def unblock(modeladmin, request, queryset):
    queryset.update(is_active=True)
unblock.short_description = u"Разблокировать выбранных пользователей"

# def notification(modeladmin, request, queryset):
#     selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
#     return HttpResponseRedirect("notification/?ids=%s" % ",".join(selected))
# notification.short_description = u"Разослать уведомления"


# Should NOT use mass block feature as one can't normally specify block reason
# this way.
#
# def block(modeladmin, request, queryset):
# queryset.update(is_active=False) block.short_description = u"Заблокировать
# выбранных пользователей"


class CustomUserAdmin(UserAdmin):
    # actions= [ unblock, message ]
    actions= [ unblock ]
    list_display = ('last_name', 'first_name',
                    'email', 'p_last_ip', 'p_city', 'p_reason_blocked', 'is_active')
    list_display_links = ('email','last_name', 'first_name')

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Почта', {'fields': ('email',)}),
        ('Права', {'fields': ('is_staff', 'is_superuser', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Группы', {'fields': ('groups',)}),
    )

    # 
    form = AdminUserForm
    user_block_form = AdminUserBlockForm
    user_block_template = 'admin/auth/user/user_block.html'

    # ===== Profile field getters =====

    def p_last_ip(self, user):
        profile = user.get_profile()
        return profile.last_ip
    p_last_ip.short_description = 'Последний IP-адрес'

    def p_city(self, user):
        profile = user.get_profile()
        return profile.city
    p_city.short_description = 'Город'

    def p_reason_blocked(self, user):
        profile = user.get_profile()
        return profile.reason_blocked
    p_reason_blocked.short_description = 'Причина блокировки'

    # ==== Additional urls =====

    def __call__(self, request, url):
        if url is None:
            return self.changelist_view(request)
        additional = {
            'block': self.user_block,
            'unblock': self.user_unblock
        }
        for ad_url, view in additional:
            if url.endswith(ad_url):
                return additional[ad_url](request, url.split('/')[0])
        return super(UserAdmin, self).__call__(request, url)

    def get_urls(self):
        from django.conf.urls.defaults import patterns
        return patterns('',
                        (r'^(\d+)/block/$', self.admin_site.admin_view(self.user_block)),
                        (r'^(\d+)/unblock/$', self.admin_site.admin_view(self.user_unblock))
        ) + super(UserAdmin, self).get_urls()

    # ===== Custom actions =====

    def user_block(self, request, id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=id)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if request.method == 'POST':
            print request.POST
            form = self.user_block_form(profile, request.POST)
            if form.is_valid():
                form.save()
                msg = 'Пользователь заблокирован.'
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.user_block_form(profile)


        fieldsets = [(None, {'fields': form.base_fields.keys()})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        return render_to_response(self.user_block_template, {
            'title': u'Заблокировать пользователя с почтой %s' % user.email,
            'adminForm': adminForm,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            'root_path': self.admin_site.root_path,
        }, context_instance=RequestContext(request))

    def user_unblock(self, request, id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=id)
        user.is_active = True
        profile = user.get_profile()
        profile.reason_blocked = None
        user.save()
        profile.save()
        msg = 'Пользователь разблокирован.'
        messages.success(request, msg)
        return HttpResponseRedirect('..')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('u_last_name', 'u_first_name',
                    'u_email', 'last_ip', 'city', 'reason_blocked', 'u_is_active')
    list_display_links = ('u_email','u_last_name', 'u_first_name')
    readonly_fields = ('last_ip', 'city', 'reason_blocked')
    
    # ===== User field getters =====
    def u_last_name(self, profile):
        return profile.user.last_name
    u_last_name.short_description = 'Фамилия'

    def u_first_name(self, profile):
        return profile.user.first_name
    u_first_name.short_description = 'Имя'

    def u_email(self, profile):
        return profile.user.email
    u_email.short_description = 'Адрес электронной почты'

    def u_is_active(self, profile):
        return profile.user.is_active
    u_is_active.short_description = 'Активный'

class PersonaAdmin(admin.ModelAdmin):
    list_display   = ('id','last_name','first_name','middle_name','me')



admin.site.unregister(User) 
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Persona, PersonaAdmin)

