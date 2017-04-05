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
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators
from datetime import timedelta

def kritsnam(request):
    return render(request,'czo/kritsnam.html')

def gateway(request):
    if request.user.is_superuser == 1:
        gateway_id = request.GET.get('gateway_id')
        if gateway_id!=None:
            mygateway = Gateway.objects.filter(id=gateway_id)
            mygateways = Gateway.objects.all()
            if (mygateway):
                gatewaystats = GatewayStats.objects.filter(gateway=mygateway[0].id)
                print (len(gatewaystats))
                return render(request, 'czo/gateway.html' , { 'gateways' : mygateways, 'gatewaystats' : gatewaystats , 'gateway_id':int(gateway_id) })
            return render(request, 'czo/sensor.html')
        else:
            mygateways = Gateway.objects.all()
            if (mygateways):
                gatewaystats = GatewayStats.objects.filter(gateway=mygateways[0].id)
                return render(request, 'czo/gateway.html' , { 'gateways' : mygateways, 'gatewaystats' : gatewaystats , 'gateway_id':mygateways[0].id })
            return render(request, 'czo/sensor.html')
    else:
        return render(request,'500.html')

def change_pass(request):
    if request.method == "POST":
        curr_pass = request.POST['curr_pass']
        new_pass = request.POST['New_pass']
        if request.user.check_password(curr_pass):
            val = validators.validate_password(new_pass, request.user)
            print(val)
            if val is None:
                u = User.objects.get(username=request.user.username)
                u.set_password(new_pass)
                u.save()
                mynodes = Node.objects.filter(owner=request.user)
                return render (request,'czo/success1.html')
            else:
                return render(request,'czo/pass.html')
        else:
            return render(request,'czo/pass.html', {'error_message': 'Wrong Password'}  )
    else:
        return render(request,'czo/pass.html')

def set_pass(request):
    names = request.GET.get('username')
    if request.method == "POST":
        print('lol_post')
        otp = request.POST['otp']
        new_pass = request.POST['New_pass']
        u = User.objects.get(username=names)
        if u.first_name != '':
            if otp == u.first_name:
                u.set_password(new_pass)
                u.save()
                return render (request,'czo/success1.html')
        else:
            return render(request,'czo/set_pass.html', {'error_message': 'Wrong otp'}  )
    else:
        print('lol_get')
        return render(request, 'czo/set_pass.html' )

def forget_pass(request):
    if request.method == "POST":
        username = request.POST['username']
        user = User.objects.get(username=username)
        if user:
            subject =  "OTP for activation of your account: "
            x = random.randint(100000,999999)
            message =   ("Hi " + username + " Put this number in form to verify your Email : "
                        + str(x) + ", you can also follow to this link to set new_pass to your Account http://127.0.0.1:8000/czo/set_pass/?username="
                        + username)
            to_email = user.email
            from_email = "satendrapandeymp@gmail.com"
            user.first_name = str(x)
            send_mail(subject, message, from_email, [to_email])
            user.save()
            return HttpResponseRedirect('/czo/set_pass/?username='+str(username))
        else:
            return render(request,'czo/forget_pass.html', {'error_message': 'Wrong username'}  )
    else:
        return render(request,'czo/forget_pass.html')

# It's the homepage
def index(request):
        mynodes = Node.objects.filter(owner=request.user)
        return render(request, 'czo/index.html' , { 'mynodes' : mynodes})

# It's for testing some new things
def otp(request):
        names = request.GET.get('username')
        print(names)
        myuser = User.objects.get(username=names)
        if request.method == "POST":
            otp = request.POST['otp']
            if len(myuser.last_name) < 5:
                if otp == myuser.first_name :
                    myuser.first_name=""
                    myuser.is_active = 1
                    myuser.save()
                    return render (request,'czo/success.html')
                else:
                    myuser.last_name = myuser.last_name + 'a';
                    print(myuser.last_name)
                    myuser.save()
                    return render(request, 'czo/login.html', {'error_message': 'Your account has been disabled'})
            else:
                subject =  "OTP for activation of your account: "
                x = random.randint(100000,999999)
                message =   ("Hi " + myuser.username + " Put this number in form to verify your Email : "
                            + str(x) + ", you can also follow to this link to verify your otp http://127.0.0.1:8000/czo/otp/?username="
                            + myuser.username)
                to_email = myuser.email
                from_email = "satendrapandeymp@gmail.com"
                myuser.first_name = str(x)
                myuser.last_name = ""
                send_mail(subject, message, from_email, [to_email])
                user_name = str(myuser.username)
                myuser.save()
                return HttpResponseRedirect('/czo/otp/?username='+ str(user_name))
        return render(request,'czo/test.html' , {'names':names})

