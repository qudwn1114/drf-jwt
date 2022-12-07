const btn_login = document.getElementById("btn-login");
const id = document.getElementById('username');
const password = document.getElementById('password');


if(authentication()){
    location.reload();
}

btn_login.addEventListener("click", () => {
    const data =new FormData(document.getElementById("loginForm"));
    btn_login.disabled=true;
    if(!validation()){
        return false
    }
    $.ajax({
        type: "POST",
        url: "/api/login/",
        data: data,
        enctype: "multipart/form-data", //form data 설정
        processData: false, //프로세스 데이터 설정 : false 값을 해야 form data로 인식
        contentType: false, //헤더의 Content-Type을 설정 : false 값을 해야 form data로 인식
        success: function(data) {
            console.log(data.user);
            console.log(JSON.stringify(data));
            setCookie("access_token", data.jwt_token.access_token, tokenPayload(data.jwt_token.access_token).exp);
            setCookie("refresh_token_index_id", data.jwt_token.refresh_token_index_id, data.jwt_token.refresh_token_exp);
            location.href = '/system-manage/'
        },
        error: function(error) {
            alert("아이디 또는 비밀번호를 잘못 입력했습니다. \n입력하신 내용을 다시 확인해주세요.");
            btn_login.disabled=false;
        },
    });
});

//유효성 체크 함수
function validation(){
    if(id.value == ''){
        id.focus();
        return false;
    }
    if(password.value == ''){
        password.focus();
        return false;
    }
    return true;
}

function enterkey() {
    if (window.event.keyCode == 13) {
        btn_login.click()
    }
}

