import views

routes = (
	('index', 'GET', r'/', views.rooms),
	('ws', 'GET', r'/ws/{room}', views.WebSocket),
	('create_room', 'GET', r'/create_room/', views.create_room),
	('chatroom', 'GET', r'/room/{room}', views.index),

)
