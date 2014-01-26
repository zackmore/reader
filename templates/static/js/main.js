$(function(){
    // Sidebar show and hide
    $('.sidebar-btn').on('click', function(e){
        e.preventDefault();
        $('.sidebar-btn').toggleClass('show');
        $('#sidebar').toggleClass('show');
        $('#nav-overall').toggleClass('show');
    });
    $('#nav-overall').on('click', function(){
        $(this).removeClass('show');
        $('.sidebar-btn, #sidebar').removeClass('show');
    });
    $('body').swipe({
        swipeLeft: function(){
            $('#sidebar, #nav-overall, .sidebar-btn').removeClass('show');
        },
        swipeRight: function(){
            $('#sidebar, #nav-overall, .sidebar-btn').addClass('show');
        }
    });

});
