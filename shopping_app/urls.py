

from django.urls import path
from django.contrib.auth import views as auth_views
from shopping_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path("",views.signin,name="signin"),
    path('logout/',auth_views.LogoutView.as_view(next_page='signin'),name="logout"),
    path("signup/",views.signup,name="signup"),
    path("otp/",views.otp,name="otp"),
    path("dashboard",views.home,name="home"),
    path("prducts/",views.product,name="product"),
    path("prducts/detail/<int:id>",views.product_detail,name="product_detail"),
    path("wallet/",views.wallet,name="wallet"),
    path("profile/",views.profile,name="profile"),



    # -------------------Recharge Url -----------------------
    path("recharge/",views.recharge,name="recharge"),
    path("recharge/history",views.recharge_history,name="recharge_history"),


    # -----------------------Withdraw Url----------------------------
    path("withdraw/transaction",views.withdraw_transaction,name="withdraw_transaction"),


    # --------------------------- Orders Url ---------------------

    path("orders",views.myorder,name="myorder"),




    # ------------------------ Booking Url -------------------
    path("booking/",views.booking,name="booking"),
    

    # ------------------------ Kyc Url -------------------
    path("Kyc/",views.kyc,name="kyc"),


    # ------------------------ Commission Url -------------------
    path("commision/",views.commision,name="commision"),
    

    
    # ------------------------ Admin Url -------------------
    # path("admin/login",views.admin_login,name="admin_login"),
    path('admin_booking',views.admin_orders,name="adminorder"),
    path('admin_kyc',views.admin_kyc,name="admin_kyc"),
    path('admin_recharge',views.admin_recharge,name="admin_recharge"),
    path('recharge_status/<int:id>',views.recharge_status,name="recharge_status"),
    path('recharge_rejected/<int:id>',views.recharge_rejected,name="recharge_rejected"),
    path('walletRequest',views.walletrequest,name="walletrequest"),
    path('walletreject/<int:id>',views.walletreject,name="walletreject"),
    # path('dailywise_commission/<int:id>',views.dailywise_commission,name="dailywise_commission"),
    

    # ---------------------------------- Team ---------------------------- 

    path('team',views.team_list,name="team"),



    # -------------------------- contact Us --------------------
    path('contact',views.contact,name="contact"),
    path('guide',views.guide,name="guide"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('coupon',views.coupon,name="coupon"),
    path('gift_request',views.gift_request,name="gift_request"),
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
