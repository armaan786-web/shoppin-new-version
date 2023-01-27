

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
    # path('editcommission/<int:id>',views.editcommission,name="editcommission"),
    path('admin_kyc',views.admin_kyc,name="admin_kyc"),
    path('admin_recharge',views.admin_recharge,name="admin_recharge"),
    path('recharge_status/<int:id>',views.recharge_status,name="recharge_status"),
    path('recharge_rejected/<int:id>',views.recharge_rejected,name="recharge_rejected"),
    path('walletRequest',views.walletrequest,name="walletrequest"),
    path('walletreject/<int:id>',views.walletreject,name="walletreject"),
    # path('dailywise_commission/<int:id>',views.dailywise_commission,name="dailywise_commission"),
    path('all/users',views.admin_all_users,name="admin_all_users"),

    # ---------------------------------- Team ---------------------------- 

    path('team',views.team_list,name="team"),



    # -------------------------- contact Us --------------------
    path('contact',views.contact,name="contact"),
    path('guide',views.guide,name="guide"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('coupon',views.coupon,name="coupon"),
    path('gift_request',views.gift_request,name="gift_request"),
    path('gift/accept/<int:id>',views.gift_accept,name="gift_accept"),
    path('gift/reject/<int:id>',views.gift_reject,name="gift_reject"),
    
    # ============================= withdraw =============== 
    path('withdraw',views.withdraw,name="withdraw"),
    path("withdraw/transaction",views.withdraw_transaction,name="withdraw_transaction"),
    path('withdraw/accept/<int:id>',views.withdraw_accept,name="withdraw_accept"),
    path('withdraw/reject/<int:id>',views.withdraw_reject,name="withdraw_reject"),
    

    # ====================================== gift ====================

    path('gift/',views.gift,name="gift"),
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
