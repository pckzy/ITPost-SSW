document.addEventListener('DOMContentLoaded', function () {
    const imgSelect = document.getElementById(imageId);
    const preview = document.getElementById('preview')
    imgSelect.addEventListener('change', () => {
        const [file] = imgSelect.files
        if (file) {
            preview.src = URL.createObjectURL(file)
        } else {
            preview.src = `/media/profile/profile.png`;
        }
    })
});

function approvePost(btnElement) {
    const postId = btnElement.getAttribute('data-post-id')
    const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
    const headers = {};
    if (csrf) headers['X-CSRFToken'] = csrf.value;

    fetch(`/post/${postId}/approve/`, { method: 'PUT', headers: headers })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                const el = document.getElementById(`post-${postId}`);
                if (el) {
                    el.style.transition = 'opacity 400ms ease, transform 400ms ease, height 400ms ease, margin 400ms ease, padding 400ms ease';
                    el.style.opacity = '0';
                    el.style.transform = 'translateY(-12px)';
                    el.style.pointerEvents = 'none';

                    el.style.height = el.offsetHeight + 'px';

                    void el.offsetHeight;
                    el.style.height = '0px';
                    el.style.marginBottom = '0px';
                    el.style.paddingTop = '0px';
                    el.style.paddingBottom = '0px';
                    setTimeout(function () { el.remove(); }, 450);
                }
            } else {
                alert('Approve failed: ' + (data.error || 'unknown'));
            }
        }).catch(err => {
            alert('Error approve post');
            console.error(err);
        });
}

function rejectPost(btnElement) {
    const postId = btnElement.getAttribute('data-post-id')
    const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
    const headers = {};
    if (csrf) headers['X-CSRFToken'] = csrf.value;

    fetch(`/post/${postId}/reject/`, { method: 'PUT', headers: headers })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                const el = document.getElementById(`post-${postId}`);
                if (el) {
                    el.style.transition = 'opacity 400ms ease, transform 400ms ease, height 400ms ease, margin 400ms ease, padding 400ms ease';
                    el.style.opacity = '0';
                    el.style.transform = 'translateY(-12px)';
                    el.style.pointerEvents = 'none';

                    el.style.height = el.offsetHeight + 'px';

                    void el.offsetHeight;
                    el.style.height = '0px';
                    el.style.marginBottom = '0px';
                    el.style.paddingTop = '0px';
                    el.style.paddingBottom = '0px';
                    setTimeout(function () { el.remove(); }, 450);
                }
            } else {
                alert('Reject failed: ' + (data.error || 'unknown'));
            }
        }).catch(err => {
            alert('Error reject post');
            console.error(err);
        });
}