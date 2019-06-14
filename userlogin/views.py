from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import *
from .models import message_table
from indexPage.models import article
from indexPage.models import comment
from indexPage.models import Notices
from django.views.decorators.csrf import *
import base64,time
from django.core.files.base import ContentFile
import json


# Create your views here.


def ulogin(request):

    if request.method == 'POST':
        user_name=request.POST.get('username')
        user_passw=request.POST.get('passw')
        log=authenticate(username=user_name,password=user_passw)
        if log:

            login(request,log)  #生成cookie
            request.session['username'] = user_name #设置session的值
            print('session',request.session['username']) #获取session的值
            rep=render(request,'redict.html')
            rep.set_cookie('username',user_name,'max_age',60*60*24*14)

            return rep

        else:
            return HttpResponse('登陆失败')

    return render(request,'Login.html')

@csrf_exempt
def uregis(request):
    if request.method == 'POST':
        user_email = request.POST.get('r_email')
        user_username = request.POST.get('r_username')
        user_passw = request.POST.get('r_passw')
        try:
            message_table.objects.create_user(username=user_username,
                                              password=user_passw,
                                              email=user_email,
                                              is_staff=True)
        except:
            return HttpResponse('[注册失败]账号已存在.')

        return HttpResponse('[注册成功]请使用该账号进行登陆')

    return HttpResponse('[请不要尝试非法操作]')

def userMessage(request):

    if request.COOKIES.get('username'):

        if request.method == 'GET':
            print('login_session', request.session['username'])
            #username = request.COOKIES.get('username')
            username = request.session['username']
            message = comment.objects.filter(comment_to=username, read=False).count()
            user_mess = message_table.objects.filter(username=username)[0]
            user_article = article.objects.filter(uid=username).order_by('-releasedate').all()
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',username)
            if request.GET.get('action') == 'edit':

                if request.GET.get('uid') == username:

                    return render(request,'message.html',{'user_mess':user_mess,'action':'edit','username':username,'message':message,'articleList':user_article})

            elif request.GET.get('action') == 'getprofile':
                #http://127.0.0.1:8000/login/user/message/?action=getprofile&username=admin
                if request.GET.get('username'):
                    print('测试点。。')
                    user_article = article.objects.filter(uid=request.GET.get('username')).order_by('-releasedate').all()
                    other_message = message_table.objects.get(username=request.GET.get('username'))
                    return render(request, 'message.html',{'user_mess': user_mess,'other_message':other_message, 'username': username, 'message': message,'articleList': user_article,'action':'getprofile'})



        else:
            #username = request.COOKIES.get('username')
            username = request.session['username']
            user_mess = message_table.objects.filter(username=username)[0]
            message = comment.objects.filter(comment_to=username, read=False).count()


            if username == request.POST.get('uid'):

                user_mess.nick_name = request.POST.get('nickname')
                user_mess.male = request.POST.get('male')
                user_mess.addr = request.POST.get('addr')
                user_mess.email = request.POST.get('email')
                user_mess.about = request.POST.get('about')
                user_mess.QQ = request.POST.get('QQ')
                user_mess.WeChats = request.POST.get('WeChat')
                user_mess.save()
                print("保存成功")
                return HttpResponseRedirect('/login/user/message/')



        #print(user_mess)

        return render(request,'message.html',{'user_mess':user_mess,"username":username,'message':message,'articleList':user_article})
    else:
        return HttpResponseRedirect('/login')

@csrf_exempt
def headImage(request):
    #获取到图片的二进制流
    print("图片>>>:{}".format(request.POST.get('image').replace('data:image/png;base64,','')))
    imgContent = base64.b64decode(request.POST.get('image').replace('data:image/jpeg;base64,',''))
    #imgContent = base64.urlsafe_b64decode(request.POST.get('image').replace('data:image/jpeg;base64,',''))
    #获取modles实例
    headImg = message_table.objects.get(username=request.session['username'])
    #生成文件名
    imgName = request.session['username']+'_'+str(time.time()).replace('.','')+'.jpg'
    #使用ContentFile把二进制的图片文件转换成imgFile可以保存的格式
    headImg.headImage.save(imgName,ContentFile(imgContent))
    print('名字：',imgName)


    return HttpResponse('1')

def Deal(request):

    if request.COOKIES.get('username'):

        if request.session['username']==request.COOKIES.get('username'):

            if request.method == "GET":
                aid = request.GET.get('aid')
                action = request.GET.get('action')
                print(action)

                if action == "delete":
                    if message_table.objects.get(username=request.session['username']).is_superuser:
                        article.objects.get(article_id=aid).delete()
                    else:
                        article.objects.get(article_id=aid,uid=request.session['username']).delete()

                elif action =='re':
                    print("进到这个方法了")
                    s_state=article.objects.get(article_id=aid)
                    s_state.state=True
                    s_state.save()
            else:
                print("测试点....")
                a_aid = request.POST.get('aid')
                recover = request.POST.get('content')
                r_content = article.objects.get(article_id=a_aid)
                r_content.recover_content = recover
                r_content.state=True
                r_content.save()


        else:
            return HttpResponseRedirect('/login')





    return HttpResponseRedirect('/login/user/message/')


def GetArticle(request):

    if request.COOKIES.get('username') == request.session['username']:

        if request.method == "GET":
            aid = request.GET.get('aid')
            print('接收到了参数：{}'.format(aid))
            article_table = article.objects.get(article_id=aid)
            r_content="""
                    <h5 style="text-align: center">{}</h5>
                    <h6 style="text-align: center;color: #8e908c"><span>{}-{}-{}</span></h6>
                    <hr>
                    <div style="width: 90%;margin: auto;">

                            {}

                    </div>
            """.format(article_table.title,article_table.addr,article_table.item,article_table.lostdate,article_table.content)

            return HttpResponse(r_content)

        pass

def GetFound(request):

    article_list = article.objects.filter(content_verify=1, state=1).order_by('-newsdate')[0:10]

    dic = []
    for each in article_list:
        strr = ''

        if each.lost_type == 0:
            strr = '<div class="FoundDiv"><p class="FoundContent">{}</p></div>'.format('[已找回]'+each.title)
        else:
            strr = '<div class="FoundDiv"><p class="FoundContent">{}</p></div>'.format('[已归还]'+each.title)

        dic.append(strr)

    resp = {
        'code': '200',
        'message': 'success',
        'data': {'replay': dic,},
    }
    response = HttpResponse(content=json.dumps(resp), content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')

    return response

def GetNotice(request):

    # 获取最近一条公告
    notice_content = Notices.objects.all().order_by('-Notices_date')[0]

    print(notice_content.Notices_content)
    resp = {
        'code': '200',
        'message': 'success',
        'data': {'replay': notice_content.Notices_content, },
    }
    response = HttpResponse(content=json.dumps(resp), content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')

    return response