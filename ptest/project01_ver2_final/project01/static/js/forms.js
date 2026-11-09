document.addEventListener('submit', async function (event) {
    const form = event.target;
    if (!form.matches('form[data-ajax]')) {
        return;
    }

    event.preventDefault();
    if (form.dataset.submitting === 'true') {
        return;
    }

    const confirmation = form.dataset.confirm;
    if (confirmation && !window.confirm(confirmation)) {
        return;
    }

    const formData = new FormData(form);
    const submitButton = event.submitter;
    form.dataset.submitting = 'true';
    if (submitButton) {
        submitButton.disabled = true;
    }

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        });

        const contentType = response.headers.get('content-type') || '';
        const data = contentType.includes('application/json') ? await response.json() : {};
        if (!response.ok) {
            const message = response.status === 403
                ? '요청을 처리할 권한이 없거나 세션이 만료되었습니다.'
                : '요청을 처리하지 못했습니다. 입력값과 서버 상태를 확인해 주세요.';
            throw new Error(data.message || message);
        }

        if (!data.redirect_url) {
            throw new Error('서버 응답에서 이동할 주소를 찾지 못했습니다.');
        }
        if (form.action.includes('/member/login/')) {
            window.alert('로그인이 되었습니다.');
        }
        window.location.assign(data.redirect_url);
    } catch (error) {
        window.alert(error.message);
    } finally {
        delete form.dataset.submitting;
        if (submitButton) {
            submitButton.disabled = false;
        }
    }
});
