from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from shopping_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import Prodcut,Recharge,Profile,Booking,Kyc,Wallet,CouponCode
from django.db.models import Q
import random,math
import requests
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="signin")
def home(request):
    return render(request,'homepage/home.html')

@login_required(login_url="signin")
def product(request):
    product = Prodcut.objects.all()
    return render(request,'Products/product.html',{'product':product})


@login_required(login_url="signin")
def product_detail(request,id):
    product = Prodcut.objects.get(id=id)
    # user = Profile.objects.get(user=request.user)
    # booking = Booking.objects.get(product=product)
    # if user.objects.filter(username = username).exists():
    #             messages.warning(request, "Username is already Taken")
    #             return redirect('signup')
    return render(request,'Products/product_detail.html',{'product':product})


@login_required(login_url="signin")
def wallet(request):
    
    
        # print("sssssssss",daily_commission)
    total_amount = 0
    recharge = Recharge.objects.all()
    if recharge:
        for p in recharge:
            if p.recharge_request == "Accept":

                total_amount += p.amount
    user2 = Profile.objects.get(user=request.user)
   
    
    balance_wallet = Booking.objects.filter(user=user2)
    daily_commission = sum(booking.daily_wise_commission for booking in balance_wallet)
    
   
    # wll = Wallet.objects.get(user=user2)
        
    if request.method == "POST":
        amount = int(request.POST.get('amount'))
        
        
        if amount <= 1000 | amount > daily_commission:
            messages.warning(request,"Insufficient Balance")
            return redirect('wallet')
        
        # wallet = Wallet.objects.create()
    
    context = {
    'total_amount':total_amount,
    'commission':daily_commission
    }
        
    return render(request,'Wallet/wallet.html',context)
   
    # try:      
    #     recharge = Recharge.objects.all()
    #     if recharge:
    #         for p in recharge:
    #             if p.recharge_request == "Accept":

    #                 total_amount += p.amount
    #     user2 = Profile.objects.get(user=request.user)
    #     balance_wallet = Booking.objects.filter(user=user2)
    #     daily_commission = 0
    #     if balance_wallet:
    #         for wallet in balance_wallet:
    #             daily_commission += wallet.daily_wise_commission
        
    #     if request.method == "POST":
    #         amount = request.POST.get('amount')
    #         print("ammmmmmmmmmmmm",amount)
           
    #         if amount <= 1000 :
    #             messages.warning(request,"Insufficient Balance")
    #             print("inssucfff")
    #             return redirect('wallet')

    #         else:
    #             print("errorrr")
       
    #     context = {
    #     'total_amount':total_amount,
    #     'commission':daily_commission
    #     }
        
    #     return render(request,'Wallet/wallet.html',context)
    # except:
    #     pass
    
    #             # print("total",total_amount)
   
    # return render(request,'Wallet/wallet.html')

        
def signup(request):

    # if request.method == "POST":
       
            #         if otp == otp_verfication:
                
    #             user = User.objects.create_user(username=username,password=password)
    #             user.profile.mobile = mobile  
    #         # user.save()
    #             messages.success(request,"Registration sucessfully Please Sign In ")
    #             return redirect("signin")      
    #         else:
    #             print("otp is not valid")
   
    
    #     # print("verif",otp_verfication)
    #     otp = ""
    #     for i in range(1,7):
    #         a = random.random()
    #         b = math.floor(a*10)
    #         otp += str(b)
        
    #     print("hello",username,mobile,password,otp,otp_verfication)
        
    #     try:
    #         if User.objects.filter(username = username).exists():
    #             messages.warning(request, "Username is already Taken")
    #             return redirect('signup')
            
    #         if otp == otp_verfication:
                
    #             user = User.objects.create_user(username=username,password=password)
    #             user.profile.mobile = mobile  
    #         # user.save()
    #             messages.success(request,"Registration sucessfully Please Sign In ")
    #             return redirect("signin")      
    #         else:
    #             print("otp is not valid")
   
    
   
    return render(request,'signup/signup.html')

def otp(request):
    referral = request.POST.get("referral")
    username = request.POST.get("username")
    mobile = request.POST.get("mob_no")
    password = request.POST.get("password")
   

    try:
        if User.objects.filter(username = mobile).exists():
            messages.warning(request, "Mobile Number is already Taken")
            return redirect('signup')
        if Profile.objects.filter(referral_id=referral).exists:
            print("helooooooooooooo")

            user = User.objects.create_user(username=mobile,password=password,first_name=username)
            user.profile.mobile = mobile  
            user.profile.refer_by = referral  
            user.save()
        else:
            messages.warning(request, "Referral code no match")
            return redirect('signup')
        if referral == "":
            user = User.objects.create_user(username=mobile,password=password,first_name=username)
            user.profile.mobile = mobile  
            user.profile.refer_by = referral
            user.save()

        

    except:
            pass

    otp = ""
    for i in range(1,7):
        a = random.random()
        b = math.floor(a*10)
        otp += str(b)
    
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    message = "Dear User Your Mobile Verify OTP is." + otp
    numbers = mobile
    payload = f"sender_id=TXTIND&message={message}&route=v3&language=english&numbers={numbers}"
    headers = {
    'authorization': "aiLHjGsN0AKYPUqTFp3lM5weZzct4xhE9VXI2yCDBnoR6gJvrOFE0Hr9UQcWn4vePkmwxfVdGjIb6Aga",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    
    response = requests.request("POST", url, data=payload, headers=headers)

    # if request.method == "POST":
    #     return redirect("signin")
        

    return render(request,'Otp/otp.html')
def signin(request):

    if request.method == "POST":
        print("helloooo",request.POST.get("username"))
        print("helloooo",request.POST.get("password"))
        user=EmailBackEnd.authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        
        if user!=None:
            login(request,user)
            # if user.is_superuser
            return redirect("home")
            # return HttpResponseRedirect('home')
           
           
        else:
            messages.error(request,"Invalid Login Or Password !!")
            return redirect('signin')
    
   
    if request.user.is_authenticated:
        return redirect("home")

    return render(request,'signup/signin.html')


@login_required(login_url="signin")
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,'Profile/profile.html',{'profile':profile})    




