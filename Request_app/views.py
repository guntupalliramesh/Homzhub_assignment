from django.http import HttpResponse, FileResponse
from django.template import response
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout, login
from django.contrib import messages
from .models import StateMaster, RequestTypeMaster, StatusMaster, UserRequest, ScrappedResult
import datetime
from django.contrib.auth import logout as django_logout
from rest_framework import viewsets
from .serializers import UserRequestSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request

def Login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect('/request/')
        else:
           return render(request, 'Login.html')
    else:
        userid = request.POST["userid"]
        password = request.POST["password"]
        user = auth.authenticate(username=userid, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/request/')
        else:
            messages.info(request, 'Invalid login details')
            return HttpResponseRedirect('/Login/')

def Logout(request):
    if not request.user.is_authenticated:
        return render(request, 'Login.html')
    django_logout(request)
    return render(request, 'Login.html')

def Signup(request):
     if request.method == "GET":
         return render(request, 'Signup.html')
     else:
         username = request.POST['userid']
         email = request.POST['email']
         Password1 = request.POST['Password1']
         Password2 = request.POST['Password2']
         if Password1 != Password2:
             messages.info(request, 'Passwords not matching')
             return render(request, 'Signup.html')
         elif User.objects.filter(username=username).exists():
             messages.info(request, 'User already exist')
             return render(request, 'Signup.html')
         elif User.objects.filter(email=email).exists():
             messages.info(request, 'email already exist')
             return render(request, 'Signup.html')
         else:
             authuser = User.objects.create_user(username = username, password=Password1, email=email)
             authuser.save()
             messages.info(request, 'Registered succesfully!')
             return HttpResponseRedirect('/Login/')



def RequestView(request):
  if not request.user.is_authenticated:
      return render(request, 'Login.html')
  if request.method == 'GET':
      Requests = UserRequest.objects.filter(RequestedUser=request.user)
      context = {
        'Requests':Requests
      }
      return render(request, 'Base.html', context)

def AddRequest(request):
  if not request.user.is_authenticated:
      return render(request, 'Login.html')
  if request.method == 'GET':
      RequestType = RequestTypeMaster.objects.all()
      allstates =  StateMaster.objects.all()
      context = {
        'RequestType':RequestType,
        'allstates':allstates,
      }
      return render(request, 'AddRequest.html', context)
  else:
    RequestType =  request.POST['rtype'];
    RequestDescription = request.POST['Rqdesc']
    phonenum = request.POST['phonenum']
    ccode = request.POST['ccode']
    pcode = request.POST['pcode']
    state = request.POST['state']
    cityname = request.POST['cityname']
    Request_Instance = RequestTypeMaster.objects.get(id=RequestType)
    State_Instance = StateMaster.objects.get(id=state)
    Status_Instance = StatusMaster.objects.get(id=1)
    Request = UserRequest(RequestedUser=request.user,RequestType=Request_Instance,RequestDesc=RequestDescription,City=cityname,State=State_Instance,Pincode=pcode,PhoneCode=ccode,Phone=phonenum,Status=Status_Instance,Remark='pending')
    Request.save()
    return HttpResponseRedirect('/request/')


class RequestViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserRequestSerializer
    queryset = UserRequest.objects.all()
    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(RequestedUser=self.request.user)
        return self.queryset

def ReqDetail(request, id):
    if not request.user.is_authenticated:
      return render(request, 'Login.html')
    Request = UserRequest.objects.filter(RequestedUser=request.user, id=id)
    context = {
        'Request':Request
      }
    return render(request, 'RequestDetail.html', context)



def OpenAssignment2(request):
    ScrapWeb()
    if request.method == 'GET':
        Result = ScrappedResult.objects.all()
        count = ScrappedResult.objects.all().count()
        context = {
            'Result':Result,
            'count':count,
      }
        return render(request, 'ScrappedResult.html', context)

def ScrapWeb():
    news_url=['https://realty.economictimes.indiatimes.com/rss/residential','https://realty.economictimes.indiatimes.com/rss/topstories','https://economictimes.indiatimes.com/wealth/real-estate/rssfeeds/48997582.cms']
    for news in news_url:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request(url=news, headers=headers)
        Client=urlopen(req)
        xml_page=Client.read()
        Client.close()
        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        for news in news_list:
              if ScrappedResult.objects.filter(Title = news.title.text,Link = news.link.text, PubDate = news.pubDate.text).exists():
                  print("not found")
              else:
                  ScrappedResults = ScrappedResult(Title = news.title.text,Link = news.link.text, PubDate = news.pubDate.text)
                  ScrappedResults.save()