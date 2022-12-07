const search_form = document.getElementById("search-form");

search_form.addEventListener("submit", (e) =>{
    e.preventDefault();
    search_form.submit();
})

const menu_creation_modal = new bootstrap.Modal(document.getElementById('modal_create_menu'), {
    keyboard: false
});

const menu_update_modal = new bootstrap.Modal(document.getElementById('modal_update_menu'), {
    keyboard: false
});

function updateUrlText(el, alerter_id) {
    url = el.value;
    url_alerter = document.getElementById(alerter_id);
    if (url === '') {
        url_alerter.innerHTML = '<i class="fa" aria-hidden="true" ></i>접근 권한을 설정할 Code를 입력하세요.';
    } else {        
        url_alerter.innerHTML = `<code>${url}</code>` + "에 대한 메뉴 접근 권한이 생성됩니다.";
    }
}


function clearCreationModal() {
    document.getElementById('name').value = '';
    document.getElementById('codename').value = '';
    updateUrlText(
        document.getElementById('codename'),
        'create_url_alerter'
    );
    document.getElementById('error_msg').textContent = '';
}

function clearUpdateModal(id_to_update) {
    const id = document.getElementById(`permId${id_to_update}`).dataset.value;
    const name = document.getElementById(`permName${id_to_update}`).dataset.value;
    const codename = document.getElementById(`permCodename${id_to_update}`).dataset.value;

    document.getElementById('id_update').value = id;
    document.getElementById('name_update').value = name;
    document.getElementById('codename_update').value = codename;
    updateUrlText(
        document.getElementById('codename_update'),
        'update_url_alerter'
    );
    document.getElementById('update_error_msg').textContent = '';
}


function createMenu() {
    const err_elem = document.getElementById('error_msg');
    const menu_name = document.getElementById('name').value;
    const menu_codename = document.getElementById('codename').value;
    if (menu_name === '' || menu_codename === '') {
        err_elem.textContent = "필드값을 모두 입력하세요.";
        return;
    }
    $.ajax({
        type: "POST",
        url: "",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "name" : menu_name,
            "codename" : menu_codename
        },
        datatype: "JSON",
        success: function(data) {
            alert("권한이 생성되었습니다!");
            location.reload();
        },
        error: function(error) {
            alert(error.status + JSON.stringify(error.responseJSON));
        },
    });
}

function updateMenu() {
    const err_elem = document.getElementById('update_error_msg');
    const menu_id = document.getElementById('id_update').value;
    const menu_name = document.getElementById('name_update').value;
    const menu_codename = document.getElementById('codename_update').value;
    
    if (menu_name === '' || menu_codename === '') {
        err_elem.textContent = "필드값을 모두 입력하세요.";
        return;
    }
    $.ajax({
        type: "PUT",
        url: "",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "id" : menu_id,
            "name" : menu_name,
            "codename" : menu_codename
        },
        datatype: "JSON",
        success: function(data) {
            alert("권한이 수정되었습니다!");
            location.reload();
        },
        error: function(error) {
            alert(error.status + JSON.stringify(error.responseJSON));
        },
    });
}

function deleteMenu(id) {
    if (id === '' || !confirm('권한을 삭제하시겠습니까? ')) {
        return;
    }

    $.ajax({
        type: "DELETE",
        url: "",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "id" : id
        },
        datatype: "JSON",
        success: function(data) {
            alert("권한이 삭제되었습니다!");
            location.reload();
        },
        error: function(error) {
            alert(error.status + JSON.stringify(error.responseJSON));
        },
    });
}