# ---------------------------- Recharge ---------------------- 




def recharge(request):
    profile=Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        upi_id = request.POST.get('upi_id')
        amount = int(request.POST.get('amount'))
        utr_no = request.POST.get('utr_no')
        if upi_id == "":
            messages.error(request,"select your Payment Modes")
            return redirect('recharge')
            
        if amount == "":
            messages.error(request,"Choose Your Amount")
            return redirect('recharge')

        

        
            
            
        try:
            
            recharge = Recharge.objects.create(user=profile,upi_id=upi_id,amount=amount,utr=utr_no)

            recharge.save()
            messages.success(request,"Recharge Request Sent Successfully")
            return redirect('recharge')
            

        except:
            messages.error(request,"Something is Wrong Try Again !!")
            return redirect('recharge')
        

    return render(request,'Recharge/recharge.html')    

def recharge_history(request):
    recharge = Recharge.objects.all()
    return render(request,'transaction/recharge_history.html',{'recharge':recharge})

def withdraw_transaction(request):
    recharge = Recharge.objects.all()
    return render(request,'transaction/withdraw_transaction.html',{'recharge':recharge})



def booking(request):
    user = Profile.objects.get(user=request.user)
    product_id = request.GET.get('prod_id')
    print("sssss",product_id)
    product = Prodcut.objects.get(id=product_id)
    Booking(user=user,product=product).save()
    messages.success(request,"Your Product is Successfully Purchased !!!")
    return redirect('myorder')


def myorder(request):
    user = Profile.objects.get(user=request.user)
    booking = Booking.objects.filter(user=user)
    context = {
        'booking':booking
    }
    return render(request,'orders/myorder.html',context)


def kyc(request):
    
    user = Profile.objects.get(user=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        bank_name = request.POST.get("bank_name")
        ac_no = request.POST.get("account_no")
        ifsc_code = request.POST.get("ifsc_code")
        try:
            kyc = Kyc.objects.create(user=user,bank_holder_name=name,bank_name=bank_name,account_number=ac_no,ifsc_code=ifsc_code)
            messages.success(request,f"{user} Kyc is updated")
            kyc.save()
        except:
            messages.error(request,"something is error Try Again !!")
    kyc = Kyc.objects.all()   
    return render(request,'kyc/kyc.html',{'kyc':kyc})



def commision(request):
    return render(request,'commission/commission.html')


def admin_orders(request):
    booking = Booking.objects.all()
    if request.method == "POST":
        commission2 = request.POST.get('commission')
        id = request.POST.get('prod_id')
        
        book = Booking.objects.get(id=id)
        
        book.daily_wise_commission=commission2
       
        book.save()
    return render(request,'admin_panel/order/order.html',{'booking':booking})

def admin_kyc(request):
    kyc = Kyc.objects.all()
    return render(request,'admin_panel/kyc/kyc.html',{'kyc':kyc})

def admin_recharge(request):
    recharge = Recharge.objects.all()
    return render(request,'admin_panel/Recharge/recharge.html',{'recharge':recharge})


def recharge_status(request,id):
    
    recharge=Recharge.objects.get(id=id)
    recharge.recharge_request= "Accept"
    recharge.save()
    return redirect('admin_recharge')



def recharge_rejected(request,id):
    recharge=Recharge.objects.get(id=id)
    recharge.recharge_request= "Reject"
    recharge.save()
    return redirect('admin_recharge')


def walletrequest(request):
    wallet=Wallet.objects.all()
    
    return render(request,'admin_panel/walletRequest/wallet.html',{'wallet':wallet})


def walletreject(request,id):
    wallet=Wallet.objects.get(id=id)
    wallet.wallet_request= "Reject"
    wallet.save()
    return redirect('walletrequest')


# def dailywise_commission(request,id):
#     if request.method == "POST":
#         commission = request.POST.get('commission')
#         booking = Booking.objects.get(id=id)
#         booking.daily_wise_commission=commission
#         booking.save()
#     return redirect('adminorder')



def team_list(request):
    # profile = Profile.objects.filter(referral_id=request.user)
    profile = Profile.objects.filter(refer_by=request.user.profile.referral_id)
    
  
   
    return render(request,'Team/team_list.html',{'profile':profile})

def contact(request):
    return render(request,'contactUs/contact.html')

def guide(request):
    return render(request,'Guide/guide.html')

def aboutus(request):
    return render(request,'Guide/aboutus.html')

def coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        user = Profile.objects.get(user=request.user)
        coupon = CouponCode.objects.create(user=user,coupon_code=coupon_code)
        coupon.save()
        messages.success(request,'Your Gift Code sent Successfully ')
    return redirect('profile')


def gift_request(request):
    coupon = CouponCode.objects.all()
    return render(request,'admin_panel/gift_request.html',{'coupon':coupon})