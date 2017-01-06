var source=new EventSource("/showlog/"); 
source.onmessage=function(event) 
{ 
    //log = event.data.replace(/(^\s*)|(\s*$)/g,'');
    //log = event.data.replace(/(^\s+)/g,'&nbsp;')
    //alert(event.data.replace(/(^\s+)/g,'&nbsp;'))
    //document.getElementById("logbox").innerHTML+=event.data + "<br />"; 
    //document.getElementById("logbox").innerHTML+=event.data + "<br />"; 
    $("#logboxdiv").removeAttr('style')
    $("#logbox").append(event.data + "\n")
}; 
