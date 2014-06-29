from django.http import HttpResponse
from django.views.generic import View

class QueryUrlPath(View):
    def dispatch(self, request, article, *args, **kwargs):
        max_num = kwargs.pop('max_num', 20)
        query = request.GET.get('query', None)
        
        if query:
            matches = models.URLPath.objects.can_read(request.user).active().filter(
                article__current_revision__title__contains=query,
                article__current_revision__deleted=False,
            )
            matches = matches.select_related_common()
            return [("[%s](wiki:%s)") % (m.article.current_revision.title, '/'+m.path.strip("/")) for m in matches[:max_num]]
        
        return []
