mdc.ripple.MDCRipple.attachTo(document.querySelector('.foo-button'));

function p() {
    var q = document.getElementById('audio');
    var t = document.getElementById('lo');
    var fr = document.getElementById('fr');
    if (q.paused) {
        q.play();
        t.style.display = "block";
        fr.style.display = "none";
        t.focus();
        fr.focus();
        return false;
    } else
        q.pause();
    t.style.display = "none";
    fr.style.display = "block";
    fr.focus();
    t.focus();
    return false;
}


function o() {
    var playPromise = audio.play();

    if (playPromise !== undefined) {
        playPromise.then(_ => {
                // Automatic playback started!
                // Show playing UI.
            })
            .catch(error => {
                // Auto-play was prevented
                // Show paused UI.
            });
    }
}