from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.views import View
import omise.errors
from . models import *
from . forms import RegistrationForm, ProfileSettingForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import omise
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@login_required
def index(request):
    item = Item.objects.all()
    user = User.objects.get(username=request.user)  
    total_item = 0
    total_wishlist = 0
    wishlist = []
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=user))
        total_wishlist = len(Wishlist.objects.filter(user=user))
        wishlist = list(Wishlist.objects.filter(user=user).values_list('item_id', flat=True))

    return render(request, "app/index.html", locals())


def index_api(request):
    if  request.user.is_authenticated:
        user = request.user
        item = list(Item.objects.values())
        total_item = Cart.objects.filter(user=user).count()
        total_wishlist = Wishlist.objects.filter(user=user).count()
        wishlist = list(Wishlist.objects.filter(user=user).values_list('item_id', flat=True))
        return JsonResponse({
            'item': item,
            'total_item': total_item,
            'total_wishlist': total_wishlist,
            'wishlist': wishlist
        }, safe=False)
    else:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'app/register.html', locals())
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ลงทะเบียนเข้าใช้งานสำเร็จ! ตอนนี้คุณสามารถเข้าสู่ระบบเพื่อเข้าใช้งานได้")
        else:
            messages.error(request, "ข้อมูลไม่ถูกต้อง! กรุณากรอกข้อมูลอีกครั้ง")
        return render(request, 'app/register.html', locals())


@login_required
def profile(request):
    customer = Customer.objects.filter(user=request.user)
    total_item = 0
    total_wishlist = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        total_wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/profile.html', locals())


@method_decorator(login_required, name='dispatch')
class ProfileSettingView(View):
    def get(self, request):
        form = ProfileSettingForm()
        total_item = 0
        total_wishlist = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            total_wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile_setting.html', locals())
    
    def post(self, request):
        form = ProfileSettingForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            zipcode = form.cleaned_data['zipcode']

            customer = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, zipcode=zipcode)
            customer.save()
            messages.success(request, "โปรไฟล์ได้รับการบันทึกแล้ว")
        else:
            messages.error(request, "การบันทึกโปรไฟล์ไม่สำเร็จ!")
        return render(request, 'app/profile_setting.html', locals())
    

@method_decorator(login_required, name='dispatch')
class UpdateProfileView(View):
    def get(self, request, pk):
        customer = Customer.objects.get(pk=pk) 
        form = ProfileSettingForm(instance=customer)
        total_item = 0
        total_wishlist = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            total_wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/update_profile.html', locals())

    def post(self, request, pk):
        form = ProfileSettingForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(pk=pk)
            customer.name = form.cleaned_data['name']
            customer.locality = form.cleaned_data['locality']
            customer.city = form.cleaned_data['city']
            customer.mobile = form.cleaned_data['mobile']
            customer.zipcode = form.cleaned_data['zipcode']

            customer.save()
            messages.success(request, "บันทึกการแก้ไขแล้ว!")

        else:
            messages.error(request, "บันทึกการแก้ไขไม่สำเร็จ กรุณากรอกข้อมูลให้ถูกต้อง!")
        return redirect('profile')

