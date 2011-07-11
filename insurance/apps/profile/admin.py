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

from profile.forms import AdminUserBlockForm
from profile.models import UserProfile



def unblock(modeladmin, request, queryset):
    queryset.update(is_active=True)
unblock.short_description = u"Разблокировать выбранных пользователей"

def block(modeladmin, request, queryset):
    queryset.update(is_active=False)
block.short_description = u"Заблокировать выбранных пользователей"

class CustomUserAdmin(UserAdmin):
    actions= [ block, unblock ]
    list_display = ('p_last_name', 'p_first_name', 'p_middle_name',
                    'email', 'p_last_ip', 'p_city', 'p_reason_blocked', 'is_active')
    list_display_links = ('email','p_last_name', 'p_first_name', 'p_middle_name')

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Почта', {'fields': ('email',)}),
        ('Права', {'fields': ('is_staff', 'is_superuser', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Группы', {'fields': ('groups',)}),
    )

    user_block_form = AdminUserBlockForm
    user_block_template = 'admin/auth/user/user_block.html'

    def p_last_ip(self, user):
        profile = user.get_profile()
        return profile.last_ip
    p_last_ip.short_description = 'Последний IP-адрес'

    def p_city(self, user):
        profile = user.get_profile()
        return profile.city
    p_city.short_description = 'Город'

    def p_last_name(self, user):
        profile = user.get_profile()
        return profile.last_name
    p_last_name.short_description = 'Фамилия'

    def p_first_name(self, user):
        profile = user.get_profile()
        return profile.last_name
    p_first_name.short_description = 'Имя'

    def p_middle_name(self, user):
        profile = user.get_profile()
        return profile.last_name
    p_middle_name.short_description = 'Отчество'

    def p_reason_blocked(self, user):
        profile = user.get_profile()
        return profile.reason_blocked
    p_reason_blocked.short_description = 'Причина блокировки'

    def __call__(self, request, url):
        if url is None:
            return self.changelist_view(request)
        if url.endswith('block'):
            return self.user_block(request, url.split('/')[0])
        elif url.endswith('unblock'):
            return self.user_block(request, url.split('/')[0])
        return super(UserAdmin, self).__call__(request, url)

    def get_urls(self):
        from django.conf.urls.defaults import patterns
        return patterns('',
            (r'^(\d+)/block/$', self.admin_site.admin_view(self.user_block)),
            (r'^(\d+)/unblock/$', self.admin_site.admin_view(self.user_unblock))
        ) + super(UserAdmin, self).get_urls()

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
        user.save()
        msg = 'Пользователь разблокирован.'
        messages.success(request, msg)
        return HttpResponseRedirect('..')
    
admin.site.unregister(User) 
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
