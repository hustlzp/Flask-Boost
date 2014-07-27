$(function () {
    /* 显示flash message */
    $(function () {
        setTimeout(showFlash, 200);
        setTimeout(hideFlash, 2000);
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
