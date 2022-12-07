function page(num){
    if(window.location.search){
        let urlParams = new URLSearchParams(window.location.search);
        if(urlParams.has('page')){
            urlParams.set('page', num);
            window.location.href = window.location.pathname + '?' + urlParams;
        }
        else{
            window.location.href = window.location.href + '&page=' + num;
        }
    }
    else{
        window.location.href = '?page=' + num;
    }
}