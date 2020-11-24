const usernameField = document.getElementById('usernameField');
const feedBackFiled = document.querySelector('.invalid-feedback')
usernameField.addEventListener('keyup', (e) => {
    const usernameValue = e.target.value;

     usernameField.classList.remove("is-invalid");
     feedBackFiled.style.display = "none";

    if (usernameValue.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({'username': usernameValue}),
            method: "POST",
        }).then(res => res.json()).then(data => {
            console.log('data', data)
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                feedBackFiled.style.display = "block";
                feedBackFiled.innerHTML = `<p>${data.username_error} </p>`
            }
        })
    }
});
