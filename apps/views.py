from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, ListView

from apps.forms import RegisterForm
from apps.models import User, Category, Product


class CustomRegisterView(FormView):
    form_class = RegisterForm
    template_name = 'auth/register.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return redirect('login')


class CustomLoginView(TemplateView):
    template_name = 'auth/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return redirect('login')
        else:
            user = authenticate(request, email=user.email, password=request.POST.get('password'))
            if user:
                login(request, user)
                return redirect('product-list')

            else:
                context = {
                    "messages_error": ["Not found account"]
                }
                return render(request, template_name='auth/login.html', context=context)

class ProductListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'trade/product-list.html'

    def get_queryset(self):
        category_slug = self.request.GET.get('category_slug')
        query = super().get_queryset()
        if category_slug:
            query = query.filter(category__slug = category_slug)
        return query

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data