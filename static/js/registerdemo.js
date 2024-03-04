function bindEmailCaptchaClick(){
//在整个网页全部加载完成后执行该函数；
//$(function(){})
$(function(){
    $("#captcha-btn").click(function(event){
        var $this=$(this);//$this代表按钮的jquery对象
        //阻止默认的事件
        event.preventDefault();
        //$("#exampleInputEmail1")
        var email =$("input[name='email']").val();//val函数可以获取用户输入的值
        $.ajax({
            //域名，默认http://127.0.0.1:500
            url:"/auth/captcha/email?email="+email,
            methods:'GET',
            success:function(result){
                var code=result['code'];
                if(code == 200){
                    var countdown=5;//倒计时
                    //开始倒计时之前，就取消按钮的点击事件
                    $this.off("click");
                    var timer=setInterval(function(){ 
                        $this.text(countdown);
                        countdown-=1;
                        if(countdown<=0){
                            //清掉定时器
                            clearInterval(timer);
                            //将按钮的文字重新修改回来
                            $this.text("获取验证码");
                             //倒计时结束，重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    },1000);//毫秒级
                    //alert("邮箱验证发送成功");
                }else{
                    alert(result['message']);
                }

            },
            fail:function(error){
                console.log(error);
            }
        })
    });
});
}

//整个网页都加载完毕后再执行的
$(function(){
    bindEmailCaptchaClick();
});