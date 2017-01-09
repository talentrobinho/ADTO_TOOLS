# -*- coding:UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from main_page import main_interface
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
import urllib2
import re
import sys, os
import json
import jenkins
from django.conf import settings
from django.core.cache import cache
import subprocess
from Galactic_Warships.SaltDeploy import SALTDEPLOY
import logging
import redis


logger = logging.getLogger('test')


########################################################################################
###                         测试实时日志信息推送到页面                               ###
########################################################################################

class MESSAGE(object):
    
    def __init__(self, host='127.0.0.1', port='6379'):
        self.host = host
        self.port= port
        self.redis = redis.StrictRedis(host=self.host, port=self.port)


    #def __CreatePubsub(self):
    #    red = redis.StrictRedis(host=self.host, port=self.port)
    #    return red

    def SubScribe(self, pname):
        #r = self.__CreatePubsub()
        #piple = r.pubsub()
        #piple.subscribe(pname)
        piple = self.redis.pubsub()
        piple.subscribe(pname)
        return piple

    def Publish(self, pname, msg):
        #r = self.__CreatePubsub()
        #r.publish(pname, msg)
        self.redis.publish(pname, msg)

 
################################################################
###                    自定义 异常类                         ###
################################################################
class rsyncException(Exception):
    """
    Raised when the SVN CLI command returns an error code.
    """
    #def __init__(self, resultcode, cmd, resultout):
    #    self.__resultcode = resultcode
    #    self.__cmd = cmd
    #    self.__resultout = resultout
    #    
    #    print '''
    #    self.__resultcode: %s
    #    self.__cmd: %s
    #    self.__resultout: %s
    #    '''%(self.__resultcode, self.__cmd, self.__resultout)

    #"Command failed with ({}): {}\n{}".format(self.__resultcode, self.__cmd, self.__resultout)
    pass
        

################################################################
###                    自定义 装饰器                         ###
################################################################
def auth_required(view):
    """身份认证装饰器，
    :param view:
    :return:
    """
 
    def decorator(request, *args, **kwargs):
        #token = request.POST.get('auth_token', '')
        user = request.COOKIES["_adtech_user"]
        try:
            if user == 'lizhansheng':
                return view(request, *args, **kwargs)
        except ValueError:
            pass
        return auth_fail_handler(request)
    return decorator
 
 
def auth_fail_handler(request):
    """非法请求处理
    :param request:
    :return:
    """
    return HttpResponse(json.dumps([{'server': 'NOPERMISSION'}]), content_type='application/json')


# Create your views here.
def top(req):
    #print req.COOKIES["_adtech_user"]
    topic = req.COOKIES["_adtech_user"]
    logger.info('User access to %s Galactic Warships platform home page' % (topic,))
    return render(req, "main.html")


##################################################################
###            将日志输出到web页面                             ###
##################################################################
import time
from django.http import StreamingHttpResponse
from django.utils.timezone import now

#logmsg = MESSAGE()
#p = logmsg.SubScribe('online')
#pp = logmsg.SubScribe('online')
#logmsg.Publish('online', 'ssssssssssssssssssssssssss')
def stream_generator(sub): 
    #for item in p.listen():
    #    for i,j in item:
    #        if i == 'data':
    #            yield u"%s"% j
    #    #if item['type'] == 'message':
    #    #    #yield u'%s\n\n' % message['data']
    #    #    #bb=item['data']
    #    #    yield u"%s" % item['data']
    while True: 
        # 发送事件数据 
        # yield 'event: date\ndata: %s\n\n' % str(now()) 
 
        ## 发送数据 
        #yield u'data: %s\n\n' % str(now()) 
        #logmsg.Publish('online', 'ttttttttttttttttttttttttttttttttttttttttttttt')
        #print aaa
        aaa = p.get_message(sub)
        if aaa:
            #if aaa['type'] == 'message':
                #print aaa
                #yield u'%s\n\n' % aaa['data']
            #yield aaa['data']
            #yield aaa
            yield u'data:%s\n\n' % aaa['data']
        #else:
        #    #continue
        #    yield u'data: %s\n\n' % str(now())
        time.sleep(0.01)

