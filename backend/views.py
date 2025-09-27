from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('product_list')  # logged-in → products
    return redirect('login')             # not logged-in → login page
