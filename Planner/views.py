from django.shortcuts import render



def main(request):
    return render(request, 'base.html')


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)