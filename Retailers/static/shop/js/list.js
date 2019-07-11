// JavaScript Document

//商品规格选择
var checkkucun
var updatanum
var commodityid

updatanum=$("#text_box").val()
$(document).ready(function() {
	//优惠券
	$(".hot span").click(function() {
		$(".shopPromotion.gold .coupon").toggle();
	})




	//获得文本框对象
	var t = $("#text_box");
	//初始化数量为1,并失效减
	$('#min').attr('disabled', true);
	//数量增加操作
	$("#add").click(function() {
			t.val(parseInt(t.val()) + 1)
			if (parseInt(t.val()) != 1) {
				$('#min').attr('disabled', false);
			}
			if (parseInt(t.val())>= parseInt(checkkucun)) {
				t.val(parseInt(checkkucun))
				$('#add').attr('disabled', true);

			}
			updatanum=t.val()
             $('#LikBuy').attr('href','/order/pay/'+commodityid+'/'+parseInt(updatanum)+'/')

		})
		//数量减少操作
	$("#min").click(function() {
		t.val(parseInt(t.val()) - 1);
		if (parseInt(t.val()) == 1) {
			$('#min').attr('disabled', true);
		}
		updatanum=t.val()
        $('#LikBuy').attr('href','/order/pay/'+commodityid+'/'+parseInt(updatanum)+'/')

	})

})


$(function() {
	$(".theme-options").each(function() {

		var i = $(this);
		var p = i.find("ul>li");
		p.click(function() {
			if (!!$(this).hasClass("selected")) {
				$(this).removeClass("selected");

			} else {
				$(this).addClass("selected").siblings("li").removeClass("selected");

			}
            $('#add').attr('disabled', false);
			$('#min').attr('disabled', false);

			var fenliang = document.getElementById("fenliang").getElementsByClassName("selected");
			var kouwei = document.getElementById("kouwei").getElementsByClassName("selected");
			console.log(fenliang,kouwei);
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
					url:'/order/price',// 跳转到 action
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
						var total_price = data.total_price;
						var total_count = data.total_count;
						$("#cuxiaojia").text(total_price);
						// $("#cuxiaojia").val(total_price);
						$("#kucunliang").text(total_count);
						checkkucun = total_count
                        $("#text_box").val(1)
						commodityid = data.goods;
					 	var count = $("#text_box").val();
					 	updatanum=$("#text_box").val()
					 	// $('#LikBuy').click(function (ev) {
						// 	ev.preventDefault()
						//
						// })
						 $('#LikBuy').attr('href','/order/pay/'+commodityid+'/'+parseInt(updatanum)+'/')
						// $("#kucunliang").val(total_count);
				 }
				})
				}


		})

	})


})


//弹出规格选择
$(document).ready(function() {
	var $ww = $(window).width();
	if ($ww <1025) {
		$('.theme-login').click(function() {
			$(document.body).css("position", "fixed");
			$('.theme-popover-mask').show();
			$('.theme-popover').slideDown(200);

		})

		$('.theme-poptit .close,.btn-op .close').click(function() {
			$(document.body).css("position", "static");
			//					滚动条复位
			$('.theme-signin-left').scrollTop(0);

			$('.theme-popover-mask').hide();
			$('.theme-popover').slideUp(200);
		})

	}
})

//导航固定
$(document).ready(function() {
	var $ww = $(window).width();
	var dv = $('ul.am-tabs-nav.am-nav.am-nav-tabs'),
		st;

	if ($ww < 623) {

				var tp =$ww+363;
				$(window).scroll(function() {
					st = Math.max(document.body.scrollTop || document.documentElement.scrollTop);
					if (st >= tp) {
						if (dv.css('position') != 'fixed') dv.css({
							'position': 'fixed',
							top: 53,
							'z-index': 1000009
						});

					} else if (dv.css('position') != 'static') dv.css({
						'position': 'static'
					});
				});
				//滚动条复位（需要减去固定导航的高度）

				$('.introduceMain ul li').click(function() {
					sts = tp;
					$(document).scrollTop(sts);
				});
       } else {

		dv.attr('otop', dv.offset().top); //存储原来的距离顶部的距离
		var tp = parseInt(dv.attr('otop'))+36;
		$(window).scroll(function() {
			st = Math.max(document.body.scrollTop || document.documentElement.scrollTop);
			if (st >= tp) {

					if (dv.css('position') != 'fixed') dv.css({
						'position': 'fixed',
						top: 0,
						'z-index': 998
					});

				//滚动条复位
				$('.introduceMain ul li').click(function() {
					sts = tp-35;
					$(document).scrollTop(sts);
				});

			} else if (dv.css('position') != 'static') dv.css({
				'position': 'static'
			});
		});



	}
});


function add_cart() {
    console.log('+++++++++++++++++++')

	var commod = commodityid
	var num =updatanum
	var shopnum= $('#J_MiniCartNum').text()

	console.log(shopnum)
	console.log(updatanum,commodityid)
    $.ajax({
					url:'/order/add_cart',// 跳转到 action
					data:{
						'commodityid':commod,
					    'updatanum' :num,
						'shopnum':shopnum
					  },
					type:'post',
					dataType:'json',
				 success:function(data) {

						console.log("------");
						console.log(data);
						$('#J_MiniCartNum').text(data.num)

						 // $('#LikBuy').attr('href','/order/pay/'+commodityid+'/'+parseInt(updatanum)+'/')

				 }
				})

}