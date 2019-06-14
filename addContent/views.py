from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from indexPage.models import article,comment
from userlogin.models import message_table

# Create your views here.


def release(request):
    if request.COOKIES.get('username'):

        #username = request.COOKIES.get('username')
        username = request.session['username']
        user_mess = message_table.objects.get(username=username)
        message = comment.objects.filter(comment_to=username, read=False).count()
        if request.method == 'POST':

            add_title=request.POST.get('title')
            add_addr=request.POST.get('addr')
            add_content=request.POST.get('content')
            add_item=request.POST.get('item')
            add_lostdate=request.POST.get('lostdate')
            #add_losttype=request.POST.get('lostType')
            if request.POST.get('lostType') == 'lost':
                add_losttype = '0'
            elif request.POST.get('lostType') == 'pickup':
                add_losttype = '1'
            arti = article()
            arti.title=add_title
            arti.addr=add_addr
            arti.content=add_content
            arti.uid=username
            arti.item=add_item
            arti.lostdate=add_lostdate
            arti.lost_type = add_losttype
            arti.save()

            try:
                aid=article.objects.filter(uid=username,title=add_title,content=add_content,addr=add_addr)[0]
                aid=aid.article_id
                return HttpResponseRedirect('../../index/content/?article_id={}'.format(aid))

            except:
                return HttpResponse('请勿发送重复内容')


        return render(request,'release.html',{"username":username,'message':message,'user_mess':user_mess})

    else:
        return render(request,'login.html')

def edit(request):

    if request.COOKIES.get('username'):
        #username = request.COOKIES.get('username')
        username = request.session['username']
        user_mess = message_table.objects.get(username=username)
        print('断点测试111111111：',username)

        message = comment.objects.filter(comment_to=username, read=False).count()

        if request.method == 'POST':
            if request.POST.get('action') == 'edit':
                print('断点2：'.format('edit'))

                article_id=request.POST.get('aid')
                edit_title=request.POST.get('title')
                edit_addr=request.POST.get('addr')
                edit_content=request.POST.get('content')
                if request.POST.get('lostType') == 'lost':
                    add_losttype = '0'
                elif request.POST.get('lostType') == 'pickup':
                    add_losttype = '1'

                #判断是不是管理员
                if message_table.objects.get(username=request.COOKIES.get('username')).is_superuser:

                    edit_update=article.objects.get(article_id=article_id)
                else:
                    edit_update = article.objects.get(article_id=article_id, uid=username)

                edit_item = request.POST.get('item')
                edit_lostdate = request.POST.get('lostdate')

                if edit_update:

                    edit_update.title=edit_title
                    edit_update.addr=edit_addr
                    edit_update.content=edit_content
                    edit_update.item = edit_item
                    edit_update.lostdate = edit_lostdate
                    edit_update.lost_type = add_losttype

                    edit_update.save()
                    return HttpResponseRedirect('../../index/content/?article_id={}'.format(article_id))
        # else:
        #     if request.GET.get('action') == 'del':
        #
        #         return HttpResponse('删除模块')


            # arti = article()
            # arti.title=edit_title
            # arti.addr=edit_addr
            # arti.content=edit_content
            # arti.uid=username
            # arti.save()


        return render(request,'release.html',{"username":username,'message':message,'user_mess':user_mess})
    else:
        return HttpResponseRedirect('/../../login')
