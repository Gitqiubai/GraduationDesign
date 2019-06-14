from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import nltk
from .models import article,comment
from userlogin.models import message_table
import json
import time
from QQ.SendMessage import send_private_msg
# Create your views here.


def indexPage(request):

    #按照最新回复排序
    #article_list=article.objects.all().order_by('-newsdate')[0:10]
    article_list=article.objects.filter(content_verify=1,state=0).order_by('-newsdate')[0:10]
    all_article = article.objects.filter(content_verify=1,state=0).count()
    print(all_article)
    if request.COOKIES.get('username'):
        #user_name = request.COOKIES.get('username')
        user_name = request.session['username']
        message = comment.objects.filter(comment_to=user_name,read=False).count()
        user_mess = message_table.objects.get(username=user_name)

        #判断是否有页码
        if request.GET.get('page'):
            print('已经登陆:{}'.format(request.COOKIES.get('username')))
            page_num=request.GET.get('page')
            print('有页码:{}'.format(page_num))
            page=(int(page_num)-1)*10
            #article_list = article.objects.filter(article_id__range=[page,page+5]).order_by('article_id')
            article_list = article.objects.filter(content_verify=1,state=0).order_by('-newsdate')[page:page+10]

            return render(request, 'index.html', {'username': user_name,'article_list':article_list,'total':all_article,'currentPage':int(page_num),'message':message,"user_mess":user_mess})
        else:
            print('没有页码')
            return render(request, 'index.html', {'username': user_name, 'article_list': article_list,'total':all_article,'currentPage':1,'message':message,"user_mess":user_mess})
    else:
        if request.GET.get('page'):
            page_num=request.GET.get('page')
            print('有页码:{}'.format(page_num))
            page=(int(page_num)-1)*10
            #article_list = article.objects.filter(article_id__range=[page,page+5]).order_by('article_id')
            article_list = article.objects.filter(content_verify=1,state=0).order_by('-newsdate')[page:page+10]
            return render(request, 'index.html', {'article_list': article_list, 'total': all_article,'currentPage':int(page_num),'message':0})

        print('还没登陆')
        return render(request,'index.html',{'article_list':article_list,'total':all_article,'currentPage':1,'message':0})



def test1(request):


    return render(request, 'test.html')


def test(request):
    username_a=request.COOKIES.get('username')
    #username_a=request.session['username']
    if username_a:

        username = request.session['username'] #获取当前cookie的user
        message = comment.objects.filter(comment_to=username, read=False).count()
        user_mess= message_table.objects.get(username=username)
        if request.method == 'GET':
            if request.GET.get('action') == 'edit':
                article_id=request.GET.get('article_id')
                #username=request.COOKIES.get('username')
                #username=request.session['username']
                print('测试断点：{}'.format(request.GET.get('action')))
                #article_content=article.objects.filter(article_id=article_id,uid=username)[0]

                if message_table.objects.get(username=request.session['username']).is_superuser:
                    article_content = article.objects.filter(article_id=article_id)[0]
                else:
                    article_content = article.objects.filter(article_id=article_id, uid=username)[0]
                return render(request, 'release.html',{"article":article_content,"username":username,'message':message,'user_mess':user_mess})

            elif request.GET.get('action') == 'del':

                article_id = request.GET.get('article_id')

                if message_table.objects.get(username=request.session['username']).is_superuser:
                    art = article.objects.get(article_id=article_id)
                else:
                    art = article.objects.get(uid=username, article_id=article_id)

                if art:
                    art.delete()
                    com = comment.objects.filter(f__article_id=article_id).delete()
                    return HttpResponseRedirect('/')


                else:
                    return HttpResponse('请勿进行越权操作')

        return render(request, 'release.html',{'username':username,'message':message,'user_mess':user_mess})
    else:
        return HttpResponseRedirect('/../../login')

