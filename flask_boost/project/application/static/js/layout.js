(function () {
    "use strict";

    // Add CSRF token header for Ajax request
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", g.csrfToken);
            }
        }
    });

    // Flash message
    setTimeout(showFlash, 200);
    setTimeout(hideFlash, 2000);

    /**
     * Show flash message.
     */
    function showFlash() {
        $('.flash-message').slideDown('fast');
    }

    /**
     * Hide flash message.
     */
    function hideFlash() {
        $('.flash-message').slideUp('fast');
    }
})();
