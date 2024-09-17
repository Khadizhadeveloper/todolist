from django.contrib import admin
from tasks.models import Tasks
from django.utils.safestring import mark_safe

class StatusFilter(admin.SimpleListFilter):
    title='Статусы задач'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('Not started', 'Не начато'),
            ('In process', 'В процессе'),
            ('Completed', 'Выполнено'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'In process':
            return queryset.filter(status='In process')
        elif self.value() == 'Completed':
            return queryset.filter(status='Completed')
        elif self.value() == 'Not started':
            return queryset.filter(status='Not started')
        return queryset

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'status')
    search_fields = ('name', 'status')
    list_filter = ( StatusFilter ,)