def delete_address(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('profile')
 

@login_required
def about_us(request):
    total_item = 0
    total_wishlist = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        total_wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/about_us.html', locals())


@login_required
def contact(request):
    total_item = 0
    total_wishlist = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        total_wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/contact.html', locals())


@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        item = Item.objects.filter(category=val)
        name = Item.objects.filter(category=val).values('name')
        total_item = 0
        total_wishlist = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            total_wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/category.html', locals())


@method_decorator(login_required, name='dispatch')
class CategoryNameView(View):
    def get(self, request, val):
        item = Item.objects.filter(name=val)
        name = Item.objects.filter(category=item[0].category).values('name')
        total_item = 0
        total_wishlist = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            total_wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/category.html', locals())


@method_decorator(login_required, name='dispatch')
class ItemDetailsView(View):
    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        colors = item.get_colors()
        sizes = item.get_sizes()
        wishlist = Wishlist.objects.filter(Q(item=item) & Q(user=request.user))
        total_item = 0
        total_wishlist = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            total_wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/item_details.html', locals())


@login_required
def add_to_cart(request):
    user = request.user
    item_id = request.POST.get('item_id')
    item = Item.objects.get(id=item_id)
    size = request.POST.get('size')
    color = request.POST.get('color')
    
    Cart(user=user, item=item, size=size, color=color).save()
    return redirect('cart/')


@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    total_saving = 0
    for i in cart:
        value = i.quantity * i.item.discounted_price
        saving = (i.quantity * i.item.selling_price) - value

        amount = amount + value
        total_saving = total_saving + saving

    total_amount = amount + 40 
    total_item = 0
    total_wishlist = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        total_wishlist = len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/add_to_cart.html', locals())


@login_required
def increase_item(request):
    if request.method == 'GET':
        item_id = request.GET['item_id']
        c = Cart.objects.get(Q(item=item_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        # getting data
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0
        total_saving = 0
        for i in cart:
            value = i.quantity * i.item.discounted_price
            saving = (i.quantity * i.item.selling_price) - value

            amount = amount + value
            total_saving = total_saving + saving

        total_amount = amount + 40 

        data = {
            "quantity": c.quantity,
            "amount": amount,
            "total_amount": total_amount,
            "total_saving": total_saving
        }
        return JsonResponse(data)
    

@login_required
def decrease_item(request):
    if request.method == "GET":
        item_id = request.GET['item_id']
        c = Cart.objects.get(Q(item=item_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        total_saving = 0
        for i in cart:
            value = i.quantity * i.item.discounted_price
            saving = (i.quantity * i.item.selling_price) - value

            amount = amount + value
            total_saving = total_saving + saving

        total_amount = amount + 40 
        data = {
            "quantity": c.quantity,
            "amount": amount,
            "total_amount": total_amount,
            "total_saving": total_saving

        }
        return JsonResponse(data)


@login_required
def remove_item(request):
    if request.method == "GET":
        item_id = request.GET['item_id']
        c = Cart.objects.get(Q(item=item_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        total_saving = 0
        for i in cart:
            value = i.quantity * i.item.discounted_price
            saving = (i.quantity * i.item.selling_price) - value

            amount = amount + value
            total_saving = total_saving + saving

        total_amount = amount + 40 if cart.exists() else 0
        data = {
            "amount": amount,
            "total_amount": total_amount,
            "total_saving": total_saving

        }
        return JsonResponse(data)


@login_required
def payment_success(request):
    total_item = 0
    total_wishlist = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        total_wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/payment_success.html", locals())   


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        OMISE_PUBLIC_KEY = settings.OMISE_PUBLIC_KEY

        user = request.user
        address = Customer.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        amount = 0
        total_saving = 0
        for i in cart:
            value = i.quantity * i.item.discounted_price
            saving = (i.quantity * i.item.selling_price) - value
            amount += value
            total_saving = total_saving + saving
        total_amount = amount + 40
        omiseamount = int(total_amount * 100)

        total_item = 0
        total_wishlist = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            total_wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/checkout.html', locals())
    
    def post(self, request):
        omise.api_secret = settings.OMISE_SECRET_KEY
        omise.api_public = settings.OMISE_PUBLIC_KEY
        user = request.user
        customer_id = request.POST.get('customer_id')
        omise_token = request.POST.get("omiseToken")
        total_amount = float(request.POST.get("total_amount"))

        if not customer_id:
            messages.error(request, "กรุณาเลือกที่อยู่จัดส่ง")
            return redirect("checkout")
        
        if not omise_token:
            messages.error(request, "ชำระเงินไม่สำเร็จ")
            return redirect("checkout")
        
        try:
            charge = omise.Charge.create(
                amount = int(total_amount * 100),
                currency = "THB",
                card = omise_token,
                description = "Order payment"
            )
            if charge.status == "successful":
                with transaction.atomic():
                    shipping_address = Customer.objects.get(id=customer_id)
                    cart_items = Cart.objects.filter(user=user)
                    payment = Payment.objects.create(
                        user=user,
                        amount=total_amount,
                        charge_id=charge.id,
                        payment_status=charge.status,
                        paid=True
                    )
                    for i in cart_items:
                        OrderPlaced.objects.create(
                            user=user,
                            customer=shipping_address,
                            item=i.item,
                            quantity=i.quantity,
                            payment=payment,
                            status="Pending"
                        )
                    # clear the cart after successful order
                    cart_items.delete()
                    messages.success(request, "คำสั่งซื้อของคุณได้รับการยืนยันแล้ว!")
                    return redirect("payment_success")
            else:
                messages.error(request, "การชำระเงินล้มเหลว กรุณาลองอีกครั้ง!")
                return redirect("checkout")
        except omise.errors.BaseError as e:
                messages.error(request, f"Payment error: {str(e)}")
                return redirect("checkout")
        

@login_required
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    total_item = 0
    total_wishlist = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        total_wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/orders.html', locals())


class OrderStatusView(View):
    def get(self, request, val):
        order = OrderPlaced.objects.filter(status=val)
        order_placed = OrderPlaced.objects.filter(user=request.user)
        return render(request, 'app/orders_status.html', locals())



@login_required
def add_wishlist(request):
    if request.method == 'GET':
        item_id = request.GET['item_id']
        item = Item.objects.get(id=item_id)
        user = request.user
        Wishlist(user=user, item=item).save()
        data = {
            'message': 'เพิ่มไอเทมไปยังรายการสิ่งที่อยากได้สำเร็จแล้ว!'
        }
        return JsonResponse(data)


@login_required 
def remove_wishlist(request):
    if request.method == 'GET':
        item_id = request.GET['item_id']
        item = Item.objects.get(id=item_id)
        user = request.user
        Wishlist.objects.filter(user=user, item=item).delete()
        data = {
            'message': 'ลบไอเท็มจากรายการสิ่งที่อยากได้แล้ว'
        }
        return JsonResponse(data)
    

@login_required
def show_wishlist(request):
    wishlist_item = Wishlist.objects.filter(user=request.user)
    total_item = 0
    total_wishlist = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        total_wishlist = len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/wishlist.html', locals())


@login_required
def search(request):
    query = request.GET['search']
    total_item = 0
    total_wishlist = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        total_wishlist = len(Wishlist.objects.filter(user=request.user))

    item = Item.objects.filter(Q(name__icontains=query))
    return render(request, 'app/search.html', locals())