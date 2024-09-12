menu = [
    # {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить задачу", 'url_name': 'tasks:create_task'},
    # {'title': "Обратная связь", 'url_name': 'contact'},
    # {'title': "Войти", 'url_name': 'login'}
]


class DataMixin:
    title_page = None
    extra_context = {}

    def get_mixin_context(self, **kwargs):
        context = kwargs
        if self.title_page:
            context['title'] = self.title_page

        context['menu'] = menu
        return context