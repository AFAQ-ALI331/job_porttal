from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login , logout 
from .models import *
from datetime import date
# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_login(request):
    error=""
    if request.method== "POST":
        u= request.POST['uname'];
        p= request.POST['pwd'];
        user = authenticate(username=u,password=p)
        try:
            if  user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}                    
            
    return render(request,'admin_login.html',d)

def admin_home(request):
    if  not request.user.is_authenticated:
        return redirect('admin_login')
    rcount=Recruiter.objects.count()
    scount=StudentUser.objects.count()
    d={'rcount':rcount,'scount':scount}
    return render(request,'admin_home.html',d)


def user_login(request):
    error=""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "Student":
                   login(request,user)
                   error="no"
                else:
                    error="yes"
            except:
                 error="yes"
        else:
            error= "yes"    

    d={'error':error}
    return render(request,'user_login.html',d)


def user_home(request):
    if  not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student =StudentUser.objects.get(user=user)
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']


        student.user.first_name=f
        student.user.last_name=l
        student.mobile=con
        student.gender=gen
        try:
                 student.save()
                 student.user.save()
                 error="no"
        except:

            error="yes"
        try:
            i=request.FILES['image']
            student.image=i
            student.save()
            error="no"
        except:

            pass  
    d={'error':error,'student':student}

    
    return render(request,'user_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')


def user_signup(request):
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        i=request.FILES['image']
        e=request.POST['email']
        p=request.POST['pwd']
        con=request.POST['contact']
        gen=request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p )
            StudentUser.objects.create(user=user, mobile=con,image=i, gender=gen ,type='Student' )
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'user_signup.html',d)



def recruiter_login(request):
    error=""
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "Recruiter" and user1.status!="pending":
                   login(request,user)
                   error="no"

                else:
                    error="not"
            except:
                 error="yes"
        else:
            error= "yes"    

    d={'error':error}

    return render(request,'recruiter_login.html',d)

def recruiter_signup(request):
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        i=request.FILES['image']
        e=request.POST['email']
        p=request.POST['pwd']
        con=request.POST['contact']
        gen=request.POST['gender']
        company=request.POST['company']
        try:
            user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p )
            Recruiter.objects.create(user=user, mobile=con,image=i, gender=gen ,type='Recruiter',company=company, status="pending" )
            error="no"
        except:
            error="yes"
    d={'error':error}

    return render(request,'recruiter_signup.html',d)


def recruiter_home(request):
    if  not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter= Recruiter.objects.get(user=user)
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']


        recruiter.user.first_name=f
        recruiter.user.last_name=l
        recruiter.mobile=con
        recruiter.gender=gen
        try:
                 recruiter.save()
                 recruiter.user.save()
                 error="no"
        except:

            error="yes"
        try:
            i=request.FILES['image']
            recruiter.image=i
            recruiter.save()
            error="no"
        except:

            pass  
    d={'error':error,'recruiter':recruiter}

    return render(request,'recruiter_home.html',d)

