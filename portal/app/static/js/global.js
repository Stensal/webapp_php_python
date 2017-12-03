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