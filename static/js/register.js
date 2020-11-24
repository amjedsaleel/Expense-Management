const usernameField = document.getElementById('usernameField');

usernameField.addEventListener('keyup', (e) => {
    const usernameValue = e.target.value;

    if (usernameValue.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({'username': usernameValue}),
            method: "POST",
        }).then(res => res.json()).then(data => {
            console.log('data', data)
        })
    }
});
