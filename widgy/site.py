from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from widgy import registry
from widgy.views import (
    NodeView,
    ContentView,
    ShelfView,
    NodeEditView,
    NodeTemplatesView,
)


class WidgySite(object):
    def __init__(self):
        self.node_view = self.get_node_view()
        self.content_view = self.get_content_view()
        self.shelf_view = self.get_shelf_view()
        self.node_edit_view = self.get_node_edit_view()
        self.node_templates_view = self.get_node_templates_view()

    def get_registry(self):
        return registry

    def get_urls(self):
        urlpatterns = patterns('',
            url('^node/$', self.node_view),
            url('^node/(?P<node_pk>[^/]+)/$', self.node_view),
            url('^node/(?P<node_pk>[^/]+)/available-children-recursive/$', self.shelf_view),
            url('^node/(?P<node_pk>[^/]+)/edit/$', self.node_edit_view),
            url('^node/(?P<node_pk>[^/]+)/templates/$', self.node_templates_view),
            url('^contents/(?P<app_label>[A-z_][\w_]*)/(?P<object_name>[A-z_][\w_]*)/(?P<object_pk>[^/]+)/$', self.content_view),
        )
        return urlpatterns

    def authorize(self, request):
        if not request.user.is_authenticated():
            raise PermissionDenied

    @property
    def urls(self):
        return self.get_urls()

    def reverse(self, *args, **kwargs):
        """
        We tried to use namespaced URLs per site just like ModelAdmins,
        however, as we refer to the views by their function objects, we can't
        use namespaces because there is a bug in Django:

        https://code.djangoproject.com/ticket/17914

        We should use named URLs instead of function references, but we
        couldn't get that working.
        """
        return reverse(*args, **kwargs)

    def get_node_view(self):
        return NodeView.as_view(site=self)

    def get_content_view(self):
        return ContentView.as_view(site=self)

    def get_shelf_view(self):
        return ShelfView.as_view(site=self)

    def get_node_edit_view(self):
        return NodeEditView.as_view(site=self)

    def get_node_templates_view(self):
        return NodeTemplatesView.as_view(site=self)