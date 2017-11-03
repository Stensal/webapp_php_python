(function (window, document) {
    var menu = document.getElementById('menu'),
        WINDOW_CHANGE_EVENT = ('onorientationchange' in window) ? 'orientationchange':'resize';

    function toggleHorizontal() {
        [].forEach.call(
            document.getElementById('menu').querySelectorAll('.menu-can-transform'),
            function(el){
                el.classList.toggle('pure-menu-horizontal');
            }
        );
    };

    function toggleMenu() {
        // set timeout so that the panel has a chance to roll up
        // before the menu switches states
        if (menu.classList.contains('open')) {
            setTimeout(toggleHorizontal, 500);
        }
        else {
            toggleHorizontal();
        }
        menu.classList.toggle('open');
        document.getElementById('toggle').classList.toggle('x');
    };

    function closeMenu() {
        if (menu.classList.contains('open')) {
            toggleMenu();
        }
    }

    document.getElementById('toggle').addEventListener('click', function (e) {
        toggleMenu();
        e.preventDefault();
    });

    window.addEventListener(WINDOW_CHANGE_EVENT, closeMenu);
})(this, this.document);

$(function(){
            var top1 = $(".issues-labels").offset().top;
            var top1 = $(".issues-labels").offset().top;
            $(window).scroll(function(){

            　　　　　　var  win_top=$(this).scrollTop();

            　　　　　　var  top=$(".issues-labels").offset().top;

            　　　　　　if(win_top>=top){

            　　　　　　　　$(".issues-labels").addClass("issues-fixed");

            　　　　　　}//如果此处用else判断来remove fixed这个类的话是不行的，因为当加上这个类的时候，win_top与top值就一直相等了；只有与以前的距离做比较才能实现滑上去的时候能回到原来的位置。

            　　　　　　if(win_top<top1){

            　　　　　　　　$(".issues-labels").removeClass("issues-fixed");

            　　　　　　}

            　　　　});

            $('#tab-collapse').click(function(){
                $(".label-list").toggleClass('show');
            });
            
        });