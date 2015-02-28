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
