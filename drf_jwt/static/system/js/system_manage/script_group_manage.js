function clearCreationModal() {
    const creation_inputs = document.getElementById('divCreateGroup').getElementsByClassName('form-control');
    for(el of creation_inputs) {
        el.value = ''
    }
    document.getElementById('error_msg').textContent = '';
}



function createGroup() { 
    const err_elem = document.getElementById('error_msg');
    const groupName = document.getElementById('groupNameCreate').value;

    if (groupName == '') {
        err_elem.textContent = "생성할 그룹이름을 입력하세요.";
        return;
    }

    $.ajax({
        type: "POST",
        url: "/system-manage/group-manage/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "group_name" : groupName
        },
        datatype: "JSON",
        success: function(data) {
            alert("그룹이 생성되었습니다!");
            location.reload();
        },
        error: function(error) {
            alert(error.status + JSON.stringify(error.responseJSON));
        },
    });
}


function deleteGroup(groupId) { 
    if (groupId == '') {
        alert("삭제 불가능한 그룹입니다.");
        return;
    }
    if (!confirm("그룹을 삭제하시겠습니까?")) {
        return;
    }
    $.ajax({
        type: "DELETE",
        url: "/system-manage/group-manage/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "group_id" : groupId
        },
        datatype: "JSON",
        success: function(data) {
            alert("그룹이 삭제되었습니다!");
            location.href='/system-manage/access-manage/';
        },
        error: function(error) {
            alert(error.status + JSON.stringify(error.responseJSON));
        },
    });
}