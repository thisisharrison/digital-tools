document.addEventListener('DOMContentLoaded', () => {

    // environment selection
    const form = document.querySelector('form')

    const formSubmit = document.getElementById('formSubmit')
    form.onsubmit = function envCheck(evt) {
        const prodEnv = document.getElementById('prodEnv').checked
        const stagEnv = document.getElementById('stagEnv').checked
        if (stagEnv) {
            evt.preventDefault();
            $('#stagEnvInfo').modal('show')
        };
    }
    // enter staging information
    const readyButton = document.getElementById('readyButton')
    readyButton.onclick = function () {
        const email = document.getElementById('email').value
        const password = document.getElementById('password').value
        const date = document.getElementById('date').value
        let stageReady =
            (email.length != 0 && password.length != 0 && date.length != 0)
        if (stageReady) {
            form.submit();
            return true;
        } else {
            alert("Enter staging information")
        }
    }
});