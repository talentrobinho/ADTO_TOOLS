/*****************************
        获取COOKIE信息
******************************/
/**************************************
      第一个方法找cookie值
***************************************/  
// 定义一个函数，用来读取特定的cookie值。  
function getCookie(cookie_name)  
{  
    // 读取属于当前文档的所有cookies  
    var allcookies = document.cookie;  
    var cookie_pos = allcookies.indexOf(cookie_name);   //索引的长度  
       
    // 如果找到了索引，就代表cookie存在，  
    // 反之，就说明不存在。  
    if (cookie_pos != -1)  
    {  
        // 把cookie_pos放在值的开始，只要给值加1即可。  
        cookie_pos += cookie_name.length + 1;      //这里我自己试过，容易出问题，所以请大家参考的时候自己好好研究一下。。。  
        var cookie_end = allcookies.indexOf(";", cookie_pos);  
        if (cookie_end == -1)  
        {  
            cookie_end = allcookies.length;  
        }  
        var value = unescape(allcookies.substring(cookie_pos, cookie_end)); //这里就可以得到你想要的cookie的值了。。。  
    }  
    return value;  
}  

/**************************************
      第二个方法找cookie值
***************************************/  
// 定义一个函数，用来读取特定的cookie值。  
function getCookie2(cookie_name)  
{  
    var allcookies = document.cookie;  
    var cookie_arr = allcookies.split(";")  //将cookie转存到数组中

    //遍历cookie数组，查找给定的cookie值
    for(var i=0;i<cookie_arr.length;i++)
    {
        cookie_pos=cookie_arr[i].indexOf(cookie_name)
        //如果找到所给cookie，则退出查找循环，并返回找到的值
        if (cookie_pos != -1)  
        {  
            cookie_value=cookie_arr[i].split("=")[1]
            break
        }
        else
        {
            cookie_value=null
        }
    }
       
    return cookie_value
}  


// 调用函数  
//var cookie_val = getCookie("_adtech_user");  
var cookie_val = getCookie2("_adtech_user");  

/*****************************
        获取树节点信息
******************************/
function get_selected_treeInfo(info)
{

    //获取所选树节点信息
    var node = $("#leftbar").tree('getSelected');
    if( node == null)
    {
        alert("请选择服务节点")
        return false
    }
    if(info == 'node')
    {
        tr=node.text    
    }
    else if(info == 'tree')
    {
        var tr = node.text;
        var root = $('#leftbar').tree('getParent', node.target);
        while(root)
        {   
            tr = root.text + '_' + tr; 
            node = root;
            root = $('#leftbar').tree('getParent', node.target);
        }
    }
    return tr 
}
/*****************************
    动态生成route的select
******************************/
function create_route_select(obj)
{
    //获取route 和ring 下拉框对象
    var routeSelect = document.getElementById('route')
    //清空route 和 ring 下拉框的值
    routeSelect.options.length=0;

    for(selectKey in obj)
    {
        routeSelect.options.add(new Option(selectKey, selectKey))
    }
}

/**********************************
    动态生成ring 的select
***********************************/
function create_ring_select(obj)
{
    //获取route 和ring 下拉框对象
    var routeSelect = document.getElementById('route')
    var ringSelect = document.getElementById('ring')
    //清空ring 下拉框的值
    ringSelect.options.length=0;

    //获取所选树节点信息
    var node = $("#leftbar").tree('getSelected');
    var tr = node.text;
    var root = $('#leftbar').tree('getParent', node.target);
    while(root)
    {   
        tr = root.text + '_' + tr; 
        node = root;
        root = $('#leftbar').tree('getParent', node.target);
    }  
    
    for(selectKey in obj)
    {
        if(selectKey == routeSelect.value)
        {
            for(var i=0;i<obj[selectKey].length;i++)
            {
                ringSelect[i] = new Option(obj[selectKey][i], obj[selectKey][i])
            }
        }
    }
}


