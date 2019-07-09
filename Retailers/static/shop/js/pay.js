

function mycommit () {
    var receiver = $('#user-name').val();
    var phone = $('#user-phone').val();
    var province = $('#cmbProvince').val();
    var city = $('#cmbCity').val();
    var area = $('#cmbArea').val();
    var intro = $('#user-intro').val();
    console.log(receiver,phone,province,city,area,intro);
    $.ajax({
        url: '/order/addre/',// 跳转到 action
        data: {
            'receiver':receiver,
            'phone':phone,
            'province':province,
            'city':city,
            'area':area,
            'intro':intro
        },
        type: 'post',
        dataType: 'json',
        success: function (data) {
            console.log(data)
        }
    })
}