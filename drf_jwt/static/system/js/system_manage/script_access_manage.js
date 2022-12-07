const search_form = document.getElementById("search-form");

function getGroupPermissionList() {
    const selectedGid = document.getElementById('groupsSelect').value;
    if (!selectedGid) {
        return;
    }
    location.href = `?group_id=${selectedGid}`
}

search_form.addEventListener("submit", (e) =>{
    e.preventDefault();
    search_form.submit();
})

function setGroupPermission(permId, groupId){
    const isChecked = document.getElementById(`Perm${permId}`).checked;
    $.ajax({
        type: "POST",
        url: "",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "group_id" : groupId,
            "permission_id" : permId,
            "has_perm" : isChecked
        },
        datatype: "JSON",
        success: function(data) {
            alert("권한이 변경되었습니다!");
        },
        error: function(error) {
            alert(error.status + JSON.stringify(error.responseJSON));
            location.reload();
        },
    });
}