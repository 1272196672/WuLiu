from django.urls import path
from . import views, m_views, s_views


urlpatterns = [
    # 游客
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login_control', views.login_control, name='login_control'),
    path('sign', views.sign, name='sign'),
    path('sign_control', views.sign_control, name='sign_control'),
    path('coldchain', views.coldchain, name='coldchain'),
    path('predict', views.predict, name='predict'),
    # 管理员
    path('backstage/manager_index', m_views.manager_index, name='manager_index'),
    path('backstage/manager/m_history', m_views.m_history, name='m_history'),
    path('backstage/manager/m_monitor', m_views.m_monitor, name='m_monitor'),
    path('backstage/manager/m_warning', m_views.m_warning, name='m_warning'),
    path('backstage/manager/m_warning_history', m_views.m_warning_history, name='m_warning_history'),
    path('backstage/manager/m_analyze_car', m_views.m_analyze_car, name='m_analyze_car'),
    path('backstage/manager/m_create_order', m_views.m_create_order, name='m_create_order'),
    path('backstage/manager/m_create_order_op', m_views.m_create_order_op, name='m_create_order_op'),
    path('backstage/manager/m_goods', m_views.m_goods, name='m_goods'),
    path('backstage/manager/m_goods_modify/<str:id>', m_views.m_goods_modify, name='m_goods_modify'),
    path('backstage/manager/m_goods_modify_op', m_views.m_goods_modify_op, name='m_goods_modify_op'),
    path('backstage/manager/m_goods_del/<str:id>', m_views.m_goods_del, name='m_goods_del'),
    path('backstage/manager/m_goods_add', m_views.m_goods_add, name='m_goods_add'),
    path('backstage/manager/m_goods_add_op', m_views.m_goods_add_op, name='m_goods_add_op'),
    path('backstage/manager/m_storehouse', m_views.m_storehouse, name='m_storehouse'),
    path('backstage/manager/m_map/<str:location>', m_views.m_map, name='m_map'),
    # 员工
    path('backstage/staff_index', s_views.staff_index, name='staff_index'),
    path('backstage/staff/s_order_now', s_views.s_order_now, name='s_order_now'),
    path('backstage/staff/s_order_history', s_views.s_order_history, name='s_order_history'),
    path('backstage/staff/s_map/<str:location>', m_views.m_map, name='s_map'),
]
