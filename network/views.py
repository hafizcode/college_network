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
from .models import GroupMessage
from .forms import GroupMessageForm


# Home page (redirect to dashboard if already logged in)
def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
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
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'network/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'network/profile.html', {'user_obj': request.user})

@login_required
def group_chat(request):
    if request.method == 'POST':
        form = GroupMessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect('group_chat')
    else:
        form = GroupMessageForm()
    messages = GroupMessage.objects.order_by('timestamp')
    return render(request, 'network/group_chat.html', {'form': form, 'messages': messages})

@login_required
def group_chat_fetch(request):
    messages = GroupMessage.objects.order_by('timestamp')
    data = []
    for msg in messages:
        data.append({
            'sender': msg.sender.username,
            'content': msg.content,
            'file_url': msg.file.url if msg.file else '',
            'file_name': msg.file.name.split('/')[-1] if msg.file else '',
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M')
        })
    return JsonResponse({'messages': data})

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