document.addEventListener("DOMContentLoaded", function () {
    const loginBtn = document.getElementById("loginBtn");
    if (loginBtn) {
        loginBtn.onclick = function () {
            window.location.href = "/login";
        };
    }

    const signupBtn = document.getElementById("signupBtn");
    if (signupBtn) {
        signupBtn.onclick = function () {
            window.location.href = "/signup";
        }
    }

    const goToPageBtn = document.getElementById("goToPageBtn");
    if (goToPageBtn) {
        goToPageBtn.onclick = function () {
            window.location.href = "/";
        };
    }

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.onclick = function(){
            window.location.href = "/logout"
        }
    }

    const profileBtn = document.getElementById("profileBtn")
    if (profileBtn) {
        profileBtn.onclick = function() {
            window.location.href = "/profile"
        }
    }

    const goBack = document.getElementById("goBack");
    if (goBack) {
        goBack.onclick = function () {
            window.location.href = "/dashboard";
        }
    }

    const deleteBtn = document.getElementById("deleteBtn")
    if (deleteBtn) {
        deleteBtn.onclick = function() {
            return confirm('Are you sure?');
        }
    }
});