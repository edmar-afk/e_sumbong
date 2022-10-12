from multiprocessing import context
from turtle import update
from django.shortcuts import render, redirect, get_object_or_404, reverse
from pkg_resources import require
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import ComplaintType, TbleComplaint, SystemAdmin
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, auth
# Create your views here.


def register_user(request):
    
    if request.method == "POST":
        first_name = request.POST['full_name']
        last_name = request.POST['mobile']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(last_name=last_name).exists():
                messages.info(request, 'Mobile Number already taken.')
                return redirect('users:user-register')
            
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken.')
                return redirect('users:user-register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                return redirect('users:user-login')
        else:
            messages.info(request, 'Password not match.')
            return redirect('users:user-register')
        
        return redirect('users:user-login')
    
    
    return render(request, 'residents/register.html')



def login_user(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password) 
        if user is not None:
            auth.login(request, user)
            return redirect("users:user-index")
        else:
            messages.info(request, "Invalid USERNAME or PASSWORD")
            return redirect("users:user-login")
    else:    
        return render(request, 'residents/login.html')
                
   


def logoutUser(request):
    auth.logout(request)
    return redirect('users:user-login')



def login_admin(request):
    return render(request, 'officials/login.html')


@login_required(login_url='user-login')
def user_index(request):
    
    pending = TbleComplaint.objects.filter(complaintStatus='Pending' ,complainant=request.user).count()
    process = TbleComplaint.objects.filter(complaintStatus='On-Process' ,complainant=request.user).count()
    solved = TbleComplaint.objects.filter(complaintStatus='Solved' ,complainant=request.user).count()
    rejected = TbleComplaint.objects.filter(complaintStatus='Rejected' ,complainant=request.user).count()
    
    
    context = {
        'pending': pending,
        'process': process,
        'solved': solved,
        'rejected': rejected,
        
    }
    return render(request, 'residents/index.html', context)




@login_required(login_url='user-login')
def file_complaint(request):
    type_complaint = ComplaintType.objects.all().order_by('id')
    status = ComplaintType.objects.all().order_by('id')
    
    if request.method == 'POST':
        
        c_type = request.POST['typecomplaint']
        c_status = request.POST['status']
        c_complainant = request.POST['complainant']
        c_address = request.POST['address']
        c_detail = request.POST['details']
        c_file = request.FILES['file']
        
        if c_file is None:
            messages.warning(request, 'Must upload file')
            return redirect(request.path)
            
        else:
            new_complaint = TbleComplaint(complaintType_id=c_type,complaintStatus=c_status, complainant_id= c_complainant, complaint_addr=c_address, complaint_details=c_detail, complaint_file=c_file)
            new_complaint.save()
        return render(request, 'residents/file-complaint.html', {
        'successful_submit': True})
     
    return render(request, 'residents/file-complaint.html', {
        'complaints': type_complaint,
        'status': status
    })
    

    
@login_required(login_url='user-login')
def complaint_history(request):
    user = User.objects.get(id=request.user.id)
    history = TbleComplaint.objects.filter(complainant=request.user).order_by('id')
    
    pending = TbleComplaint.objects.filter(complaintStatus='Pending')
    process = TbleComplaint.objects.filter(complaintStatus='On-Process')
    solved = TbleComplaint.objects.filter(complaintStatus='Solved')
    rejected = TbleComplaint.objects.filter(complaintStatus='Rejected')
    
    context = {
        'history': history,
        'pending': pending,
        'process': process,
        'solved': solved,
        'rejected': rejected,
    }
    return render(request, 'residents/complaint-history.html', context)


def hist_delete(request, complaint_id):
    TbleComplaint.objects.filter(id=complaint_id).delete()
    return redirect('/complaint-history')


@login_required(login_url='user-login')
def user_profile(request):
    
    return render(request, 'residents/user-profile.html')


@login_required(login_url='user-login')
def user_password(request):
    
    
    return render(request, 'residents/user-password.html')



@login_required(login_url='user-login')
def complaint_type(request):
    type_complaint = ComplaintType.objects.all().order_by('id')
    
    if request.method == 'POST':
        n_type = request.POST['newtype']
    
        new_type = ComplaintType(complaint_type=n_type)
        new_type.save()
        
        
    return render(request, 'officials/complaint-type.html', {
        'complaints': type_complaint
    })


def complainttype_delete(request, complainttype_id):
    ComplaintType.objects.filter(pk=complainttype_id).delete()
    return redirect('/complaint-type')

def complainttype_edit(request, complainttype_id):
    if request.method == 'POST':
        new_type = request.POST.get['updatectype']
        
        new_c = ComplaintType.objects(pk=complainttype_id)
        new_c.complaint_type = new_type
        new_c.save()
    
    return HttpResponseRedirect(reverse('users:complaint-type'))
    



def updatesolved(request, solved_id): 
    
    p_status = request.POST.get('statuspprocess')
    p_remarks = request.POST.get('processremarks')
    
    p_update = TbleComplaint.objects.get(id=solved_id)
    p_update.complaintStatus = p_status
    p_update.complaint_remark = p_remarks
    p_update.save()
    
    print(p_update)
    return HttpResponseRedirect(reverse('users:closed'))


@login_required(login_url='user-login')
def closed(request):
    solved_complaints = TbleComplaint.objects.filter(complaintStatus='Solved')
    status = TbleComplaint.objects.all().order_by('id')
    
    context = {
        'solved_complaints': solved_complaints,
        'status': status,
    }
    
    return render(request, 'officials/closed.html', context)






@login_required(login_url='user-login')
def updatepending(request, pending_id): 
    
    p_status = request.POST.get('statuspending')
    p_remarks = request.POST.get('remarks')
    
    p_update = TbleComplaint.objects.get(id=pending_id)
    p_update.complaintStatus = p_status
    p_update.complaint_remark = p_remarks
    p_update.save()
    
    print(p_update)
    return HttpResponseRedirect(reverse('users:pending'))

@login_required(login_url='user-login')   
def pending(request):
    pending_complaints = TbleComplaint.objects.filter(complaintStatus='Pending')
    status = TbleComplaint.objects.all().order_by('id')
    
    context = {
        'pending_complaints': pending_complaints,
        'status': status,
    }
    
    return render(request, 'officials/pending.html', context)








@login_required(login_url='user-login')
def updateprocess(request, process_id): 
    
    p_status = request.POST.get('statuspprocess')
    p_remarks = request.POST.get('processremarks')
    
    p_update = TbleComplaint.objects.get(id=process_id)
    p_update.complaintStatus = p_status
    p_update.complaint_remark = p_remarks
    p_update.save()
    
    print(p_update)
    return HttpResponseRedirect(reverse('users:processed'))


@login_required(login_url='user-login')
def processed(request):
    process_complaints = TbleComplaint.objects.filter(complaintStatus='On-Process')
    status = TbleComplaint.objects.all().order_by('id')
    
    context = {
        'process_complaints': process_complaints,
        'status': status,
    }
    
    return render(request, 'officials/processed.html', context)










@login_required(login_url='user-login')
def updaterejected(request, rejected_id): 
    
    p_status = request.POST.get('statusrejected')
    p_remarks = request.POST.get('rejectedremarks')
    
    p_update = TbleComplaint.objects.get(id=rejected_id)
    p_update.complaintStatus = p_status
    p_update.complaint_remark = p_remarks
    p_update.save()
    
    print(p_update)
    return HttpResponseRedirect(reverse('users:rejected'))

@login_required(login_url='user-login')
def rejected(request):
    rejected_complaints = TbleComplaint.objects.filter(complaintStatus='Rejected')
    status = TbleComplaint.objects.all().order_by('id')
    
    context = {
        'rejected_complaints': rejected_complaints,
        'status': status,
    }
    
    return render(request, 'officials/rejected.html', context)










@login_required(login_url='user-login')
def manage_users(request):
    users = User.objects.all().order_by('id')
    
    context = {'user': users}
    return render(request, 'officials/manage-users.html', context)




@login_required(login_url='user-login')
def admin_password(request):
    return render(request, 'officials/admin-password.html')

def homepage(request):
    count_complaints = TbleComplaint.objects.all().count()
    context = {'count': count_complaints}
    return render(request, 'index.html', context)

