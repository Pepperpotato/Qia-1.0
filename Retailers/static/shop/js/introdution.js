$(window).load(function () {
    $('.flexslider').flexslider({
        animation: "slide",
        start: function (slider) {
            $('body').removeClass('loading');
        }
    });
    $(".kouwei").eq(0).addClass("selected");
    $(".fenliang").eq(0).addClass("selected");
});

$(document).ready(function () {
    $(".jqzoom").imagezoom();
    $("#thumblist li a").click(function () {
        $(this).parents("li").addClass("tb-selected").siblings().removeClass("tb-selected");
        $(".jqzoom").attr('src', $(this).find("img").attr("mid"));
        $(".jqzoom").attr('rel', $(this).find("img").attr("big"));
    });
});


function add_cart() {
		var fenliang = document.getElementById("fenliang").getElementsByClassName("selected");
		var kouwei = document.getElementById("kouwei").getElementsByClassName("selected");
		if (fenliang.length == 0 || kouwei.length == 0){
				$("#cuxiaojia").text("");
				$("#kucunliang").text("");
			}else{
				var fenliang_value = fenliang[0].innerText;
				var kouwei_value = kouwei[0].innerText;
				var goodid = $("#goods_id").val();
				var count = $("#text_box").val();

				console.log({"fenliang_value":fenliang_value,
						"kouwei_value":kouwei_value,
						"goodid":goodid,
						"count":count,
					  });
				$.ajax({
					url:'/order/add_cart',// 跳转到 action
					data:{"fenliang_value":fenliang_value,
						"kouwei_value":kouwei_value,
						"goodid":goodid,
						"count":count,
					  },
					type:'post',
					dataType:'json',
				 success:function(data) {

						console.log("------");
						console.log(data);
						// var total_price = data.total_price;
						// var total_count = data.total_count;
						// $("#cuxiaojia").text(total_price);
						// $("#cuxiaojia").val(total_price);
						// $("#kucunliang").text(total_count);
						// $("#kucunliang").val(total_count);
				 }
				})
				}
	}
// function price_change(obj) {



    // var fenliang = document.getElementById("fenliang").getElementsByClassName("selected");
    // var kouwei = document.getElementById("kouwei").getElementsByClassName("selected");
    // console.log(fenliang,kouwei);
    // if (fenliang.length == 0 || kouwei.length == 0){
    //     $("#cuxiaojia").text("");
    //     $("#kucunliang").text("");
    // }else{
    //     var fenliang_value = fenliang[0].innerText;
    //     var kouwei_value = kouwei[0].innerText;
    //     var goodid = $("#goods_id").val();
    //     var count = $("#text_box").val();
    //
    //     console.log({"fenliang_value":fenliang_value,
    //             "kouwei_value":kouwei_value,
    //             "goodid":goodid,
    //             "count":count,
    //           });
    //     $.ajax({
    //         url:'/order/price',// 跳转到 action
    //         data:{"fenliang_value":fenliang_value,
    //             "kouwei_value":kouwei_value,
    //             "goodid":goodid,
    //             "count":count,
    //           },
    //         type:'post',
    //         dataType:'json',
    //      success:function(data) {
    //
    //             console.log("------");
    //             console.log(data);
    //             var total_price = data.total_price;
    //             var total_count = data.total_count;
    //             $("#cuxiaojia").text(total_price);
    //             // $("#cuxiaojia").val(total_price);
    //             $("#kucunliang").text(total_count);
    //             // $("#kucunliang").val(total_count);
    //      }
    //     })
    //     }
// }

