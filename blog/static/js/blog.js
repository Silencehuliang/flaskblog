/**

 @Name：layui.blog 闲言轻博客模块
 @Author：徐志文
 @License：MIT
 @Site：http://www.layui.com/template/xianyan/

 */

layui.define(['element', 'form', 'laypage', 'jquery', 'laytpl'], function (exports) {
    var element = layui.element
        , form = layui.form
        , laypage = layui.laypage
        , $ = layui.jquery
        , laytpl = layui.laytpl;
    var currentCid = 1;

    updateNewsData()

    // 首页分类切换
    $('.layui-nav li').click(function () {
        // 取到指定分类的cid
        var clickCid = $(this).attr('data-cid')

        // 如果点击的分类与当前分类不一致
        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            updateNewsData()
        }
    })

    //statr 分页

    laypage.render({
        elem: 'item-btn' //注意，这里的 test1 是 ID，不用加 # 号
        // , count: 50 //数据总数，从服务端得到
        , theme: '#1e9fff'
        , jump: function (obj, first) {
            updateNewsData()
        }
    });

    // end 分頁


    // start 导航显示隐藏

    $("#mobile-nav").on('click', function () {
        $("#pop-nav").toggle();
    });

    // end 导航显示隐藏


    //start 评论的特效

    (function ($) {
        $.extend({
            tipsBox: function (options) {
                options = $.extend({
                    obj: null,  //jq对象，要在那个html标签上显示
                    str: "+1",  //字符串，要显示的内容;也可以传一段html，如: "<b style='font-family:Microsoft YaHei;'>+1</b>"
                    startSize: "12px",  //动画开始的文字大小
                    endSize: "30px",    //动画结束的文字大小
                    interval: 600,  //动画时间间隔
                    color: "red",    //文字颜色
                    callback: function () {
                    }    //回调函数
                }, options);

                $("body").append("<span class='num'>" + options.str + "</span>");

                var box = $(".num");
                var left = options.obj.offset().left + options.obj.width() / 2;
                var top = options.obj.offset().top - 10;
                box.css({
                    "position": "absolute",
                    "left": left + "px",
                    "top": top + "px",
                    "z-index": 9999,
                    "font-size": options.startSize,
                    "line-height": options.endSize,
                    "color": options.color
                });
                box.animate({
                    "font-size": options.endSize,
                    "opacity": "0",
                    "top": top - parseInt(options.endSize) + "px"
                }, options.interval, function () {
                    box.remove();
                    options.callback();
                });
            }
        });
    })($);

    function niceIn(prop) {
        prop.find('i').addClass('niceIn');
        setTimeout(function () {
            prop.find('i').removeClass('niceIn');
        }, 1000);
    }

    $(function () {
        $(".like").on('click', function () {

            if (!($(this).hasClass("layblog-this"))) {
                this.text = '已赞';
                $(this).addClass('layblog-this');
                $.tipsBox({
                    obj: $(this),
                    str: "+1",
                    callback: function () {
                    }
                });
                niceIn($(this));
                layer.msg('点赞成功', {
                    icon: 6
                    , time: 1000
                })
            }
        });
    });

    //end 评论的特效


    // start点赞图标变身
    $('#LAY-msg-box').on('click', '.info-img', function () {
        $(this).addClass('layblog-this');
    })

    // end点赞图标变身

    //end 提交
    $('#item-btn').on('click', function () {
        var elemCont = $('#LAY-msg-content')
            , content = elemCont.val();
        if (content.replace(/\s/g, '') == "") {
            layer.msg('请先输入留言');
            return elemCont.focus();
        }

        var view = $('#LAY-msg-tpl').html()

            //模拟数据
            , data = {
                username: '闲心'
                , avatar: '../res/static/images/info-img.png'
                , praise: 0
                , content: content
            };

        //模板渲染
        laytpl(view).render(data, function (html) {
            $('#LAY-msg-box').prepend(html);
            elemCont.val('');
            layer.msg('留言成功', {
                icon: 1
            })
        });

    })

    // start  图片遮罩
    var layerphotos = document.getElementsByClassName('layer-photos-demo');
    for (var i = 1; i <= layerphotos.length; i++) {
        layer.photos({
            photos: ".layer-photos-demo" + i + ""
            , anim: 0
        });
    }

    // end 图片遮罩


    function updateNewsData() {
        var params = {
            "page": 1,
            "cid": currentCid,
            'per_page': 50
        }
        $.get("/post_list", params, function (resp) {
                if (resp) {
                    laypage.render({
                        elem: 'item-btn' //注意，这里的 test1 是 ID，不用加 # 号
                        , count: resp.data.total_page//数据总数，从服务端得到
                        , curr: resp.data.current_page
                        , theme: '#1e9fff'

                    });
                    // 先清空原有数据
                    $(".item-list").html('')

                    // 显示数据
                    for (var i = 0; i < resp.data.post_dict_list.length; i++) {
                        var post = resp.data.post_dict_list[i]
                        console.log(post.id)

                        var content = '<div class="item"><div class="item-box">'
                        content += '<h3><a href="/details/' + post.id + '">' + post.title + '</a></h3>'
                        content += '<h5>发布于：<span>' + post.create_time + '</span></h5>'
                        content += '<p><a href="/details/' + post.id + '"</a>' + post.digest + '</p>'
                        content += '<img src="' + post.index_image_url + '" alt="">' + '<a href="/details/' + post.id + '"'
                        content += '</div><div class="comment count"><a href="details/'+post.id+'#comment">评论</a><a href="javascript:;" class="like">点赞</a></div></div>'
                        $(".item-list").append(content)
                    }
                } else {
                    // 请求失败
                    alert(resp.errmsg)
                }
            }
        )
    }

    //输出test接口
    exports('blog', {});
});  