def showlogevent(request):
    global p
    global pp
    global logmsg
    logmsg = MESSAGE()
    logtopic = request.COOKIES["_adtech_user"]
    p = logmsg.SubScribe(logtopic)
    pp = logmsg.SubScribe(logtopic)
    #logmsg.Publish(logtopic, "Welcome %s to Galactic Warships!!!" % (logtopic,))
    response = StreamingHttpResponse(stream_generator(logtopic), content_type="text/event-stream") 
    #response = StreamingHttpResponse(p.listen(), content_type="text/event-stream") 
    #p.close()
    return response 


##################################################################
##################################################################
def split_word(str):
    eliminate_string=re.compile(r'[\t\n ]')
    if len(eliminate_string.search(str)) != 0:
        word_list=eliminate_string.split(str)

def Generate_directory_tree():
    pass

def Make_Tree_Json(fa_list, str):
    is_find=0
    tmp={}
    root=fa_list
    father=fa_list
    str_list_uniq = str
    #print str_list_uniq
    for i in range(len(str_list_uniq)):
        if not str_list_uniq[i]:
            continue
        if len(father)==0 and str_list_uniq[i] != str_list_uniq[-1]:
            tmp['text']=str_list_uniq[i]
            tmp['children']=[]
            father.append(tmp)
            father=father[-1]['children']
            tmp={}
            continue
        elif i == len(str_list_uniq)-1:
            tmp['text'] = str_list_uniq[i]
            tmp['attributes'] = {}
            #tmp['attributes']['url'] = 'aaa'
            father.append(tmp)
            tmp={}
            continue
        else:
            for j in range(len(father)):
                if str_list_uniq[i] == father[j]['text']:
                    father = father[j]['children']
                    is_find=1
                    break
                else:
                    is_find=0
            if is_find == 1:
                continue

        tmp['text']=str_list_uniq[i]
        tmp['children']=[]
        tmp['state']='closed'
        father.append(tmp)
        father = father[-1]['children']
        tmp={}

    return root



