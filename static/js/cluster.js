/**
 * Created by Administrator on 2018/9/10/010.
 */

$(function () {

    // silider Toggle

    $("li.aside-list-li>a").each(function(){
        if ($($(this))[0].href == String(window.location)){
            $(this).parent(".aside-list-li").addClass('active').attr('href','javascript:void(0);').siblings().removeClass("active");
        }
    });

    // create Pods
    $('.create-btns > .create_pods').on('click', function () {

    })


});