from django.conf.urls import patterns, url
from store import views

urlpatterns = patterns('',
                       url(r'^$', views.render_category, name='index'),
                       url(r'^category/$', views.render_category, name='index'),
                       url(r'^category/*([0-9]+)/*([0-9]*)/*([0-9]*)/*([0-9]*)$',
                           views.render_category, name='category'),
                       url(r'^product/([0-9]+)', views.product_page, name='product_page'),
                       url(r'^rate_product/$', views.rate_product, name='rate_product'),

                       url(r'^add/([0-9]+)$', views.add_product, name='add_product'),
                       url(r'^show/$', views.show_products, name='show_products'),
                       url(r'^remove/([0-9]+)$', views.remove_product, name='remove_product'),

                       url(r'^delivery$', views.show_delivery_page, name='show_delivery_page'),
                       url(r'^contact$', views.show_contact_page, name='show_contact_page'),

                       url(r'^backcall$', views.receive_backcall_query, name='receive_backcall_query'),

                       url(r'^checkout$', views.checkout_order, name='checkout'),

                       url(r'^clear-cart$', views.clear_cart, name='clear_cart'),
                       url(r'^update-cart$', views.update_cart, name="update-cart"),
                       )
