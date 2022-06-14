from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "products/products_list.html"


class AboutPageView(TemplateView):
    template_name = "about.html"