def get_service_info():
    try:
        caesar_list=urllib2.urlopen("http://stat.union.sogou-inc.com/server/GetIpByPath.php?path=/&type=text").read()
    except urllib2.HTTPError,e:
       print e.code

    IP_RE=re.compile(r'\t(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    sidebar_list=IP_RE.sub("", caesar_list).split("\n")
    return sidebar_list



def server_map_rr(list):
    service=list[:-2]
    rr=list[-2:].split('/')
    service_list={}
    service_list[service]=[]
    service_list[service].append(rr)
    return service_list



################################################################
###         make select of route and ring json data          ###
################################################################
def rr_list(req):
    service_info=get_service_info()
    join_str='_'
    tmp_dict={}
    route_info=[]
    ring_list=[]
    rr_info=[]
    deal_list=[]
    count=1
    route_count=1
    for line in service_info:
        if line and line not in deal_list:
            deal_list.append(line)
            service_rr=line.strip('/').split('/')
            service=service_rr[:-2]
            route=service_rr[-2]
            ring=service_rr[-1]
            service_str=join_str.join(service)
            if len(rr_info) == 0:
                ring_list.append(ring)
                tmp_dict['content']=service_str
                tmp_dict['children']=[{'content':route,'children':ring_list}]
                rr_info.append(tmp_dict)
                tmp_dict={}
                ring_list=[]
                continue
            for service_dict in rr_info:
                if service_str != service_dict['content'] and count != len(rr_info):
                    count+=1
                    continue
                if service_str == service_dict['content']:
                    for route_dict in service_dict['children']:
                        if route != route_dict['content'] and route_count != len(service_dict['children']):
                            route_count+=1
                            continue
                        if route == route_dict['content']:
                            route_dict['children'].append(ring)
                            route_count=1
                            break
                        else:
                            tmp_dict['content']=route
                            ring_list.append(ring)
                            tmp_dict['children']=ring_list
                            service_dict['children'].append(tmp_dict)
                            tmp_dict={}
                            ring_list=[]
                            route_count=1
                            break
                    count=1
                    break
                else:
                    ring_list.append(ring)
                    tmp_dict['content']=service_str
                    tmp_dict['children']=[{'content':route,'children':ring_list}]
                    rr_info.append(tmp_dict)
                    tmp_dict={}
                    ring_list=[]
                    count=1
                    break
    return HttpResponse(json.dumps(rr_info), content_type='application/json')



############################################
###         make tree json data          ###
############################################
@csrf_exempt
def sidebar_content(req):
    root=[]
    tmp_root=[]
    fa=[]
    tmp={}
    deal_list=[]
    sidebar_list=get_service_info()
    #print type(sidebar_list)
    for line in sidebar_list:
        if line:
            line_tmp = line.strip('/').split('/')
            line_list = line_tmp[:-2]
            if line_list in deal_list:
                continue
            deal_list.append(line_list)
            tmp_root = Make_Tree_Json(tmp_root, line_list)
    return HttpResponse(json.dumps(tmp_root), content_type='application/json')

############################################
###         operation online             ###
############################################
def operation_online(req):
    #op_user=req.COOKIES["_adtech_user"]
    op_user=req.GET["user"]
    ser=req.GET["service"]
    print "op ser:%s"%(ser,)
    online_info = cache.get("online", "Nonexxxxx")
    if online_info != 'Nonexxxxx':
        for user in online_info:
            print user
            if user['server'] == ser and op_user == user['op_user']:
                print "You are online this server %s"%(user['server'],)
                status=[{'status':'is_online'}]
                break
            elif user["server"] == ser and op_user != user['op_user']:
                print "%s is online %s"%(user['op_user'], user['server'])
                status=[{'status':user}]
                break
            else:
                status=[{'status':'offline'}]
    else:
        status=[{'status':'offline'}]
    return HttpResponse(json.dumps(status), content_type='application/json')
    

############################################
###         check     online             ###
############################################
def check_online():
    online_user = cache.get("online", "Nonexxxxx")
    if op_user == online_user:
        status='yes'
    else:
        status='no'
    return status 
    #return HttpResponse(json.dumps(status), content_type='application/json')
    #return render(req, "main.html",{'status':'online'})
 
############################################
###            lock online               ###
############################################
def lock_online(req):
    op_user=req.COOKIES["_adtech_user"]
    ser=req.GET["service"]
    #print "lock ser:%s"%(ser,)
    #cache.set('get_user_id_bugall',[{'aa':'123', 'bb':'456'}],settings.NEVER_REDIS_TIMEOUT)
    online_user_list=cache.get("online", "None")
    if online_user_list == "None":
        online_user_list = []
    online_info={'op_user':op_user,'server':ser}
    online_user_list.append(online_info)
    #cache.set("online", online_info, 60)
    cache.set("online", online_user_list, 180)
    status=[{'status':'is_online'}]
    #b=cache.get("online", "None")
    #print "xxxxxxxxxx:%s"%(type(b),)
    rep=HttpResponse(json.dumps(status), content_type='application/json')
    rep.set_cookie("is_online", "onlining")
    return rep


############################################
###     remote build project             ###
############################################
def send_build_cmd(project_name):
    if len(project_name) == 0:
        sys.exit(1)
    url="http://jenkins.adto.ad.sogou/job/adtech_PC_Search_main_BiddingMaterial_A_ring0/build?token=123456"
    userpasswd="jenkins:jenkins"
    build_cmd="curl -s -u %s %s"%(userpasswd, url)
    print build_cmd
    outlog = os.popen(build_cmd).read()
    print outlog
    

def check_building(ser, pname, build_num):
    check_status = ''
    build_info = ser.get_build_info(pname, build_num)
    build_status = build_info['building']
    if build_status:
        check_status = 'True'
    else:
        check_status = 'False'
    print "build_status: %s"%(build_status,)
    print "check_status: %s"%(check_status,)
    return check_status

############################################
###     同步配置文件到本地并上传svn      ###
############################################
class Process_File(object):
    @staticmethod 
    def split_file(str):
        return re.split(',|;| *|\n|\t', str)


class OperationFile(object):
    def __init__(self, cmd='rsync', option='-P', src_path='/tmp/', dst_path='/tmp', file_list_str='', success_code=0):
        self.__cmd=cmd
        self.__option=option
        self.__src_file=''
        self.__stdout_list=[]
        self.__src_path=src_path
        self.__dst_path=dst_path
        self.__list_file_str=file_list_str
        self.__success_code=success_code
        self.cmd_info = ""
        #self.cmd_info = [self.__cmd, self.__option, self.__src_path, self.__dst_path]
        print '''
            self.__cmd: %s
            self.__option: %s
            self.__src_path: %s
            self.__dst_path: %s
            self.cmd_info: %s
        '''%(self.__cmd,  self.__option, self.__src_path, self.__dst_path, self.cmd_info)

    def rsync_file(self):
        try:
            if not os.path.isdir(self.__dst_path):
                print 'dir exists'
                os.makedirs(self.__dst_path)
        except exception as err:
            print "create directory fail: %s"%(err,)
        else:
            print "mkdir %s"%(self.__dst_path)
        rsync_file_list=Process_File.split_file(self.__list_file_str)
        for f in rsync_file_list:
            self.__src_file="%s/%s"%(self.__src_path, f)
            self.cmd_info = [self.__cmd, self.__option, self.__src_file, self.__dst_path]
            p = subprocess.Popen(
                self.cmd_info,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            #stdout = p.stdout.read()
            self.__stdout_list.append(p.stdout.read())
            r = p.wait()
            p.stdout.close()

        print '''
            stdout: %s
            returncode: %s
        '''%(self.__stdout_list, r)
        #if r != self.__success_code:
        #    ##seq = ' '
        #    ##raise rsyncException("Command failed with ({}): {}\n{}".format(r, seq.join(cmd_info), stdout))
        #    #print 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        #    ##raise rsyncException("Command failed with ({}): {}\n{}".format(p.returncode, "rsync xxxxxxxxxxxx", stdout))
        #    #raise rsyncException("Command failed with ({})".format(r))
        #
        #return stdout.decode().strip('\n').split('\n')
        #sys.exit(2)
        return r

class OperationSVN(object):
     def __init__(self, cmd='svn', add_option='add', commit_option='commit', desc_option='-m', code_path='/tmp/', success_code=0, svn_username='test', svn_passwd='test'):
        self.__cmd=cmd
        self.__code_path=code_path
        self.__add_option=add_option
        self.__commit_option=commit_option
        self.__desc_option=desc_option
        self.__success_code=success_code
        self.__username=svn_username
        self.__passwd=svn_passwd
        self.__cmd_info=[self.__cmd, '--username', self.__username, '--password', self.__passwd]

     def add_file(self, file=''):
        if len(file)==0:
            #add_cmd = [self.__cmd, self.__add_option, "%s/%s"%(self.__code_path, "*")]
            add_cmd = [self.__cmd, self.__add_option, "%s"%(file,)]
        else:
        ###self.__cmd_info += [self.__cmd, self.__add_option, "%s/*"%(self.__code_path,)]
            #add_cmd = [self.__cmd, self.__add_option, "%s/"%(self.__code_path,)]
            seq=' '
            file_list=Process_File.split_file(file)
            #file_list=seq.join(svn_file_list)
            add_cmd = [self.__cmd, self.__add_option] + file_list
        #cmd = [self.__cmd, self.__add_option, "%s/*"%(self.__code_path,)]
        #b=" "
        #add_cmd = b.join(cmd) 
    
        print add_cmd
     
        pwd=os.getcwd()
        os.chdir(self.__code_path)
        svnaddinfo = subprocess.Popen(
            add_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
            )
        svn_add_stdout = svnaddinfo.stdout.read()
        svn_add_result = svnaddinfo.wait()
        svnaddinfo.stdout.close()
        print '''
            svn add stdout: %s
            svn add returncode: %s
        '''%(svn_add_stdout, svn_add_result)
        os.chdir(pwd)
        return svn_add_stdout.decode().strip('\n').split('\n')

     def commit_file(self, file='', desc=''):
        if desc == '':
            sys.exit(1)
        #commit_cmd = self.__cmd_info + [self.__commit_option, "%s/%s"%(self.__code_path, "*"), self.__desc_option, desc]
        commit_cmd = self.__cmd_info + [self.__commit_option, self.__desc_option, desc]
        print commit_cmd
             
        pwd=os.getcwd()
        os.chdir(self.__code_path)
        svncommitinfo = subprocess.Popen(
            commit_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
            )
        svn_commit_stdout = svncommitinfo.stdout.read()
        svn_commit_result = svncommitinfo.wait()
        svncommitinfo.stdout.close()
        print '''
            svn add stdout: %s
            svn add returncode: %s
        '''%(svn_commit_stdout, svn_commit_result)
        os.chdir(pwd)
        return svn_commit_stdout.decode().strip('\n').split('\n')


        



############################################
###         找出构建的业务线             ###
############################################
def find_module(str):
    if str.find('PC_Search')>=0:
        pname="PC_Search"
    elif str.find('Mobile_Search')>=0:
        pname="Mobile_Search"
    elif str.find('PC_Union')>=0:
        pname="PC_Union"
    elif str.find('Wireless_Union')>=0:
        pname="Wireless_Union"
    elif str.find('Common')>=0:
        pname="Common"
    return pname


############################################
###         build project                ###
############################################
def build_project(req):
    if req.method == 'POST':
        opuser = req.COOKIES["_adtech_user"]
        if check_online == 'no':
           status=[{'staus':opuser}]
        else:
            online_type = req.POST.get('onlinetype')
            pgname = req.POST.get('pgname')
            server = req.POST.get('server')
            route = req.POST.get('route')
            ring = req.POST.get('ring')
            binfilepath = req.POST.get('get_bin_path')
            binfilemd5 = req.POST.get('check_bin_md5')
            filepath = req.POST.get('rsync_path')
            filetype = req.POST.get('file')
            filelist = req.POST.get('rsync_file')
            
            ##############################################
            ### 将用户conf或bin文件拉到本地，再上传svn ###
            ##############################################

            ### if int(filetype) == 0:
            ###     new_file_path = 'bin'
            ###     print 'bbbbbbbbbbbbbbbbbbbbbbbbbbb'
            ### elif int(filetype) == 1 or int(filetype) == 2:
            ###     new_file_path = 'conf'
            ###     print 'filelist: %s'%(filelist,)
            ### localpath = "/tmp/adtech/%s/%s/%s/%s"%(server, route, ring, new_file_path)

            ### print 'localpath: %s'%(localpath,)
            ### print 'pgname: %s'%(pgname,)
            ### print 'new_file_path: %s'%(new_file_path,)
            ### opfile = OperationFile(src_path=filepath, dst_path=localpath, option="-aP", file_list_str=filelist)
            ### rsyncresult=opfile.rsync_file()
            ### print "rsyncresult: %s"%(rsyncresult,)
            ### if rsyncresult == 0:
            ###     opsvn = OperationSVN(code_path=localpath)
            ###     opsvn.add_file(filelist)
            ###     opsvn.commit_file(file=filelist, desc='test xxxx svn')

            if online_type == "on_ring":
                #print "online_type: %s; server: %s; route: %s;ring: %s;"%(online_type, server, route, ring)
                #project_name=server+"_"+route+"_"+ring
                project_name=find_module(server)

                #send_build_cmd(pname)
                build_param={'server_name':server, 'route':route, 'ring':ring, 'pgname':pgname}
            elif online_type == "on_route":
                #project_name=server+"_"+route
                project_name=find_module(server)
                build_param={'server_name':server, 'route':route,'ring':'all', 'pgname':pgname}
                #print "online_type: %s; server: %s; route: %s;"%(online_type, server, route)

            logger.info('Create connecting to Jenkins')
            jenkinsserver = jenkins.Jenkins("http://jenkins.adto.ad.sogou/", username='jenkins', password='jenkins')
            next_build_number = jenkinsserver.get_job_info(project_name)['nextBuildNumber']
            last_build_number = jenkinsserver.get_job_info(project_name)['lastBuild']['number']
            check_result = check_building(jenkinsserver, project_name, last_build_number)
            logmsg.Publish(opuser, "next_buil_number: %s" % (next_build_number,))
            logmsg.Publish(opuser, "last_buil_number: %s" % (last_build_number,))
            print "check_result: %s"%(check_result,)
            status = []
            tmp_status = {}
            if check_result == 'True':
                tmp_status['status'] ='building'
                status.append(tmp_status)
            elif check_result == 'False':
                print 'xxxxxproject_name: %s'%(project_name,)
                print "module: %s; module_route: %s; module_ring: %s;"%(server, route, ring)

                logger.info('Start build project project_name')
                #jenkinsserver.build_job(project_name, {'server_name':'BiddingServer', 'route':'A', 'ring':'ring0'})
                jenkinsserver.build_job(project_name, build_param)
                tmp_status['status'] ='start building'
                logmsg.Publish(opuser, "start building %s"%(project_name,))
                status.append(tmp_status)
                after_last_build_number = jenkinsserver.get_job_info(project_name)['lastBuild']['number']
                while 1>0:
                    if last_build_number == after_last_build_number: 
                        after_last_build_number = jenkinsserver.get_job_info(project_name)['lastBuild']['number']
                        time.sleep(10)
                        continue
                    check_result = check_building(jenkinsserver, project_name, after_last_build_number)
                    logmsg.Publish(opuser, "building : %s" % (after_last_build_number,))
                    if check_result == 'False':
                        break
                    time.sleep(10)

                buildlog=jenkinsserver.get_build_console_output(project_name, after_last_build_number)
                for bl in buildlog.split('\n'):
                    logmsg.Publish(opuser, bl)
                logmsg.Publish(opuser, "The end of %s"%(project_name,))



    else:
        status=[{'status':'fail'}]
    return HttpResponse(json.dumps(status), content_type='application/json')
    #return render_to_response(index.html, status,context_instance=RequestContext(request))


############################################
###         deploy project               ###
############################################
def deploy_project(req):
    deploy_tgt=""
    opuser = req.COOKIES["_adtech_user"]
    if req.method == 'POST':
        if check_online == 'no':
            status=[{'staus':opuser}]
        else:
            online_type = req.POST.get('onlinetype')
            pgname = req.POST.get('pgname')
            server = req.POST.get('server')
            route = req.POST.get('route')
            ring = req.POST.get('ring')

            print 'online_type: %s'%(online_type,)
            print 'pgname: %s'%(pgname,)
            print 'server: %s'%(server,)
            print 'route: %s'%(route,)
            print 'ring: %s'%(ring,)

            if online_type == "on_ring":
                project_name=find_module(server)
                tgt="%s_%s_%s"%(server, route, ring)
                deploy_tgt=tgt.replace('adtech_','')
                deploy_pkg=pgname
            elif online_type == "on_route":
                project_name=find_module(server)
                tgt="%s_%s_%s"%(server, route, 'all')
                deploy_tgt=tgt.replace('adtech_','')
                deploy_pkg=pgname
                #print "deploy_tgt: %s; server: %s; route: %s;"%(online_type, server, route)
            print "deploy_tgt: %s; deploy_pkg: %s"%(deploy_tgt,deploy_pkg)

    

    logger.info('Started deploying %s to %s' % (deploy_pkg, deploy_tgt))
    saltDeploy=SALTDEPLOY()
    DResult = saltDeploy.RunCmd(cmdtarget=deploy_tgt, pkgname=deploy_pkg)
    print type(eval(DResult)['return'])
    #print eval(DResult)['return'][0]
    resultDict = eval(DResult)['return'][0]
    #print resultDict
    for k,v in resultDict.iteritems():
        #print "====================== %s ===========================" % k
        logmsg.Publish(opuser, "="*100)
        logmsg.Publish(opuser, k)
        logger.info(k)
        for msg in v.split('\n'):
            #print msg
            logger.info(msg)
            logmsg.Publish(opuser, "%s"%(msg,))
    status=[{'status':'sccess'}]
    return HttpResponse(json.dumps(status), content_type='application/json')

###################################################
###     show set privilege server list          ###
###################################################
@auth_required
def show_privilege_list(req):
    root=[]
    tmp_root=[]
    fa=[]
    tmp={}
    privilege_list=[]
    deal_server_list=[]
    server_list=get_service_info()
    for line in server_list:
        if line:
            line_tmp = line.strip('/').split('/')
            line_list = line_tmp[:-2]
            if line_list in deal_server_list:
                continue
            server_str="_".join(line_list)
            deal_server_list.append(line_list)
            tmp['server']=server_str
            privilege_list.append(tmp)
            tmp={}
    #print "privilege_list: \n%s"%(privilege_list,)
    return HttpResponse(json.dumps(privilege_list), content_type='application/json')

def record_privilege(req):
    yes_select_server = req.POST['yes_choice_privilege']
    no_select_server = req.POST['no_choice_privilege']
    op_user = req.POST['user']
    print "select server: %s"%(yes_select_server,)
    print "no select server: %s"%(no_select_server,)
    print "op user: %s"%(op_user,)
    return HttpResponse(json.dumps([{'status':'0'}]), content_type='application/json')
    
