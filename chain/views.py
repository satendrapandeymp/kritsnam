from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth import authenticate,login, logout
from .forms import UserForm
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
import random, csv, datetime
from datetime import timedelta


def change_pass(request):
    if request.method == "POST":
        curr_pass = request.POST['curr_pass']
        new_pass = request.POST['New_pass']
        if request.user.check_password(curr_pass):
            u = User.objects.get(username=request.user.username)
            u.set_password(new_pass)
            u.save()
            mynodes = Node.objects.filter(owner=request.user)
            return render (request,'chain/success1.html')
        else:
            return render(request,'chain/pass.html', {'error_message': 'Wrong Password'}  )
    else:
        return render(request,'chain/pass.html')

def set_pass(request, names):
    if request.method == "POST":
        print('lol_post')
        otp = request.POST['otp']
        new_pass = request.POST['New_pass']
        u = User.objects.get(username=names)
        if u.first_name != '':
            if otp == u.first_name:
                u.set_password(new_pass)
                u.save()
                return render (request,'chain/success1.html')
        else:
            return render(request,'chain/set_pass.html', {'error_message': 'Wrong Username'}  )
    else:
        print('lol_get')
        return render(request,'chain/set_pass.html')

def forget_pass(request):
    if request.method == "POST":
        print('lol')
        username = request.POST['username']
        user = User.objects.get(username=username)
        if user:
            subject =  "OTP for activation of your account: "
            x = random.randint(100000,999999)
            message =   ("Hi " + username + " Put this number in form to verify your Email : "
                        + str(x) + ", you can also follow to this link to set new_pass to your Account http://127.0.0.1:8000/chain/set_pass/"
                        + username)
            to_email = user.email
            from_email = "satendrapandeymp@gmail.com"
            user.first_name = str(x)
            send_mail(subject, message, from_email, [to_email])
            user.save()
            return HttpResponseRedirect('/chain/set_pass/'+str(username))
        else:
            return render(request,'chain/forget_pass.html', {'error_message': 'Wrong username'}  )
    else:
        return render(request,'chain/forget_pass.html')

def AddUser(request):
    if request.method == "POST":
        form = ProfileForm(request.POST , request.FILES )
        if form.is_valid():
            temp_node = form.save(commit=False)
            temp_node.owner = request.user
            temp_node.save()
            mynodes = Node.objects.filter(owner=request.user)
            return render(request, 'chain/index.html' , { 'mynodes' : mynodes})
        else:
            form = ProfileForm(initial={'owner': request.user})
            return render(request, 'chain/test.html')
    else:
        form = ProfileForm()
        return render(request, 'chain/profile_form.html', {'form': form})


# For updating the User
class UpdateUser(UpdateView):
        model= Profile
        fields = ['first_name','last_name','about', 'image']


# It's the homepage
def index(request):
        mynodes = Node.objects.filter(owner=request.user)
        return render(request, 'chain/index.html' , { 'mynodes' : mynodes})

# It's for testing some new things
def test(request,names):
        myuser = User.objects.get(username=names)
        if request.method == "POST":
            otp = request.POST['otp']
            if len(myuser.last_name) < 5:
                if otp == myuser.first_name :
                    myuser.first_name=""
                    myuser.is_active = 1
                    myuser.save()
                    return render (request,'chain/success.html')
                else:
                    myuser.last_name = myuser.last_name + 'a';
                    print(myuser.last_name)
                    myuser.save()
                    return render(request, 'chain/login.html', {'error_message': 'Your account has been disabled'})
            else:
                subject =  "OTP for activation of your account: "
                x = random.randint(100000,999999)
                message =   ("Hi " + myuser.username + " Put this number in form to verify your Email : "
                            + str(x) + ", you can also follow to this link to verify your otp http://127.0.0.1:8000/chain/otp/"
                            + myuser.username)
                to_email = myuser.email
                from_email = "satendrapandeymp@gmail.com"
                myuser.first_name = str(x)
                myuser.last_name = ""
                send_mail(subject, message, from_email, [to_email])
                user_name = str(myuser.username)
                myuser.save()
                return HttpResponseRedirect('/chain/otp/'+ str(user_name))
        return render(request,'chain/test.html' , {'names':names} )

# it's for registering new user
class Register_User(View):
    form_class = UserForm
    template_name = 'chain/reg.html'

    def get(self,request):
        form = self.form_class(None)
        return render (request,self.template_name , {'form' :form })

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # normalised data_set
            username = form.cleaned_data ['username']
            password = form.cleaned_data ['password']
            user.set_password(password)
            user.is_active = 0
            subject =  "OTP for activation of your account: "
            x = random.randint(100000,999999)
            message =   ("Hi " + username + " Put this number in form to verify your Email : "
                        + str(x) + ", you can also follow to this link to verify your otp http://127.0.0.1:8000/chain/otp/"
                        + username)
            to_email = user.email
            from_email = "satendrapandeymp@gmail.com"
            user.first_name = str(x)
            send_mail(subject, message, from_email, [to_email])
            user_name = str(username)
            user.save()
            return HttpResponseRedirect('/chain/otp/'+ username)

# For user login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                mynodes = Node.objects.filter(owner=request.user)
                return render(request, 'chain/index.html', {'mynodes' : mynodes})
            else:
                return render(request, 'chain/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'chain/login.html', {'error_message': 'Invalid login'})
    return render(request, 'chain/login.html')

# For logout user
def logout_user(request):
        logout(request)
        return render(request, 'chain/login.html')

# To find all Sensors att One place
def sensors(request):
        mynodes = Node.objects.filter(owner=request.user)
        return render(request, 'chain/sensors.html' , { 'mynodes' : mynodes})

# To Find all sensors attached to a Node
def sensor(request,names):
        mynodes = Node.objects.filter(name=names)
        return render(request, 'chain/sensor.html' , { 'mynodes' : mynodes})

# To find data of a sensor
def data(request,names):
    if request.method=="GET":
        mysensors = Sensor.objects.filter(name=names)
        timedelta1 = timedelta(days=90)
        lol = Data.objects.filter(sensor_name=mysensors[0].id, doc__gte= datetime.datetime.now()-timedelta1)
        return render(request, 'chain/data.html' , {  'mysensor' : lol, 'name':names})
    else:
        mysensors = Sensor.objects.filter(name=names)
        timedelta1 = request.POST['initial']
        timedelta2 = request.POST['final']
        lol = Data.objects.filter(sensor_name=mysensors[0].id, doc__gte= timedelta1 , doc__lte= timedelta2)
        return render(request, 'chain/data.html' , {  'mysensor' : lol,'name':names})
# To find all data From all sensors
def datas(request):
        mynodes = Node.objects.filter(owner=request.user)
        lol = Data.objects.filter(sensor_name=10)
        lol1 = Data.objects.filter(sensor_name=4).order_by('doc')
        return render(request, 'chain/datas.html' , { 'mynodes' : mynodes, 'mysensor' : lol, 'mysensors' : lol1})

# For CSV Download
def csv_out(request,names):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={0}.csv'.format(names)
    mysensors = Sensor.objects.filter(name=names)
    id_sen = mysensors[0].id;
    lol = Data.objects.filter(sensor_name=id_sen).order_by('doc')
    writer = csv.writer(response)
    writer.writerow(['Data', 'Timestamp', 'UnixTimestamp'])
    for data in lol:
        writer.writerow([data.data, data.doc, time.mktime(data.doc.timetuple())])
    return response
