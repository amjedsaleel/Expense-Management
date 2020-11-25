const usernameField = document.getElementById('usernameField');
const emailField = document.getElementById('emailField');
const passwordField = document.getElementById('passwordField');
const invalidPassword = document.getElementById('password-invalid')
const feedBackFiled = document.querySelector('.invalid-feedback');
const usernameValidFeedBAck = document.querySelector('.username-valid-feedback');
const emailFeedBackArea = document.querySelector('.emailFeedBackArea');
const emailValidFeedBack = document.querySelector('.mail-valid-feedback');
const showPasswordToggle = document.getElementById('show-password-toggle')

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "SHOW") {
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener('click', handleToggleInput)


usernameField.addEventListener('keyup', (e) => {
    const usernameValue = e.target.value;

    usernameField.classList.remove("is-valid");
    usernameField.classList.remove("is-invalid");

    usernameValidFeedBAck.style.display = "none";
    feedBackFiled.style.display = "none";

    if (usernameValue.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({'username': usernameValue}),
            method: "POST",
        }).then(res => res.json()).then(data => {
            // console.log('data', data)
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                feedBackFiled.style.display = "block";
                feedBackFiled.innerHTML = `<p>${data.username_error} </p>`
            } else if (data.username_valid === true) {
                console.log('Username is True')
                usernameField.classList.add("is-valid");
                usernameValidFeedBAck.style.display = "block";
            } else {
                console('true')
            }
        })
    }
});


// Function for validating email
emailField.addEventListener('keyup', (e) => {
    const emailValue = e.target.value;

    emailField.classList.remove("is-valid");
    emailField.classList.remove("is-invalid");

    emailFeedBackArea.style.display = "none";
    emailValidFeedBack.style.display = "none";

    if (emailValue.length > 0) {
        fetch('/authentication/validate-email', {
            body: JSON.stringify({'email': emailValue}),
            method: 'POST',
        }).then(res => res.json()).then(data => {
            // console.log(data);
            if (data.email_error) {
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = `<p>${data.email_error} </p>`
            } else if (data.email_valid === true) {
                console.log("Email is True");
                emailField.classList.add("is-valid");
                emailValidFeedBack.style.display = "block";
            } else {
                console.log('ok')
            }
        })
    }
})

// function for validation password length
passwordField.addEventListener('keyup', (e) => {
    const password = e.target.value;

    passwordField.classList.remove("is-valid")
    passwordField.classList.remove("is-invalid")

    invalidPassword.innerText = '';
    invalidPassword.style.display = 'none';

    if (password.length >= 6) {
        passwordField.classList.add("is-valid")
    } else {
        passwordField.classList.add("is-invalid")
        invalidPassword.style.display = 'block';
        invalidPassword.innerText = 'Password must be 6 or more characters'
    }
})

