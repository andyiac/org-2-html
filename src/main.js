
var logout = function(){
    var str = window.location.href + new Date().getTime();
    var xmlhttp;
    if (window.XMLHttpRequest) xmlhttp=new XMLHttpRequest();
    else xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4) location.reload();
    }
    xmlhttp.open("GET",str,true);
    xmlhttp.setRequestHeader("Authorization","Basic xxxxxxxxxx")
    xmlhttp.send();
    return false;
}

