$(function () {
    /* 显示flash message */
    $(function () {
        setTimeout(showFlash, 200);
        setTimeout(hideFlash, 2000);
    });

    if ($("#nav-dialogs a span").text() !== "") {
        var timerArr = $.blinkTitle.show();
    }

    setTimeout(function () {
        $.blinkTitle.clear(timerArr);
    }, 6000);

    /* 省市联动 */
    var provinces = locals.provinces;
    var province = null;
    var provinceId = locals.provinceId;
    var cityId = locals.cityId;
    var provinceSelect = $('#province-id');
    var citySelect = $('#city-id');

    // 填充省
    $.each(provinces, function (index, p) {
        provinceSelect.append("<option value=" + p.id + ">" + p.name + "</option>");
    });
    provinceSelect.val(provinceId);

    // 省市联动
    provinceSelect.change(function () {
        provinceId = parseInt($(this).val());
        province = _.findWhere(provinces, {id: provinceId});
        citySelect.empty();
        $.each(province.cities, function (index, c) {
            citySelect.append("<option value=" + c.id + ">" + c.name + "</option>");
        });
    });

    // 填充市
    province = _.findWhere(provinces, {id: provinceId});
    $.each(province.cities, function (index, c) {
        citySelect.append("<option value=" + c.id + ">" + c.name + "</option>");
    });
    citySelect.val(cityId);

    // 切换城市
    $('.btn-switch-city').click(function () {
        $(".region-box").toggle();
        $(".search-knowledge-form").toggle();
    });

    $(".btn-submit-switch").click(function () {
        cityId = citySelect.val();
        window.location = '/switch_city/' + cityId;
    });

    /* 每隔10s查询新私信数目 */
    function updateMsg() {
        $.getJSON(locals.checkNewMessagesUrl, {
            csrf_token: locals.csrf
        }, function (result) {
            if (result.count) {
                $("#nav-dialogs .label").text(result.count);
            }
        });
    }

    setInterval(updateMsg, 10000);

    // 切换一级子菜单
    $('.dropdown-toggle').click(function () {
        return false;
    });
    $('li.dropdown').hover(function () {
        $(this).addClass('open');
    }, function () {
        $(this).removeClass('open');
    });

    // 切换二级子菜单
    $('.course-type').hover(function () {
        $(this).children('.courses-menu').show();
    }, function () {
        $(this).children('.courses-menu').hide();
    });
});

/**
 * 显示flash消息
 */
function showFlash() {
    $('.flash-message').slideDown('fast');
}

/**
 * 隐藏flash消息
 */
function hideFlash() {
    $('.flash-message').slideUp('fast');
}

/**
 * 闪烁标题
 * jQuery.blinkTitle
 */
(function ($) {
    $.extend({
        /**
         * 调用方法
         * var timerArr = $.blinkTitle.show();
         * $.blinkTitle.clear(timerArr);
         */
        blinkTitle: {
            show: function () {	//有新消息时在title处闪烁提示
                var step = 0, _title = document.title;

                var timer = setInterval(function () {
                    step++;
                    if (step == 3) {
                        step = 1
                    }
                    if (step == 1) {
                        document.title = '【　　　】' + _title
                    }
                    if (step == 2) {
                        document.title = '【新消息】' + _title
                    }
                }, 500);

                return [timer, _title];
            },

            /**
             * @param timerArr[0], timer标记
             * @param timerArr[1], 初始的title文本内容
             */
            clear: function (timerArr) {	//去除闪烁提示，恢复初始title文本
                if (timerArr) {
                    clearInterval(timerArr[0]);
                    document.title = timerArr[1];
                }
            }
        }
    });
})(jQuery);