var source=new EventSource("/showlog/"); 
source.onmessage=function(event) 
{ 
    $("#logboxdiv").removeAttr('style')
    //    $("#logbody").append(event.data + "<br/>")
    var aa = event.data.replace(/[ ]/g, "&nbsp;")    
    $("#logbody").append(aa + "<br/>")
}; 
