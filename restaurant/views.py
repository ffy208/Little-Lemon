# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.shortcuts import get_object_or_404




# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views


def menu(request):
    menu_data = Menu.objects.all().order_by('name')  # 获取所有菜单项
    main_data = {"menu": menu_data}
    return render(request, "menu.html", main_data)  # 渲染 `menu.html`


def display_menu_item(request, pk=None):
    if pk:
        menu_item = get_object_or_404(Menu, pk=pk)
    else:
        menu_item = None
    return render(request, "menu_item.html", {"menu_item": menu_item})
