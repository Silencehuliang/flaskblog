layui.use(['jquery', 'flow'], function () {
    var $ = layui.jquery;
    article.Init($);
    var flow = layui.flow;
    flow.load({
        elem: '#LAY_bloglist' //指定列表容器
        , done: function (page, next) {
            var lis = [];
            var currentCid = 1;
            var cur_page = 1;
            var params = {
                "cid": currentCid,
                "page": page,
                'per_page': 10
            }
            //以jQuery的Ajax请求为例，请求下一页数据（注意：page是从2开始返回）
            $.get('/article/post_list?', params, function (res) {
                if (res.errno == "0") {
                    if (cur_page == 1) {
                        $(".bloglist").html("")
                    }
                    for (var i = 0; i < res.data.post_dict_li.length; i++) {
                        var post = res.data.post_dict_li[i]
                        var content = '<section class="article-item zoomIn article">\n'

                        content += '<h5 class="title"><a href="read.html">' + post.title + '</a></h5>'
                        content += '<div class="time"><span class="day">21</span><span class="month fs-18">1<span class="fs-14">月</span></span><span class="year fs-18 ml10">2019</span></div>'
                        content += '<a href="/post/' + post.id + '" ">' + post.digest + '</a>'
                        content += '<div class="content"><a href="read.html" class="cover img-light"><img src="' + post.index_image_url + '"></a>' + post.digest + '</div><div class="read-more"><a href="read.html" class="fc-black f-fwb">继续阅读</a></div>'
                        content += ' <aside class="f-oh footer"><div class="f-fl tags"><span class="fa fa-tags fs-16"></span> <a class="tag">' + post.category + '</a></div>'
                        content += '<div class="f-fr"><span class="read"><i class="fa fa-eye fs-16"></i><i class="num">57</i></span><span class="ml20"><i class="fa fa-comments fs-16"></i><a href="javascript:void(0)" class="num fc-grey">1</a></span>'
                        content += '</div></aside></section>'
                        $(".bloglist").append(content)
                    }
                } else {
                    // 请求失败
                    alert(res.errmsg)
                }

                //执行下一页渲染，第二参数为：满足“加载更多”的条件，即后面仍有分页
                //pages为Ajax返回的总页数，只有当前页小于总页数的情况下，才会继续出现加载更多
                next(content, page < res.data.pages);
            });


        }
    })
    ;
})
;

var article = {};
article.Init = function ($) {
    var slider = 0;
    blogtype();
    //类别导航开关点击事件
    $('.category-toggle').click(function (e) {
        e.stopPropagation();    //阻止事件冒泡
        categroyIn();
    });
    //类别导航点击事件，用来关闭类别导航
    $('.article-category').click(function () {
        categoryOut();
    });
    //遮罩点击事件
    $('.blog-mask').click(function () {
        categoryOut();
    });
    $('.f-qq').on('click', function () {
        window.open('http://connect.qq.com/widget/shareqq/index.html?url=' + $(this).attr("href") + '&sharesource=qzone&title=' + $(this).attr("title") + '&pics=' + $(this).attr("cover") + '&summary=' + $(this).attr("desc") + '&desc=你的分享简述' + $(this).attr("desc"));
    });
    $("body").delegate(".fa-times", "click", function () {
        $(".search-result").hide().empty();
        $("#searchtxt").val("");
        $(".search-icon i").removeClass("fa-times").addClass("fa-search");
    });

    //显示类别导航
    function categroyIn() {
        $('.category-toggle').addClass('layui-hide');
        $('.article-category').unbind('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend');
        $('.blog-mask').unbind('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend');
        $('.blog-mask').removeClass('maskOut').addClass('maskIn');
        $('.blog-mask').removeClass('layui-hide').addClass('layui-show');
        $('.article-category').removeClass('categoryOut').addClass('categoryIn');
        $('.article-category').addClass('layui-show');
    }

    //隐藏类别导航
    function categoryOut() {
        $('.blog-mask').on('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
            $('.blog-mask').addClass('layui-hide');
        });
        $('.article-category').on('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
            $('.article-category').removeClass('layui-show');
            $('.category-toggle').removeClass('layui-hide');
        });
        $('.blog-mask').removeClass('maskIn').addClass('maskOut').removeClass('layui-show');
        $('.article-category').removeClass('categoryIn').addClass('categoryOut');
    }

    function blogtype() {
        $('#category li').hover(function () {
            $(this).addClass('current');
            var num = $(this).attr('data-index');
            $('.slider').css({'top': ((parseInt(num) - 1) * 40) + 'px'});
        }, function () {
            $(this).removeClass('current');
            $('.slider').css({'top': slider});
        });
        $(window).scroll(function (event) {
            var winPos = $(window).scrollTop();
            if (winPos > 750)
                $('#categoryandsearch').addClass('fixed');
            else
                $('#categoryandsearch').removeClass('fixed');
        });
    };
};

