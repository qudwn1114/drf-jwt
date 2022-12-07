const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function authentication(){
    let access_token = getCookie("access_token");
    let refresh_token_index_id = getCookie("refresh_token_index_id");
    if(boolCheckCookie("access_token")){
        // access token이 유효 할때..
        if(checkToken(access_token)){
            // 토큰 유효기간 5분 이내일 때 연장.
            if(tokenPayload(access_token).exp * 1000 - Date.now() < 300000){
                return reissueToken(refresh_token_index_id);
            }
            return true;
        }
    }
    else if(boolCheckCookie("refresh_token_index_id")){
        // access token 만료, refresh 유효 시
        return reissueToken(refresh_token_index_id);
    }
    else{
        // access, refresh 모두 만료시
        resetToken();
        return false;
    }
}

// 토큰 유효체크
function checkToken(token){
    let rtn = false;
    $.ajax({
        type: "POST",
        url: "/api/token/verify/",
        data: {
            "token" : token
        },
        datatype: "JSON",
        async: false,
        success: function(data) {
            rtn = true;
        },
        error: function(error) {
            console.log(error.responseJSON);
        },
    });
    return rtn;
}

// 토큰 재발급
function reissueToken(refresh_token_index_id){
    let rtn = false;

    $.ajax({
        type: "POST",
        url: "/api/token/refresh/",
        data: {
            "refresh_token_index_id" : refresh_token_index_id
        },
        datatype: "JSON",
        async: false,
        success: function(data) {
            console.log(data.user);
            setCookie("access_token", data.jwt_token.access_token, tokenPayload(data.jwt_token.access_token).exp);
            setCookie("refresh_token_index_id", data.jwt_token.refresh_token_index_id, data.jwt_token.refresh_token_exp);
            rtn = true;
        },
        error: function(error) {
            alert("만료된 토큰입니다.");
            resetToken();
        },
    });
    return rtn;
}

// 토큰 초기화
function resetToken(){
    delCookie("access_token");
    delCookie("refresh_token_index_id");
}

// 토큰 payload
function tokenPayload(token){
    let base64Url = token.split('.')[1];
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    let jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
}

function setCookie(key, value, timestamp) {
    let expiresDate = new Date(timestamp * 1000);
    document.cookie = key + "=" + escape(value) + "; path=/; expires=" + expiresDate.toGMTString() + ";";
}

function getCookie(key){
    key = new RegExp(key + '=([^;]*)'); // 쿠키들을 세미콘론으로 구분하는 정규표현식 정의
    return key.test(document.cookie) ? unescape(RegExp.$1) : ''; // 인자로 받은 키에 해당하는 키가 있으면 값을 반환
}

function delCookie(key){
    let todayDate = new Date();
    todayDate.setHours(todayDate.getMinutes() - 1);
    document.cookie = key + "=; path=/; expires=" + todayDate.toGMTString() + ";" // 현재 시각 이전이면 쿠키가 만료되어 사라짐.
}

function boolCheckCookie(key) {
    return getCookie(key) != '' ? true : false;
}

function logout(){
    if (!confirm("로그아웃 하시겠습니까?")) {
        return false;
    }
    let access_token = getCookie("access_token");
    let refresh_token_index_id = getCookie("refresh_token_index_id");
    $.ajax({
        type: "POST",
        url: "/api/logout/",
        headers: {
            'Authorization': `Bearer ${access_token}`,
        },
        data: {
            "refresh_token_index_id" : refresh_token_index_id
        },
        datatype: "JSON",
        success: function(data) {
            resetToken();
            location.reload();
        },
        error: function(error) {
            alert(error.responseJSON);
        },
    });
}