/*******************************
          选择环路事件
********************************/
function control_route()
{
    //document.getElementById('ring')
    //$("#ring").attr('disabled',false)
    $("#ring").attr('style',"display:none")
    $("#opselectbutton").removeAttr('style')
    $("#multi_button").removeAttr('style')
    $("#according_ring").removeAttr('checked')
    $("#according_multi_route").removeAttr('checked')
    $("#according_route").attr('checked', 'checked')
    $("#according_route").attr('value', 'on_route')
}
function control_ring()
{
    //document.getElementById('ring')
    //$("#ring").attr('disabled',true)
    $("#ring").removeAttr('style')
    $("#multi_button").attr('style', 'display:none')
    $("#according_route").removeAttr('checked')
    $("#according_multi_route").removeAttr('checked')
    $("#according_ring").attr('checked', 'checked')
    $("#according_ring").attr('value', 'on_ring')
    /***************************************************************
                删除多个路的下拉框，只保留第一个路选择下拉框
                将count赋值为1，重新计算路选择下拉框个数
    ***************************************************************/
    $("#routediv").children("select:first").next().nextAll().remove();
    count=1
}

/*******************************
          文件路径显示函数
********************************/
function show_filepath()
{
    if($("#conf").is(":checked"))
    {
        $("#filepath").removeAttr('style')
        $("#filelist").removeAttr('style')
    }
    else
    {
        $("#filepath").attr('style', 'display:none')
        $("#filelist").attr('style', 'display:none')
    }
    
}

/*******************************
    增加、减少路选择框函数          
********************************/
count=1
function addroute()
{
    var optarray = new Array(); //定义数组
    $("#route option").each(
                            //遍历全部option
                            function()
                            {   //获取option的内容
                                var txt = $(this).val();
                                //添加到数组中
                                optarray.push(txt);
                            });


    //select_route = $("#route option:selected").val()

    //获取select元素的option个数
    max=document.getElementById("route").options.length
    var select1 = document.createElement('select');
    if(count<max)
    {
        select1.setAttribute("class", "form-control");
        select1.setAttribute("id", "select"+count)
        $("#route").after(select1)
        $("#select"+count).before("</br>")

        //给新添加的select添加option选项
        var routeSelect = document.getElementById('select'+count)
        $.each(optarray, function(n, value){
                //alert(n+"..."+value)
                routeSelect.options.add(new Option(value, value))
        });
        count++
        //children_count=$("#routediv").children("select").length
        //alert(children_count)
    }
    //else
    //{
    //    children_count=$("#routediv").children("select").length
    //    alert(children_count)
    //    if(children_count == 1)
    //    {
    //        count = 1
    //    }
    //}
}
function delroute()
{
}


/*******************************
    create tree in the left
********************************/
$(document).ready(function(){
    /*** 设置ajax为同步，来讲获取的返回值赋值给全局变量 ***/
    $.ajaxSettings.async = false;

    /*** 从凯撒获取服务信息 ***/
    $.getJSON("/getrr/", function(json_data){
                rr_json=json_data
        });
    $.getJSON("/getsidebar/", function(json_data){
                tree_data=json_data
        });
    /*** 回复ajax的异步模式 ***/
    $.ajaxSettings.async = true;

    /*** 生成左侧树形列表 ***/
    $("#leftbar").tree({
        //url: 'http://10.129.149.152/getsidebar/',
        data: tree_data,
        onClick: function(leftbar){
            //var node = $("#leftbar").tree('getSelected');
            //var tr = node.text;
            //var root = $('#leftbar').tree('getParent', node.target);
            //while(root)
            //{   
            //    tr = root.text + '_' + tr;
            //    node = root;
            //    root = $('#leftbar').tree('getParent', node.target);
            //}
            tr = get_selected_treeInfo('tree')
            if(tr == false)
            {
                return false
            }
            
            var route = ""
            var ring_list = ""
            var rr = new Object()
            var ring = new Array()
            for(var ser_index in rr_json)
            {
                server=rr_json[ser_index]['content']
                route_list=rr_json[ser_index]['children']
                if(server == tr)
                {
                    for(var route_index in route_list)
                    {
                        route=route_list[route_index]['content']
                        ring_list=route_list[route_index]['children']
                        ring.length=0
                        for(var key in ring_list)
                        { 
                            ring[key]=ring_list[key]
                        }
                        rr[route]=ring;
                    }
                }
            }
            create_route_select(rr);
            create_ring_select(rr);


            /*** 检查是否在上线状态，开启构建、分发按钮 ***/
            $.getJSON("/op_online/",{"service":tr,"user":cookie_val}, function(json_data){
                        if(json_data[0]['status']=='is_online')
                        {
                            $("#button_build").removeAttr('disabled')
                            $("#button_deploy").removeAttr('disabled')
                        }
                        else
                        {
                            $("#button_build").attr('disabled',true)
                            $("#button_deploy").attr('disabled',true)
                        }
            });
        }

        });
});

