from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    no_page_query_param = 'no_page'

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get(self.no_page_query_param) is not None:
            return None
        return super().paginate_queryset(queryset, request, view)