def recruiter_pending(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data = Recruiter.objects.filter(status='pending')
    d = {'data':data} 
    return render(request,'recruiter_pending.html',d)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data = Recruiter.objects.filter(status='Accept')
    d = {'data':data} 
    return render(request,'recruiter_accepted.html',d)



def recruiter_rejected(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data = Recruiter.objects.filter(status='Reject')
    d = {'data':data} 
    return render(request,'recruiter_rejected.html',d)

def recruiters_all(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data = Recruiter.objects.all()
    d = {'data':data} 
    return render(request,'recruiters_all.html',d)


def change_status(request,pid):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    error=""
    recruiter = Recruiter.objects.get(id=pid)
    if request.method=="POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"    
    d = {'recruiter':recruiter,'error':error} 
    return render(request,'change_status.html',d)

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    recruiter = User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiters_all')



def change_passwordadmin(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n)
               u.save()
               error="no"
            else:
               error="not"
        except:
            error="yes"    
    d = {'error':error} 
    
    return render(request,'change_passwordadmin.html',d)

def change_passworduser(request):
    if not request.user.is_authenticated:
       return redirect('user_login')
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n)
               u.save()
               error="no"
            else:
               error="not"
        except:
            error="yes"    
    d = {'error':error} 
    
    return render(request,'change_passworduser.html',d)


def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
       return redirect('recruiter_login')
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n)
               u.save()
               error="no"
            else:
               error="not"
        except:
            error="yes"    
    d = {'error':error} 
    
    return render(request,'change_passwordrecruiter.html',d)


def view_users(request):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    data = StudentUser.objects.all()
    d = {'data':data} 
    return render(request,'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
       return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def job_add(request):
    if not request.user.is_authenticated:
       return redirect('recruiter_login')
    error=""
    if request.method== "POST":
        jt=request.POST['jobtitle']
        sd=request.POST['startdate']
        ed=request.POST['enddate']
        sal=request.POST['salary']
        l=request.FILES['logo']
        exp=request.POST['experience']
        loc=request.POST['location']
        skills=request.POST['skills']
        des=request.POST['description']
        user=request.user
        recruiter= Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,start_date=sd,end_date=ed,image=l,salary=sal,experience=exp,
                               title=jt,description=des,skills=skills,location=loc,creation_date=date.today())
            error= "no"
        except:    
            error= "yes"           
    d={'error':error}        
    return render(request,'job_add.html',d)

def job_list(request):
    if not request.user.is_authenticated:
       return redirect('recruiter_login')
    user=request.user
    recruiter= Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    
    d={'job':job}
    return render(request,'job_list.html',d)
    
def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    
    error=""
    job = Job.objects.get(id=pid)
    if request.method== "POST":
        jt=request.POST['jobtitle']
        sd=request.POST['startdate']
        ed=request.POST['enddate']
        sal=request.POST['salary']
        exp=request.POST['experience']
        loc=request.POST['location']
        skills=request.POST['skills']
        des=request.POST['description']
        
        job.title=jt
        job.salary=sal
        job.experience=exp
        job.location=loc
        job.skills=skills
        job.description=des
        try:
            job.save()
            error= "no"
        except:    
            error= "yes"
        if sd:
            try:
                job.start_date=sd
                job.save()
            except:
                    pass
        else:
            pass
        if ed:
            try:
                job.end_date=ed
                job.save()   
            except:
                    pass
        else:
            pass                
    d={'error':error,'job':job}
    return render(request,'edit_jobdetail.html',d)

def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login') 
    error=""
    job=Job.objects.get(id=pid)
    if request.method=="POST":
        cl=request.FILES['logo']
        job.image=cl
        try:
            job.save()
            error="no"
        except:
            error="yes"
    d={'error':error,'job':job}        

    return render(request,'change_companylogo.html',d)


def jobs_latest(request):
    data = Job.objects.all().order_by('-start_date')
    d={'data':data}
    return render(request,'jobs_latest.html',d) 


def user_latestjobs(request):
    job = Job.objects.all().order_by('-start_date')
    user=request.user
    student = StudentUser.objects.get(user=user)
    data1= Apply.objects.filter(student=student)
    l1=[]
    for i in data1:
        l1.append(i.job.id)
    d={'job':job,'l1':l1}
    return render(request,'user_latestjobs.html',d) 



def job_detaile(request,pid):
    data = Job.objects.get(id=pid)
    d={'data':data}
    return render(request,'job_detaile.html',d)

def apply_forjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login') 
    error=""
    user=request.user
    student=StudentUser.objects.get(user=user)
    job=Job.objects.get(id=pid)
    date1=date.today()
    if job.end_date < date1:
        error="close"
    elif job.start_date > date1:
        error="notopen"
    else:

        if request.method=="POST":
            r=request.FILES['resume']
            Apply.objects.create(student=student,resume=r,apply_date=date.today(),job=job)
            error="done"
    d={'error':error}        

    return render(request,'apply_forjob.html',d)

def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    data=Apply.objects.all()
    d={'data':data}
    return render(request,'applied_candidatelist.html',d)


def contact(request):
    return render(request,'contact.html')