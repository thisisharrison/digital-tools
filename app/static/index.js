document.addEventListener('DOMContentLoaded', () => {

    // Navbar
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
    
    $('#navbarText .navbar-nav a').on('click', function () {
        // $('#navbarText .navbar-nav').find('li.active').removeClass('active');
        $(this).parent('li').addClass('active');
    });

    const taskType = window.location.pathname

});