/*********************************************************************************************************************
                                               to_online 
*********************************************************************************************************************/
function to_online()
{
    tr = get_selected_treeInfo('tree')
    if(tr == false)
    {
        return false    
    }
    /*** 是否进行上线操作模态框弹出 ***/
    $.getJSON("/op_online/", {"service":tr,"user":cookie_val}, function(json_data){
                //alert(json_data[0]['status'])
                if(json_data[0]['status']=='is_online')
                {
                   alert("你在上线状态") 
                }
                else if(json_data[0]['status']=='offline')
                {
                    $("#online_modal").modal({backdrop: 'static', keyboard: false, show: true})
                }
                else
                {
                    alert(json_data[0]['status']['op_user']+" is online "+json_data[0]['status']['server'])    
                }
        });
}
/*********************************************************************************************************************
                                               Lock online 
*********************************************************************************************************************/
function sure_online()
{
    tr = get_selected_treeInfo('tree')
    if(tr == false)
    {
        return false    
    }
    $.getJSON("/lock_online/", {"service":tr}, function(json_data){
        //if(json_data[0]['status']=="is_online")
        //{
        //    alert(json_data[0]['status']+"you online stauts......")
        //}
        $("#online_modal").modal('hide')
    });
    $("#button_build").removeAttr('disabled')
    $("#button_deploy").removeAttr('disabled')
    
}

/*********************************************************************************************************************
                                                Build and Deploy
*********************************************************************************************************************/
function check_form()
{
    var accorde_route = ""
    var accorde_ring = ""
    var select_route = ""
    var select_ring = ""
    var bin_flag=0
    var conf_flag=0
    var tree = get_selected_treeInfo('tree')
    var form_content = {}
    
    if(tree == false)
    {
        return false
    }
    form_content['server'] = tree

    choice_way=$("input[type='radio']:checked").val();
    //if($("#according_route").attr("checked") == 'checked')
    if(choice_way == 'on_route')
    {
        select_route = $("#route option:selected").val()
        if(typeof(select_route) == "undefined")
        {
            alert("route 不能为空")
            return false
        }
        //form_content['onlinetype'] = $("#according_route").val()
        form_content['onlinetype'] = choice_way
        form_content['route'] = select_route
    }
    //else if($("#according_ring").attr("checked") == 'checked')
    else if(choice_way == 'on_ring')
    {
        select_route = $("#route option:selected").val()
        select_ring = $("#ring option:selected").val()
        //alert(select_route+"|"+select_ring)
        if(typeof(select_route) == "undefined")
        {
            alert("route 不能为空")
            return false
        }
        else if(typeof(select_ring) == "undefined")
        {
            alert("ring 不能为空")
            return false
        }
        //form_content['onlinetype'] = $("#according_ring").val()
        form_content['onlinetype'] = choice_way
        form_content['route'] = select_route
        form_content['ring'] = select_ring
    }
    else
    {
        alert("请选择上线粒度。")    
        return false
    }
    if($("#bin").is(":checked"))
    {
            select_bin = $("#bin").val()
            bin_flag=1
            //alert(select_bin)
            //form_content['bin'] = select_bin
    }
    if($("#conf").is(":checked"))
    {
            rsync_path=$("#file_path").val()
            rsync_file=$("#file_list").val()
            if(rsync_path.length==0)
            {
                alert("文件地址不能为空")
                return false
            }
            if(rsync_file.length==0)
            {
                alert("文件列表不能为空")
                return false
            }
            select_conf = $("#conf").val()
            conf_flag=1
            //form_content['conf'] = select_conf
            form_content['rsync_path'] = rsync_path
            form_content['rsync_file'] = rsync_file
    }
   if(bin_flag == 0 && conf_flag == 0) 
    {
        alert("bin和conf 选项不能都为空")
        return false

    }
    else if(bin_flag == 1 && conf_flag == 1)
    {
            form_content['file'] = 2
        
    }
    else if(conf_flag==1)
    {
            form_content['file'] = 1
    }
    else if(bin_flag==1)
    {
            form_content['file'] = 0
    }

    //alert(form_content["onlinetype"]+"+"+form_content['server']+"+"+form_content["route"]+"+"+form_content["ring"]+"+"+form_content["bin"]+"+"+form_content["conf"])
    return form_content
}



