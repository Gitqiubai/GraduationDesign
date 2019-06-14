/*
* @Author: wuna
* @Date:   2018-07-09 15:13:30
* @Last Modified by:   wuna
* @Last Modified time: 2018-07-09 16:39:05
*/
var pagination = pagination || {};
(function(){
    function Pagination(){
    }
    Pagination.prototype = {
        render: function(obj){
            /*显示分页器的容器元素id*/
            this._wrapid = '#'+obj.wrapid;
            this._total = obj.total;
            this._pagesize = obj.pagesize;
            this._currentPage = obj.currentPage;
            this._titleid = obj.titleid;

            /*页码改变的回调函数*/
            this._cb = obj.onPagechange;
            /*设置页码超过多少个时，显示省略号*/
            if(obj.btnCount<5){
                obj.btnCount = 5;
            }else if(obj.btnCount%2==0){
                //非奇数
                obj.btnCount = obj.btnCount+1;
            }
            this._btnsValue = obj.btnCount?obj.btnCount:7;
            /*页码过多，左右都存在省略号时，当前点击页码左右两边的页码个数*/
            this._halfbtns = parseInt((this._btnsValue-3)/2);
            /*显示的总页面数*/
            this._btnNum = obj.total/obj.pagesize>parseInt(obj.total/obj.pagesize)?parseInt(obj.total/obj.pagesize)+1:parseInt(obj.total/obj.pagesize);   
        },
        bindEvent: function(){
            var that = this;
            /*页码点击*/
            $(that._wrapid).on('click','.pagenum',function(){
                that._currentPage = parseInt($(this).text());
                that._cb(that._currentPage);
                isshowMore.call(that);
                $(location).attr('href', '/index/content/?article_id='+that._titleid+'&comment_page='+that._currentPage);
            });

            /*上一页*/
            $(that._wrapid).on('click','#pagination-prev',function(){

                if($(this).hasClass('pagination-disabled')){
                    return;
                }
                that._currentPage--;
                $('#pagination-next').hasClass('pagination-disabled')&&$('#pagination-next').removeClass('pagination-disabled');
                if(that._currentPage==1){
                    $('#pagination-prev').addClass('pagination-disabled');
                }else{
                    $('#pagination-prev').removeClass('pagination-disabled');
                }
                that._cb(that._currentPage);
                isshowMore.call(that);

                $(location).attr('href', '/index/content/?article_id='+that._titleid+'&comment_page='+that._currentPage);
            });

            /*下一页*/
            $(that._wrapid).on('click','#pagination-next',function(){

                if($(this).hasClass('pagination-disabled')){
                    return;
                }
                that._currentPage++;
                $('#pagination-prev').hasClass('pagination-disabled')&&$('#pagination-prev').removeClass('pagination-disabled');
                if(that._currentPage==that._btnNum){
                    $('#pagination-next').addClass('pagination-disabled');
                }else{
                    $('#pagination-next').removeClass('pagination-disabled')
                }
                that._cb(that._currentPage);
                isshowMore.call(that);

                $(location).attr('href', '/index/content/?article_id='+that._titleid+'&comment_page='+that._currentPage);



            });
            isshowMore.call(this);

            /*判断省略符位置*/
            function isshowMore(){
                if(this._btnNum<=this._btnsValue){
                    // console.log('不显示');
                    creatBtns.call(this,'none')
                }else{
                    if(this._currentPage<=(this._btnsValue-1-this._halfbtns)){
                        //只显示后省略
                        creatBtns.call(this,'after');
                    }else if(this._currentPage>=this._btnNum-1-this._halfbtns){
                        //只显示前省略
                        creatBtns.call(this,'before')
                    }else{
                        //前后省略都显示
                        creatBtns.call(this,'all')
                    }
                }
            }

            /*创建页码按钮标签*/
            function creatBtns(ismorePosition){
                var html = '';
                var ismore = '<li class="pagination-ellipsis">...</li>';
                var firstbtn = '<li class="pagenum pagination-btn" data-num="1">1</li>';
                var lastbtn = '<li class="pagenum pagination-btn" data-num='+this._btnNum+'>'+this._btnNum+'</li>';
                var prevbtn = '<span class="pagination-btn" id="pagination-prev"><</span>';
                var nextbtn = '<span class="pagination-btn" id="pagination-next">></span>'
                if(this._currentPage == 1){
                    firstbtn = '<li class="pagenum pagination-btn pagination-current" data-num="1">1</li>';
                    prevbtn = '<span class="pagination-btn pagination-disabled" id="pagination-prev"><</span>'
                }
                if(this._currentPage == this._btnNum){
                    lastbtn = '<li class="pagenum pagination-btn pagination-current" data-num='+this._btnNum+'>'+this._btnNum+'</li>';
                    nextbtn = '<span class="pagination-btn pagination-disabled" id="pagination-next">></span>'
                }
                
                if(ismorePosition == 'none'){
                    for(var i = 1; i <= this._btnNum; i++){
                        if(i == this._currentPage){
                            html+= '<li class="pagenum pagination-btn pagination-current" data-num='+i+'>'+i+'</li>';
                        }else{
                            html += '<li class="pagenum pagination-btn" data-num='+i+'>'+i+'</li>';
                        }
                    }
                }
                if(ismorePosition=="after"){
                    // console.log('省略在后面');
                    for(var i = 1; i <= this._btnsValue-1; i++){
                        if(i == this._currentPage){
                            html += '<li class="pagenum pagination-btn pagination-current" data-num='+i+'>'+i+'</li>';
                        }else{
                            html += '<li class="pagenum pagination-btn" data-num='+i+'>'+i+'</li>';
                        }
                    }
                    html = html + ismore + lastbtn;
                }
                
                if(ismorePosition=="before"){
                    // console.log('省略在前面');
                    html = html + firstbtn + ismore;
                    for(var i=this._btnNum-(this._btnsValue-2);i<=this._btnNum;i++){
                        if(i == this._currentPage){
                            html+='<li class="pagenum pagination-btn pagination-current" data-num='+i+'>'+i+'</li>';
                        }else{
                            html+='<li class="pagenum pagination-btn" data-num='+i+'>'+i+'</li>';
                        }
                    }
                }
                
                if(ismorePosition=="all"){
                    // console.log('省略前后都有');
                    var halfnum = parseInt((this._btnsValue-3)/2);
                    html += firstbtn + ismore;
                    for(var i = (this._currentPage-halfnum);i<=this._currentPage+halfnum+((this._btnsValue-3)%2);i++){
                        if(i == this._currentPage){
                            html += '<li class="pagenum pagination-btn pagination-current" data-num='+i+'>'+i+'</li>'
                        }else{
                            html += '<li class="pagenum pagination-btn" data-num='+i+'>'+i+'</li>'
                        }
                    }
                    html+=ismore+lastbtn;
                }
                $(this._wrapid).html(prevbtn+'<ul class="pagination-wrap">'+html+'</ul>'+nextbtn);
            }
        },
        init:function(paginationObj){
            this.render(paginationObj);
            this.bindEvent();
        }
    }

    pagination.init = function(paginationObj){
        /*参数：wrapid,total,pagesize,currentPage,onPagechange[,btnCount]*/
        return new Pagination().init(paginationObj)
    }
})()