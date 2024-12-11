from django.shortcuts import render, get_object_or_404, reverse
from .models import Car, Order, Service
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import OrderReviewForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic import DetailView


def index(request):
    num_cars = Car.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders_completed = Order.objects.filter(status__exact='d').count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_cars': num_cars,
        'num_orders_completed': num_orders_completed,
        'num_services': num_services,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def cars(request):
    paginator = Paginator(Car.objects.all(), 8)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    context = {
        'cars': cars
    }
    return render(request, 'cars.html', context=context)


def car(request, car_id):
    single_car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': single_car})


class OrderListView(generic.ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'order_list'
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.all().order_by('-date')


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'order_detail.html'
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)


def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Car.objects.filter(
        Q(client__icontains=query) | Q(license_plate__icontains=query) | Q(vin_code__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})


class LoanedCar(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_cars.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).order_by('date')


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile Updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)

class OrderServicesByUserListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'user_orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).order_by('date')


class OrderByUserDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'user_order.html'