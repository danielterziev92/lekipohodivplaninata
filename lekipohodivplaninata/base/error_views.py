from django.shortcuts import render


def bad_request_view(request, exception):
    return render(request, "errors/400.html", {})


def permission_denied_view(request, exception):
    return render(request, 'errors/403.html', {})


def page_not_fount_view(request, exception):
    return render(request, 'errors/404.html', {})


def server_error_view(request, exception):
    return render(request, 'errors/500.html', {})