function build_project()
{
    var pgn = {}
    op_server_info = check_form()
    pgn['pgname'] = get_selected_treeInfo('node')
    form_info = $.extend(op_server_info, pgn)
    if(form_info == false)
    {
        return false
    }
    //alert(form_info["onlinetype"]+"+"+form_info['server']+"+"+form_info["route"]+"+"+form_info["ring"]+"+"+form_info["bin"]+"+"+form_info["conf"])
    /******************
          进度条
    *******************/
    //show_bar()
    $.post("/build/", form_info, function(json_data){
                
                alert(json_data[0]['status'])
                //if(json_data[0]['status'] == "success")
                //{
                //     $('#barc').css("width","100%");
                //}
        },
        "json");
    show_build_modal('false')
    
}

function deploy_project()
{
    var pgn = {}
    op_server_info = check_form()
    pgn['pgname'] = get_selected_treeInfo('node')
    form_info = $.extend(op_server_info, pgn)
    if(form_info == false)
    {
        return false
    }
    $.post("/deploy/", form_info, function(json_data){
                alert(json_data[0]['status'])
        },
        "json");
    show_deploy_modal('false')
}


//function build_project()
//{
//    form_info = check_form()
//    if(form_info == false)
//    {
//        return false
//    }
//    $("#build_service").text('adtech_pc_search_main_bidding')
//    $("#build_content").text('bin and conf')
//    $('#build_modal').modal('show')
//}
//
//function deploy_project()
//{
//    //alert("Deploy Success")
//    $("#deploy_service").text('adtech_pc_search_main_bidding')
//    $("#deploy_content").text('bin and conf')
//    $("#ip_list").text('10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11 10.101.10.100 10.11.111.11')
//    $('#deploy_modal').modal('show')
//}

