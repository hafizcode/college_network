from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .forms import RegisterForm, MessageForm, FileTransferForm
from .models import Message, FileTransfer

# Home page (redirect to dashboard if already logged in)
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'network/home.html')

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'network/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'network/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard view with message and file handling
@login_required
def dashboard(request):
    # Get received messages and files
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    received_files = FileTransfer.objects.filter(receiver=request.user).order_by('-timestamp')

    # Default form instances
    msg_form = MessageForm(user=request.user)
    file_form = FileTransferForm(user=request.user)

    # Handle POST requests for message or file sending
    if request.method == 'POST':
        if 'send_message' in request.POST:
            msg_form = MessageForm(request.POST, user=request.user)
            if msg_form.is_valid():
                msg = msg_form.save(commit=False)
                msg.sender = request.user
                msg.save()
                return redirect('dashboard')

        elif 'send_file' in request.POST:
            file_form = FileTransferForm(request.POST, request.FILES, user=request.user)
            if file_form.is_valid():
                file_instance = file_form.save(commit=False)
                file_instance.sender = request.user
                file_instance.save()
                return redirect('dashboard')

    context = {
        'msg_form': msg_form,
        'file_form': file_form,
        'messages': received_messages,
        'files': received_files,
    }
    return render(request, 'network/dashboard.html', context)

# AJAX view to fetch updates for real-time message/file updates
@login_required
def fetch_updates(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    files = FileTransfer.objects.filter(receiver=request.user).order_by('-timestamp')

    data = {
        'messages': [
            {
                'sender': msg.sender.username,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M')
            } for msg in messages
        ],
        'files': [
            {
                'sender': file.sender.username,
                'filename': file.file.name.split('/')[-1],
                'url': file.file.url,
                'timestamp': file.timestamp.strftime('%Y-%m-%d %H:%M')
            } for file in files
        ]
    }
    return JsonResponse(data)

@staff_member_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'network/user_list.html', {'users': users})

@staff_member_required
def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        is_staff = 'is_staff' in request.POST
        is_active = 'is_active' in request.POST
        user.username = username
        user.is_staff = is_staff
        user.is_active = is_active
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('user_list')
    return render(request, 'network/user_edit.html', {'user_obj': user})

@staff_member_required
def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('user_list')
    return render(request, 'network/user_delete_confirm.html', {'user_obj': user})