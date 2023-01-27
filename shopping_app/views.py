from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from shopping_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import Prodcut,Recharge,Profile,Booking,Kyc,Wallet,CouponCode,Withdraw
from django.db.models import Q
import random,math
import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage

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
    user = Profile.objects.get(user=request.user)
    total_amount = 0
    total_recharge = 0
    abb = 0
    recharge = Recharge.objects.filter(user=user,recharge_request="Accept")
    totalpurchase = Booking.objects.filter(user=user)
    
    if totalpurchase:
        
        for pur in totalpurchase:
            abb = pur.total_purchase
            # print("ourrrrrrrrr",pur.total_purchase)
    if recharge:
        for p in recharge:
            total_recharge = p.total_cost
    c =0
    c = total_recharge - abb  
    
    
    user2 = Profile.objects.get(user=request.user)
    withdraw = Withdraw.objects.filter(user=user2,withdraw_request="Accept")
    balance_wallet = Booking.objects.filter(user=user2)
    user_gift = CouponCode.objects.filter(user=user2,coupen_request="Accept")
    
    
    total_wallet = sum(wallet.amount for wallet in withdraw)
    
   
    daily_commission = sum(booking.daily_wise_commission for booking in balance_wallet)
    total_gift= sum(coupon.gift_amt for coupon in user_gift)   
    total_balance_wallet = (daily_commission+total_gift) - total_wallet
    
        
        # wallet = Wallet.objects.create()
    
    context = {
    'total_amount':total_amount,
    'commission':daily_commission,
    'total_recharge':total_recharge,
    'c':c,
    'total_balance_wallet':total_balance_wallet
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
            user=Profile.objects.get(user=request.user)
            
            recharge = Recharge.objects.create(user=user,upi_id=upi_id,amount=amount,utr=utr_no)

            recharge.save()
            messages.success(request,"Recharge Request Sent Successfully")
            return redirect('recharge')
            

        except:
            messages.error(request,"Something is Wrong Try Again !!")
            return redirect('recharge')
        

    return render(request,'Recharge/recharge.html')    

def recharge_history(request):
    user = Profile.objects.get(user=request.user)
    recharge = Recharge.objects.filter(user=user)
    return render(request,'transaction/recharge_history.html',{'recharge':recharge})


def booking(request):
    user = Profile.objects.get(user=request.user)
    
    abb = 0

    total_amount = 0
    recharge = Recharge.objects.filter(user=user,recharge_request="Accept")
    totalpurchase = Booking.objects.filter(user=user)
    # bookingg = Booking.objects.filter(user=user)
    product_id = request.GET.get('prod_id')
    product_price = int(request.GET.get('price'))
    
    rem = 0
    product = Prodcut.objects.get(id=product_id)
    if recharge:
        for p in recharge:
            rem = p.total_cost
    
   
    # if rem>=product_price:
    #     Booking(user=user,product=product).save()

    if totalpurchase:
        for pur in totalpurchase:
            abb = pur.total_purchase
               
    c =0
    c = (rem - abb)
   

    if c != "" :
        if c>=product_price:
            Booking(user=user,product=product).save()
            messages.success(request,"Your Product is Purchased Successfully")
            return redirect('myorder')
            # if Booking.objects.filter(user=user, product=product).exists():
            #     messages.error(request,"Your Product is already Purchased")
            #     return redirect('product')
            # else:      
        else:
            messages.error(request,"Insufficient Balance ")
            return redirect('product')
        
    elif rem>=product_price:
        Booking(user=user,product=product).save()
        messages.success(request,"Your Product is Purchased Successfully")
        return redirect('myorder')

    else:
        messages.error(request,"Insufuccient Balance")
        return redirect('product')
    



            # if p.total_cost>=product_price:
            #     # p.total_cost = p.total_cost-product_price
            #     # p.save()
                
            # remaining_amount = p.total_cost - product_price
                
                    
        #         if p.remaining_amount>=product_price:
        #             remaining_amount = p.remaining_amount - product_price
        #             p.remaining_amount = remaining_amount
        #             p.save()
        #         else:
        #             messages.error(request,"Insufficient Balance")
        #             return redirect('product')
        #     else:
        #         rem = p.total_cost-product_price
        #         print("ssssssssssssssssssssssssssss",rem)
        #         p.remaining_amount = rem
        #         # p.remaing_amt
        #         p.save()
        # else:
        #     messages.error(request,"Insufficient Balance")
        #     return redirect('product')
    return redirect('product')

        

        #     total_amount += p.amount
        # if total_amount>=product.price:
            
            # total_cost = int(p.total_cost - product_price)
            # print("tttttttttttttt",total_cost)
            # p.total_cost = total_cost
            # p.save()
        #     Booking(user=user,product=product).save()
        #     messages.success(request,"Your Product is Successfully Purchased !!!")
        #     return redirect('myorder')
        # else:
        #     messages.error(request,"Insufficient Balance")
        #     return redirect('product')
    # else:

    #     return redirect('product')


    


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
    kyc = Kyc.objects.filter(user=user)   
    return render(request,'kyc/kyc.html',{'kyc':kyc})



def commision(request):
    user = Profile.objects.get(user=request.user)
    daily_commission = Booking.objects.filter(user=user)
    return render(request,'commission/commission.html',{'daily_commission':daily_commission})


def admin_orders(request):
    booking = Booking.objects.all()
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        commission_amt = request.POST.get('commission_amt')       
        wallet=Booking.objects.get(id=booking_id)        
        wallet.daily_wise_commission= commission_amt
        wallet.save()
        return redirect('adminorder')
    
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
   
    wallet=Withdraw.objects.all()
    
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


def admin_all_users(request):
    profile = Profile.objects.all()
    paginator = Paginator(profile, 1)
    page = request.GET.get('page')
    profiles = paginator.get_page(page)
    
    return render(request,'admin_panel/user/all_users.html',{'profile':profile,'profiles':profiles})
    
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
    if request.method == "POST":
        id = request.POST.get('gift_id')
        gift_amt = request.POST.get('gift_amt')
        coupon_id = CouponCode.objects.get(id=id)
        coupon_id.gift_amt = gift_amt
        coupon_id.save()
    
    return render(request,'admin_panel/gift_request.html',{'coupon':coupon})


def gift_accept(request,id):
    
    gift_accept=CouponCode.objects.get(id=id)
    gift_accept.coupen_request= "Accept"
    gift_accept.save()
    return redirect('gift_request')

def gift_reject(request,id):
    
    gift_accept=CouponCode.objects.get(id=id)
    gift_accept.coupen_request= "Reject"
    gift_accept.save()
    return redirect('gift_request')

def withdraw(request):
    
    user = Profile.objects.get(user=request.user)
    if request.method == "POST":
        
        amount = int(request.POST.get('amount'))

        balance_wallet = Booking.objects.filter(user=user)
        daily_commission = sum(booking.daily_wise_commission for booking in balance_wallet)
        user_gift = CouponCode.objects.filter(user=user,coupen_request="Accept")
        total_gift= sum(coupon.gift_amt for coupon in user_gift)   
        withdraw = Withdraw.objects.filter(user=user,withdraw_request="Accept")
        total_wallet = sum(wallet.amount for wallet in withdraw)
        
        total_balance_wallet = daily_commission+total_gift - total_wallet  
        print("total balance wallent", total_balance_wallet)     
    
        
        
        
        if amount <= total_balance_wallet:
            withdraw = Withdraw.objects.create(user=user,amount=amount)
            withdraw.save()
            messages.success(request,"Withdraw Request Sent")
            return redirect('wallet')
        else:
            messages.error(request,"Insufficient Balance")
            return redirect('wallet')

        
    return redirect('wallet')




def withdraw_accept(request,id):
    wallet=Withdraw.objects.get(id=id)
    wallet.withdraw_request= "Accept"
    wallet.save()
    return redirect('walletrequest')

def withdraw_reject(request,id):
    wallet=Withdraw.objects.get(id=id)
    wallet.withdraw_request= "Reject"
    wallet.save()
    return redirect('walletrequest')


def withdraw_detail(request):
    user =Profile.objects.get(user=request.user)
    withdraw =Withdraw.objects.filter(user=user)
    return render(request,'withdraw/withdraw_detail.html',{'withdraw':withdraw})

def gift(request):
    user = Profile.objects.get(user=request.user)
    user_gift= CouponCode.objects.filter(user=user)

    return render(request,'userGift/gift_detail.html',{'user_gift':user_gift})


def withdraw_transaction(request):
    user = Profile.objects.get(user=request.user)
    withdraw = Withdraw.objects.filter(user=user)
    return render(request,'transaction/withdraw_transaction.html',{'withdraw':withdraw})

