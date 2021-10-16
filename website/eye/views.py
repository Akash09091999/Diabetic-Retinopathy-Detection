from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import *
import datetime


# Create your views here.
def index(request):
	if request.session.has_key('userid'):
		return render(request,"index_after_login.html")
	elif request.session.has_key('docid'):
		
		pt=Patient.objects.filter(Did=request.session['docid']).order_by('Name')
		pf=list()
		for ob in pt:
			for m in Performance.objects.filter(pid=ob.id).order_by('-time')[0:1]:
				pf.append([ob.id,ob.Name,ob.age,m.accuracy,m.time,m.category])
		print(pf)
        
		tot=pt.count()
		d={'n':request.session['Name'],'c':request.session['city'],'a':request.session['age'],'do':request.session['dob'],'pf':pf,'tot':tot}
		return render(request,"doctor222.html",d)



	return render(request,"index.html")

def test(request):
	if request.session.has_key('docid') and request.method=='POST':
		id1=request.POST['pic']
		request.session['id1']=id1

		return render(request,"doc_index_after_login.html")


def vid(request):
	return render(request,"havingvideo.html")   
	
def logout(request):
	if request.session.has_key('userid'):
		request.session.flush()
	if request.session.has_key('docid'):
		request.session.flush()	
	return redirect('/')
	
def myprofile(request):
	if request.session.has_key('userid'):
		dd=Doctor.objects.all()
		now=datetime.datetime.now()
		current_time = now.strftime("%H:%M:%S")
		today = datetime.date.today()
		d2 = today.strftime("%B %d, %Y")
		t=Performance.objects.filter(pid=request.session['userid']).order_by('-time')
		total=t.count()
		d={'n':request.session['Name'],'c':request.session['city'],'a':request.session['age'],'do':request.session['dob'],'dd':dd,'date':d2,'time':current_time,'t':t,'total':total}
		return render(request,"index222.html",d)
	return redirect('/signup')

def setdoctor(request):
	t=Patient.objects.get(id=request.session['userid'])
	t.Did=float(request.POST['cars'])
	t.save()
	return redirect('/myprofile')
def signin(request):
	if request.method=="POST":
		email=request.POST['name']
		password=request.POST['pass']
		dop=request.POST['member_level']
		if dop=="doctor":
			doctor=Doctor.objects.get(email=email,password=password)
			request.session['Name']=doctor.Name
			request.session['city']=doctor.city
			request.session['age']=doctor.age
			request.session['dob']=str(doctor.Dob)
			request.session['docid']=doctor.id
			
			
			
		elif dop=="patient":
			user=Patient.objects.get(email=email,password=password)
			request.session['Name']=user.Name
			request.session['city']=user.city
			request.session['age']=user.age
			request.session['dob']=str(user.Dob)
			request.session['userid'] = user.id
			
			
		if request.session.has_key('userid'):
			
			return redirect('/')

		elif request.session.has_key('docid'):
			
			return redirect('/')

		else:
			return redirect('/signin')

	return render(request,"login.html")

def signup(request):
	if request.method=='POST':
		dop=request.POST['member_level']
		name=request.POST['name']
		monumber=request.POST['monumber']
		email=request.POST['email']
		city=request.POST['city']
		dob=request.POST['dob']
		age=request.POST['age']
		password=request.POST['pass']
		
		if dop=="doctor":
			data=Doctor(Name=name,Number=monumber,email=email,password=password,city=city,Dob=dob,age=age)
			data.save()
			return redirect('/signin')
		else:
			data=Patient(Name=name,Number=monumber,email=email,password=password,city=city,Dob=dob,age=age,Did=0)
			data.save()
			return redirect('/signin') 
	return render(request,"register.html")

def result(request):
	if request.method=='POST' and request.FILES['eyeimage']:

		import os
		from os import path
		project_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		img_url=os.path.join(project_path,'test_images','uploaded','uploaded.jpg')
		os.remove(img_url)

		myfile=request.FILES['eyeimage']
		fs=FileSystemStorage()
		fname=fs.save("uploaded.jpg",myfile)
		uploaded_url=fs.url(fname)
		#uploaded_url = os.path.join(project_path,'test_images', 'uploaded', 'uploaded.jpg')
		
		
		
		from .classifier import prediction
		tested,percent=prediction()

		if percent<=41:
			b="Normal"
		elif percent<=48:
			b="Mild"
		elif percent<=58:
			b="Moderate"
		elif percent<=78:
			b="Severe"
		else:
			b="Very Severe"

	if request.session.has_key('userid'):
		#save last copy of photo
		
		a=str(request.session['userid'])+".jpg"
		upurl = os.path.join(project_path,'eye','static','user_last_photo',a)
		if os.path.exists(upurl):
			os.remove(upurl)
		folder='eye/static/user_last_photo/'
		fs=FileSystemStorage(location=folder)
		fs.save(a,myfile)
		
		pid=request.session['userid']
		accuracy=percent
		time=datetime.datetime.now()
		picture=a
		category=b
		data=Performance(pid=pid,accuracy=accuracy,time=time,picture=picture,category=category)
		data.save()
		return render(request,"result_after_login.html",{'tested': tested,'url':uploaded_url,'percent':percent,'category':category})

	if request.session.has_key('docid'):
		#save last copy of photo
		
		
		a=str(request.session['id1'])+".jpg"
		upurl = os.path.join(project_path,'eye','static','user_last_photo',a)
		if os.path.exists(upurl):
			os.remove(upurl)
		folder='eye/static/user_last_photo/'
		fs=FileSystemStorage(location=folder)
		fs.save(a,myfile)
		
		pid=request.session['id1']
		accuracy=percent
		time=datetime.datetime.now()
		picture=a
		category=b
		data=Performance(pid=pid,accuracy=accuracy,time=time,picture=picture,category=category)
		data.save()
		return render(request,"doc_result_after_login.html",{'tested': tested,'url':uploaded_url,'percent':percent,'category':category})
	

	return render(request,"results.html",{'tested': tested,'url':uploaded_url,'percent':percent,'category':b})