# it's for registering new user
class Register_User(View):
    form_class = UserForm
    template_name = 'czo/reg.html'

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
            val = validators.validate_password(password, username)
            if val is None:
                user.set_password(password)
                user.is_active = 0
                subject =  "OTP for activation of your account: "
                x = random.randint(100000,999999)
                message =   ("Hi " + username + " Put this number in form to verify your Email : "
                            + str(x) + ", you can also follow to this link to verify your otp http://127.0.0.1:8000/czo/otp/?username="
                            + username)
                to_email = user.email
                from_email = "satendrapandeymp@gmail.com"
                user.first_name = str(x)
                send_mail(subject, message, from_email, [to_email])
                user_name = str(username)
                user.save()
                return HttpResponseRedirect('/czo/otp/?username='+ username)
            else:
                return render (request,self.template_name , {'form' :form })

# For user login
def login_user(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return HttpResponseRedirect('/czo/')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/czo/')
            else:
                return render(request, 'czo/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'czo/login.html', {'error_message': 'Invalid login'})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/czo/')
        return render(request, 'czo/login.html')

# For logout user
def logout_user(request):
        logout(request)
        return HttpResponseRedirect('/')

# To find all Sensors att One place
def sensors(request):
    if request.method=="GET":
        sensor_id = request.GET.get('id')
        if sensor_id==None:
            mynodes = Node.objects.filter(owner=request.user)
            if (mynodes):
                sensors = Sensor.objects.filter(node_name=mynodes[0].id)[:1]
                if (sensors):
                    timedelta1 = timedelta(days=7)
                    datas = Data.objects.filter(sensor_name=sensors[0].id, doc__gte= datetime.datetime.now()-timedelta1)
                    sensor_first = sensors[0].id
                    return render(request, 'czo/sensors.html' , { 'mynodes' : mynodes, 'datas' : datas , 'sensor_id' : sensor_first})
        else:
            var = 0
            mynodes = Node.objects.filter(owner=request.user)
            if (mynodes):
                sensors = Sensor.objects.filter(id=sensor_id)
                if (sensors):
                    node = Node.objects.filter(owner=request.user, name = sensors[0].node_name)[:1]
                    if node!={}:
                        timedelta1 = timedelta(days=7)
                        datas = Data.objects.filter(sensor_name=sensors[0].id, doc__gte= datetime.datetime.now()-timedelta1)
                        return render(request, 'czo/sensors.html' , { 'mynodes' : mynodes, 'datas' : datas , 'sensor_id' : int(sensor_id)})
    return render(request, 'czo/sensors.html')
# To Find all sensors attached to a Node
def sensor(request):
    if request.method=="GET":
        node_req = request.GET.get('node_id')
        sensor_id = request.GET.get('sensor_id')
        if node_req!=None:
            if sensor_id==None:
                mynodes = Node.objects.filter(id=node_req,owner=request.user)
                if (mynodes):
                    sensors = Sensor.objects.filter(node_name=mynodes[0].id)[:1]
                    if (sensors):
                        timedelta1 = timedelta(days=7)
                        datas = Data.objects.filter(sensor_name=sensors[0].id, doc__gte= datetime.datetime.now()-timedelta1)
                        name = sensors[0].name
                        return render(request, 'czo/sensor.html' , { 'mynodes' : mynodes, 'datas' : datas , 'nodeName' : node_req,'sensor_id' :sensors[0].id})
            else:
                var = 0
                mynodes = Node.objects.filter(id=node_req,owner=request.user)
                if (mynodes):
                    sensors = Sensor.objects.filter(id=sensor_id)
                    if (sensors):
                        node = Node.objects.filter(owner=request.user, name = sensors[0].node_name)[:1]
                        if node!={}:
                            timedelta1 = timedelta(days=7)
                            datas = Data.objects.filter(sensor_name=sensors[0].id, doc__gte= datetime.datetime.now()-timedelta1)
                            name = sensors[0].name
                            return render(request, 'czo/sensor.html' , { 'mynodes' : mynodes, 'datas' : datas , 'nodeName' : node_req,'sensor_id' :int(sensor_id)})
    return render(request, 'czo/sensor.html')

# To find data of a sensor
def data(request):
    sensor_id = request.GET.get('sensor_id')
    if request.method=="GET":
        mysensors = Sensor.objects.filter(id=sensor_id)
        timedelta1 = timedelta(days=7)
        lol = Data.objects.filter(sensor_name=mysensors[0].id, doc__gte= datetime.datetime.now()-timedelta1)
        return render(request, 'czo/data.html' , {  'mysensor' : lol, 'name':sensor_id})
    else:
        mysensors = Sensor.objects.filter(id=sensor_id)
        timedelta1 = request.POST['initial']
        timedelta2 = request.POST['final']
        print(timedelta1);
        print(timedelta2);
        lol = Data.objects.filter(sensor_name=mysensors[0].id, doc__gte= timedelta1 , doc__lte= timedelta2)
        return render(request, 'czo/data.html' , {  'mysensor' : lol,'name':sensor_id})

# For CSV Download
def csv_out(request):
    sensor_id = request.GET.get('sensor_id')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=sensor-{0}.csv'.format(sensor_id)
    Datas = Data.objects.filter(sensor_name=sensor_id).order_by('doc')
    writer = csv.writer(response)
    writer.writerow(['Data', 'Timestamp'])
    for data in Datas:
        writer.writerow([data.data, data.doc])
    return response
