from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import RegisterForm, FileUploadForm, ProfileForm,ChangePasswordForm
from .models import UserFile

from django.http import FileResponse
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid username or password'
                }
            )

    return render(
        request,
        'accounts/login.html'
    )


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('dashboard')

    else:

        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )
@login_required
def dashboard(request):

    search = request.GET.get('search', '').strip()
    sort = request.GET.get('sort', 'newest')

    files = UserFile.objects.filter(
        user=request.user
    )

    if search:
        files = files.filter(
            file__icontains=search
        )

    if sort == 'oldest':
        files = files.order_by('uploaded_at')

    elif sort == 'name_az':
        files = files.order_by('file')

    elif sort == 'name_za':
        files = files.order_by('-file')

    else:
        files = files.order_by('-uploaded_at')

    return render(
        request,
        'accounts/dashboard.html',
        {
            'files': files,
            'search': search,
            'sort': sort,
            'file_count': files.count(),
        }
    )

def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def upload_file(request):

    if request.method == 'POST':

        form = FileUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            UserFile.objects.create(
                user=request.user,
                file=form.cleaned_data['file']
            )

            return redirect('dashboard')

    else:

        form = FileUploadForm()

    return render(
        request,
        'accounts/upload.html',
        {
            'form': form
        }
    )


@login_required
def delete_file(request, file_id):

    user_file = get_object_or_404(
        UserFile,
        id=file_id,
        user=request.user
    )

    if request.method == 'POST':

        user_file.file.delete(save=False)
        user_file.delete()

    return redirect('dashboard')
@login_required
def secure_file(request, file_id):

    user_file = get_object_or_404(
        UserFile,
        id=file_id,
        user=request.user
    )

    return FileResponse(
        user_file.file.open('rb'),
        as_attachment=False,
        filename=user_file.file.name.split('/')[-1]
    )
@login_required
def toggle_favorite(request, file_id):

    user_file = get_object_or_404(
        UserFile,
        id=file_id,
        user=request.user
    )

    if request.method == 'POST':

        user_file.is_favorite = not user_file.is_favorite
        user_file.save(update_fields=['is_favorite'])

    return redirect('dashboard')
@login_required
def profile_view(request):

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        'accounts/profile.html',
        {
            'form': form
        }
    )
@login_required
def change_password(request):

    if request.method == 'POST':

        form = ChangePasswordForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('profile')

    else:

        form = ChangePasswordForm(request.user)

    return render(
        request,
        'accounts/change_password.html',
        {
            'form': form
        }
    )