/********************************
        显示模态框控制
********************************/
function show_build_modal(open='true')
{
    if(open == 'true')
    {
        
        choice=$("input[type='radio']:checked").val();
        build_info=check_form()
        if(build_info == false)
        {
            return false    
        }
        //alert(form_content["onlinetype"]+"+"+form_content['server']+"+"+form_content["route"]+"+"+form_content["ring"]+"+"+form_content["bin"]+"+"+form_content["conf"])
        if(choice == 'on_route')
        {
            $("#build_service").text(build_info['server']+'  '+build_info['route']+' 路')
        }
        else if(choice == 'on_ring')
        {
            $("#build_service").text(build_info['server']+'  '+build_info['route']+' 路  '+build_info['ring']+' 环')
        }

        //alert(build_info['file'])
        //if('bin' in build_info && 'conf' in build_info)
        if(build_info['file'] == 2)
        {
            $("#build_content").text()
            $("#file_path_label").show()
            $("#file_list_label").show()
            //$("#build_content").text(build_info['bin']+' 文件和'+build_info['conf']+' 文件')
            $("#build_content").text('bin 文件和conf 文件')
            $("#rsync_file_path").text(build_info['rsync_path'])
            $("#rsync_file_list").text(build_info['rsync_file'])
        }
        //else if ('bin' in build_info)
        else if (build_info['file'] == 0)
        {
            $("#build_content").text()
            $("#rsync_file_path").text('')
            //$("#build_content").text(build_info['bin']+' 文件')
            $("#build_content").text('bin 文件')
            $("#file_path_label").hide()
            $("#file_list_label").hide()
        }
        //else if ('conf' in build_info)
        else if (build_info['file'] == 1)
        {
            $("#build_content").text()
            $("#file_path_label").show()
            $("#file_list_label").show()
            //$("#build_content").text(build_info['conf']+' 文件')
            $("#build_content").text('conf 文件')
            $("#rsync_file_path").text(build_info['rsync_path'])
            $("#rsync_file_list").text(build_info['rsync_file'])
        }
        $('#build_modal').modal('show')
    }
    else
    {
        $('#build_modal').modal('hide')    
    }
}

function show_deploy_modal(open='true')
{
    if(open == 'true')
    {
        $('#deploy_modal').modal('show')
    }
    else
    {
        $('#deploy_modal').modal('hide')    
    }
}

/********************************
        构建进度条
********************************/
function process(percent){
    $('#barc').css("width",percent+"%");
}

function show_bar(){
    var percent = 0;
    myBar = setInterval(function(){
                process(percent);
                percent += 0.2;
                if(percent > 92)
                {
                    clearInterval(myBar);
                }
            }, 100);
}


/********************************
        添加上线权限
********************************/
function set_privilege()
{
        var server_info=""
        var tmp_add=""
        var is_privilege
        $.getJSON("/getserverlist/", function(json_data){
            for(var i=0;i<json_data.length;i++)
            {
                server_info=json_data[i]['server']
                if(server_info == 'NOPERMISSION')
                {
                    is_privilege='NO'
                }
                else
                {
                    $("#server_list").append("<option value='Value'>"+server_info+"</option>")
                }
            }
            if(is_privilege == 'NO')
            {
                alert('YOU ARE NOPERMISSION')
                return false
            }
            $('#set_privilege').modal('show')
        });

        // 选择赋予权限的server，在已选择列表中显示，并在待选列表中删除
        $('#server_list').dblclick(function(){
            append_server=$("#server_list").find("option:selected").text()
            $('#server_list option:selected').remove();
            $("#select_server").append("<option value='Value'>"+append_server+"</option>")
        });

        // 删除已选择的server，并添加到待选择列表中
        $('#select_server').dblclick(function(){
            append_server=$("#select_server").find("option:selected").text()
            $('#select_server option:selected').remove();
            $("#server_list").append("<option value='Value'>"+append_server+"</option>")
        });


}

/********************************
        选中server函数
********************************/
//function move_server()
//{
//    
//}
/********************************
        权限写入数据库
********************************/
function add_privilege_to_db()
{
    $('#set_privilege').modal('hide')
    no_select=$("#server_list option").map(function(){return $(this).text();}).get().join(", ")
    yes_select=$("#select_server option").map(function(){return $(this).text();}).get().join(", ")
    //alert(yes_select)
    //alert("添加权限成功！");
    //$.getJSON("/record_privilege/", {"no_choice_privilege":'xxxxxxxxxx', "yes_choice_privilege":yes_select, 'user':cookie_val}, function(json_data){
    $.post("/record_privilege/", {"no_choice_privilege":no_select, "yes_choice_privilege":yes_select, 'user':cookie_val}, function(json_data){
        alert(json_data[0]['status'])
    }, "json");
}
