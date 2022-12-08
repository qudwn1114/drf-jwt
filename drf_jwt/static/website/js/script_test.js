const btn_submit = document.getElementById("btn-submit");
const email = document.getElementById("email");


btn_submit.addEventListener("click", () => {
    if (!confirm("전송하시겠습니까?") || !validation()) {
        return;
    }
    btn_submit.disabled=true;
    btn_submit.innerHTML='<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
    let access_token = getCookie("access_token");
    $.ajax({
        type: "POST",
        url: "/api/test/",
        headers: {
            'Authorization': `Bearer ${access_token}`,
        },
        data: {
            "email" : document.getElementById("email").value
        },
        datatype: "JSON",
        success: function(data) {
            alert("전송되었습니다!");
            location.reload();
        },
        error: function(error) {
            //로그인이 필요한 경우.
            btn_submit.disabled=false;
            btn_submit.innerHTML='전송';
            if(error.status == 401){
                alert("로그인을 해주세요.");
                return;
            }
            if(error.status == 500){
                alert("서버에러..");
                return;
            }
            alert(error.status + JSON.stringify(error.responseJSON));
        },
    });
});


//유효성 체크 함수
function validation(){
    if(email.value == ''){
        email.focus();
        return false;
    }
    return true;
}