#评论模块
def content(request):


    if request.method == 'GET':

        aid = request.GET.get('article_id')
        #all_comment = comment.objects.filter(f__article_id=aid).count()


        if request.GET.get('command_id'):

            #auth=request.COOKIES.get('username')
            auth=request.session['username']
            message = comment.objects.filter(comment_to=auth, read=False).count()

            cid=request.GET.get('command_id')
            print(">>>:{}".format(aid))

            if message_table.objects.get(username=request.session['username']).is_superuser:
                del_comment=comment.objects.filter(f__article_id=aid,f_id=cid)[0]
                del_comment.delete()
            else:
                del_comment = comment.objects.filter(f__article_id=aid, comment_auth=auth, f_id=cid)[0]
                del_comment.delete()

        print(aid)
        arti = article.objects.filter(article_id=aid)[0]
        com = comment.objects.filter(f__article_id=aid).order_by('-comment_date')[0:5]
        if request.GET.get('comment_page'):
            page_num = int(request.GET.get('comment_page'))
            page = (page_num-1)*5
            com = comment.objects.filter(f__article_id=aid).order_by('-comment_date')[page:page+5]
        else:
            page_num = 1




    else:


        aid = request.GET.get('article_id')
        arti = article.objects.filter(article_id=aid)[0]

        article_auth = arti.uid
        article_title = arti.title
        action=request.POST.get('action')
        art_id = request.GET.get('article_id')
        com = comment.objects.filter(f__article_id=art_id)
        if action == 'add':

            auth = request.session['username']
            auth_head = message_table.objects.get(username=auth).headImage
            auth_nickname = message_table.objects.\
            get(username=auth).nick_name
            com_content = request.POST.get('comment_content')

            command_save = comment()
            com_num = comment.objects.filter(f__article_id=art_id).count()

            article_update = article.objects.get(article_id=art_id)
            print('当前评论数量{}'.format(com_num))

            command_save.f__article_id=art_id
            command_save.comment_auth=auth
            command_save.comment_content=com_content
            command_save.comment_to=article_auth
            command_save.comment_article_title = article_title
            command_save.f_id=aid
            command_save.auth_head = auth_head
            command_save.auth_nickname =auth_nickname

            command_save.save()

            article_update.reply_num = com_num+1
            article_update.save()

            return HttpResponseRedirect('/index/content/?article_id={}'.format(aid))




            #return HttpResponse(com_content+'  '+art_id)
        elif action == 'del':

            #auth = request.COOKIES.get('username')
            auth = request.session['username']
            cid = request.POST.get('delcomment')
            if message_table.objects.get(username=request.session['username']).is_superuser:
                del_comment = comment.objects.filter(f__article_id=aid, id=cid)[0]
            else:
                del_comment = comment.objects.filter(f__article_id=aid, comment_auth=auth, id=cid)[0]
            del_comment.delete()
            #return HttpResponse('shanchu')
            return HttpResponseRedirect('/index/content/?article_id={}'.format(aid))



    if request.COOKIES.get('username'):

        if request.GET.get('comment_page'):
            page_num = int(request.GET.get('comment_page'))
            page = (page_num - 1) * 5
        else:
            page_num = 1
        print('已经登陆')
        print(request.COOKIES.get('username'))
        #user_name=request.COOKIES.get('username')
        user_name=request.session['username']
        user_mess = message_table.objects.get(username=user_name)
        message = comment.objects.filter(comment_to=user_name, read=False).count()
        print(user_name)
        print(arti.uid)
        all_comment = comment.objects.filter(f__article_id=aid).count()
        return render(request,'articleContent.html',{'username':user_name,'article':arti,'comment':com,'total':all_comment,'currentPage':int(page_num),'message':message,"user_mess":user_mess})
    else:
        if request.GET.get('comment_page'):
            page_num = int(request.GET.get('comment_page'))
        else:
            page_num = 1
        page = (page_num - 1) * 5
        all_comment = comment.objects.filter(f__article_id=aid).count()
        return render(request, 'articleContent.html',{'article':arti,'comment':com,'total':all_comment,'currentPage':int(page_num),'message':0})


def mymessage(request):

    if request.COOKIES.get('username'):
        #username = request.COOKIES.get('username')
        username = request.session['username']
        user_mess = message_table.objects.get(username=username)

        message_num = comment.objects.filter(comment_to=username,read=False).count()

        if request.method == "GET":
            if request.GET.get("currentPage"):

                currentPage = int(request.GET.get('currentPage'))+1

                #message = comment.objects.filter(comment_to=username)[currentPage*5:currentPage*5+5]

                try:
                    message = comment.objects.filter(comment_to=username).order_by('-comment_date')[currentPage*10:currentPage*10+10]
                except:
                    message == None

                if message:
                    dic=[]
                    for each in message:
                        each.read = True
                        each.save()
                        comment_auth = each.comment_auth
                        comment_title = each.comment_article_title
                        comment_date = 	each.comment_date
                        comment_content = each.comment_content
                        article_id = each.f_id
                        comment_nickname = each.auth_nickname
                        comment_authhead =each.auth_head


                        mess = """
                                <div class="CommentBox">
                                    <div class="msgCon">
                                        <div class="msgBox">
                                            <div class="headUrl">
                                                <img src="/media/{}" width="50" height="50">
                                                <div>
                                                    <span class="title">[{}] 在 <a href='/index/content/?article_id={}'>[{}]</a> 回复了你</span>
                                                    
                                                    <span class="time">{}</span>
                                                </div>
                            
                                            </div>
                                            <div class="msgTxt">
                                                {}
                                            </div>
                                        </div>
                                    </div> 
                                <div class="CommentBox">                     
                                """.format(comment_authhead,comment_nickname,article_id,comment_title,comment_date,comment_content)
                        dic.append(mess)
                    resp = {
                        'code': '200',
                        'message': 'success',
                        'data': {'replay':dic,'currentPage':currentPage+1},
                    }
                    response = HttpResponse(content=json.dumps(resp), content_type='application/json;charset = utf-8',
                                            status='200',
                                            reason='success',
                                            charset='utf-8')

                    return response
                else:
                    return HttpResponse('')

            else:
                message = comment.objects.filter(comment_to=username).order_by('-comment_date')[0:10]

            for each in message:
                each.read = True
                each.save()
        else:
            return HttpResponseRedirect('/login')


    else:
        return HttpResponseRedirect('/login')




    return render(request, 'replay.html',{'username':username,"message_num":message,"messages":message,'user_mess':user_mess})

