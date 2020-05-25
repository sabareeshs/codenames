from django.conf.urls import url
from gameplay import views

urlpatterns = [
	url(r'^$', views.index, name='gameplay_index'),
	url(r'^create_board/$', views.create_board, name='create_board'),
	url(r'^(?P<board_id>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/delete/$', views.delete, name='delete'),
	url(r'^(?P<board_id>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/num_clues/$', views.num_clues, name='num_clues'),
	url(r'^(?P<board_id>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/(?P<player>[\_a-z]+)/$', views.board, name='board'),
	url(r'^(?P<board_id>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/(?P<player>[\_a-z]+)/end_turn/$', views.end_turn, name='end_turn'),
	url(r'^(?P<board_id>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/card/(?P<word>[\sa-z\-]+)/(?P<player>[\_a-z]+)/$', views.card_click, name='card_click'),
]