#审核模块
def Reviewed(request):

    if request.COOKIES.get('username'):

        if message_table.objects.get(username=request.session['username']).is_superuser:
            username = request.session['username']
            message_num = comment.objects.filter(comment_to=username, read=False).count()
            user_mess = message_table.objects.get(username=username)
            not_verify = article.objects.filter(content_verify=0)

            if request.method == "GET":
                if request.GET.get('type') == 'auditing':
                    not_verify = article.objects.filter(content_verify=1)

                elif request.GET.get('type') == 'Unaudited':
                    not_verify = article.objects.filter(content_verify=2)

                else:

                    if request.GET.get("reviewed_id"):
                        if request.GET.get('action') == "pass":

                            art_id = article.objects.get(article_id=request.GET.get("reviewed_id"))
                            art_id.content_verify = "1"
                            art_id.save()
                            #发送消息模块
                            try:

                                headstr = '【遗失】' if art_id.lost_type == 0 else '【拾取】'
                                headstr += '【{}】'.format(art_id.lostdate)+'【{}】'.format(art_id.item)
                                send_private_msg(headstr+art_id.title+'\n -'+'\n'+'详情: http://127.0.0.1:8000/index/content/?article_id={}'.format(art_id.article_id))

                            except:
                                pass

                        else:
                            art_id = article.objects.get(article_id=request.GET.get("reviewed_id"))

                            art_id.content_verify = "2"
                            art_id.save()

                        return  HttpResponseRedirect("/reviewed/")

            return render(request, "reviewed.html", {"article_list": not_verify,'user_mess':user_mess,'username':username,'message':message_num})
        else:
            return HttpResponse("这是个虚假的403 但是你真的无权访问该页面")

    return HttpResponseRedirect("/reviewed/")

def recover(request):
    # 按照最新回复排序
    # article_list=article.objects.all().order_by('-newsdate')[0:10]
    article_list = article.objects.filter(content_verify=1,state=1).order_by('-newsdate')[0:10]
    all_article = article.objects.filter(content_verify=1,state=1).count()
    print(all_article)
    if request.COOKIES.get('username'):
        # user_name = request.COOKIES.get('username')
        user_name = request.session['username']
        message = comment.objects.filter(comment_to=user_name, read=False).count()
        user_mess = message_table.objects.get(username=user_name)

        # 判断是否有页码
        if request.GET.get('page'):
            print('已经登陆:{}'.format(request.COOKIES.get('username')))
            page_num = request.GET.get('page')
            print('有页码:{}'.format(page_num))
            page = (int(page_num) - 1) * 10
            # article_list = article.objects.filter(article_id__range=[page,page+5]).order_by('article_id')
            article_list = article.objects.all().order_by('-newsdate')[page:page + 10]

            return render(request, 'index_re.html',
                          {'username': user_name, 'article_list': article_list, 'total': all_article,
                           'currentPage': int(page_num), 'message': message, "user_mess": user_mess})
        else:
            print('没有页码')
            return render(request, 'index_re.html',
                          {'username': user_name, 'article_list': article_list, 'total': all_article, 'currentPage': 1,
                           'message': message, "user_mess": user_mess})
    else:
        if request.GET.get('page'):
            page_num = request.GET.get('page')
            print('有页码:{}'.format(page_num))
            page = (int(page_num) - 1) * 10
            # article_list = article.objects.filter(article_id__range=[page,page+5]).order_by('article_id')
            article_list = article.objects.all().order_by('-newsdate')[page:page + 10]
            return render(request, 'index_re.html',
                          {'article_list': article_list, 'total': all_article, 'currentPage': int(page_num),
                           'message': 0})

        print('还没登陆')
        return render(request, 'index_re.html',
                      {'article_list': article_list, 'total': all_article, 'currentPage': 1, 'message': 0})

    pass



def page_not_found(request):

    responce = render('404.html', {})
    responce.status_code = 404
    return responce

def page_errors(request):
    """
    500页面
    """
    responce = render('500.html', {})
    responce.status_code = 500
    return responce
