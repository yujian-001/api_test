#coding=utf-8
import os
import sys
import shutil
import time
import json
import traceback
from dataInterface.functions import CFunction
from dataInterface.db.params import CPgSqlParam
from appsUtils.appInterfaceApi import AppApi
from appsUtils import proxyUtil

PATH = os.environ["BASE_DIR"] + '/logs/bsa_tsa.install.log'

def write_info(info=''):
    fp = open(PATH, 'a')
    if not info :
        info = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    else :
        info += "\n" + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    fp.write(info)
    fp.write('\n')
    fp.close()

cur_path = os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
dst_path = sys.argv[1]
is_update = sys.argv[2]

app_folder = 'bsa_tsa'
appApi = AppApi()

def main() :
    src_path = os.path.normpath(cur_path + os.sep + app_folder)
    shutil.copytree(src_path, dst_path)
    write_info('---------------install success!')

class Updater(object):
    def __init__(self, src_path, dst_path):
        self.src_path = src_path
        self.dst_path = dst_path
        #需要进行替换的文件夹和文件
        self.replace_folders = [
            "assetaccount", "bin", "conf", "plugins", "sql",\
            "static", "tass_modules", "tsaglobal", "webapp_demo", "cur_views", "cur_models", "data_outgoing"
        ]
        self.new_folders = [
            "datasource", "message_gateway", "sso"
        ]
        self.replace_files = [
            "__init__.py", "assetAnalysis.py", "assetOverview.py",\
            "models.py", "Top10Models.py", "urls.py",\
            "validation.py", "views.py", "datasourceUtil.py", "ataglobal.py",
            "sms_gateway_interface_view.py"
        ]

    def backup(self):
        try:
            backpath = os.environ["BASE_DIR"] + "/backapp"
            if not os.path.exists(backpath):
                os.mkdir(backpath)
            backup_filename = '%s/%s.%s.%d'%(backpath,app_folder,time.strftime("%Y%m%d", time.localtime(time.time())),\
                int(time.time()),)
            shutil.copytree(self.dst_path, backup_filename)
            self.backup_filename = backup_filename
        except Exception:
            write_info("error : can not backup app")
            return False

        return True

    def replace_folder(self):
        try:
            for item in self.replace_folders:
                src_folder = os.path.normpath(self.src_path + "/" + item)
                dst_folder = os.path.normpath(self.dst_path + "/" + item)
                shutil.rmtree(dst_folder)
                shutil.copytree(src_folder, dst_folder)

                write_info("copy folder %s -> %s"%(src_folder, dst_folder,))
            
            for item in self.new_folders:
                src_folder = os.path.normpath(self.src_path + "/" + item)
                dst_folder = os.path.normpath(self.dst_path + "/" + item)
                if not os.path.exists(dst_folder):
                    shutil.copytree(src_folder, dst_folder)
                    write_info("copy folder %s -> %s"%(src_folder, dst_folder,))

        except Exception, e:
            write_info(traceback.format_exc())
            raise e

    def replace_file(self):
        try:
            for item in self.replace_files:
                src_file = os.path.normpath(self.src_path + "/" + item)
                dst_file = os.path.normpath(self.dst_path + "/" + item)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                if os.path.exists(dst_file+"c"):
                    os.remove(dst_file+"c")
                if os.path.exists(src_file+"c"):
                    src_file = src_file+"c"
                    dst_file = dst_file+"c"
                    shutil.copy(src_file, dst_file)
                else:
                    shutil.copy(src_file, dst_file)

                write_info("copy file %s -> %s"%(src_file, dst_file,))
        except Exception, e:
            write_info(traceback.format_exc())
            raise e

    def update_conf(self):
        try:
            dst_conf_path = self.dst_path + "/conf/"
            backup_conf_path = self.backup_filename + "/conf/"
            conf_files_and_dirs = os.listdir(dst_conf_path)
            reserve_conf_files = []
            reserve_conf_dirs = []
            for item in conf_files_and_dirs:
                if os.path.isfile(dst_conf_path + item):
                    reserve_conf_files.append(item)
                elif os.path.isdir(dst_conf_path + item):
                    reserve_conf_dirs.append(item)

            # 使用备份的conf文件写回新配置文件
            for conf_file in reserve_conf_files:
                # app.conf和buildversion始终保持最新配置
                if conf_file in ["app.conf", "buildversion"]:
                    continue
                backup_srcfile = backup_conf_path + conf_file
                conf_dstfile = dst_conf_path + conf_file
                if os.path.exists(backup_srcfile):
                    shutil.copy(backup_srcfile, conf_dstfile)
                    write_info("reserve conf %s" % conf_dstfile)
            for conf_dir in reserve_conf_dirs:
                backup_srcdir = backup_conf_path + conf_dir
                conf_dstdir = dst_conf_path + conf_dir
                if os.path.exists(backup_srcdir):
                    shutil.rmtree(conf_dstdir, ignore_errors=True)
                    shutil.copytree(backup_srcdir, conf_dstdir)
                    write_info("reserve conf dir %s" % conf_dstdir)
        except Exception, e:
            write_info(traceback.format_exc())
            raise e

    def update_table(self):
        try:
            sql = '''
            create table if not exists internal_app_bsatsa.web_threat_score(
            uuid varchar(32) primary key,
            score float
            );
            create table if not exists internal_app_bsatsa.web_risk_score(
            uuid varchar(32) primary key,
            website varchar(256),
            score float
            );
            create table if not exists internal_app_bsatsa.web_global_score(
            key varchar(32) primary key,
            score float
            );
            CREATE OR REPLACE FUNCTION get_website(url text) RETURNS text AS $$
            DECLARE
                proto text;
                domain text;
            BEGIN
                url := lower(url);
                proto := lower(substring(url,0,position(':' in url)));
                domain := replace(url,proto||'://','');
                if position('/' in domain) > 0 then
                    domain := substring(domain,0,position('/' in domain));
                end if;
                if position(':' in domain) = 0 then
                    if proto = 'http' then
                        domain := domain||':80';
                    elsif proto = 'https' then
                        domain := domain||':443';
                    end if;
                end if;
                return lower(proto)||'://'||domain;
            END;
            $$ LANGUAGE plpgsql;
            create table if not exists internal_app_bsatsa.nti_event(
                serial_id  bigserial,
                appid int,
                sequence_id uuid,
                key text,
                value text,
                type int,
                is_detail boolean,
                is_realtime int,
                is_back int,
                id bigint,
                timestamp bigint,
                tidy_info json
            );
            CREATE TABLE IF NOT EXISTS internal_app_bsatsa.nti_vuls(
            id bigserial primary key,
            nsfocus_id varchar(255),
            confidentiality varchar(255),
            update_time varchar(32),
            updated_time varchar(32),
            solution text,
            create_time varchar(32),
            created_time varchar(32),
            heat_level varchar(32),
            threat_level varchar(32),
            integrity varchar(255),
            availability varchar(255),
            cve_id varchar(32),
            cpe_full text,
            threat_type varchar(255),
            vuln_desc text,
            poc varchar(32),
            source text,
            authentication varchar(255),
            type varchar(255),
            cvss varchar(32),
            refer text,
            product varchar(255),
            vendor varchar(255),
            data_type varchar(255),
            nti_vul_id varchar(255),
            source_url text,
            heat varchar(255),
            name text,
            level varchar(255),
            modified varchar(255),
            complexity varchar(255),
            other_id varchar(255),
            published varchar(255),
            affected_version text
            );
            CREATE TABLE IF NOT EXISTS internal_app_bsatsa.vul_relate_assets(
            cve_id varchar(32),
            asset_id varchar(32)
            );
            '''

            CFunction.execute(CPgSqlParam(sql))
            write_info("update pg")
        except Exception, e:
            write_info(traceback.format_exc())
            raise e

    def set_proxypass(self):
        """
        F02平台升级包替换了apache的配置文件，
        将TSA设置的代理弄丢了，在此加一下
        """
        proxypass_infos = [
            '/vulnerabilityApp https://%s/vulnerabilityApp',
            '/api/v1/vuls https://%s/api/v1/vuls',
        ]
        sql = "SELECT ip FROM internal_app_bsatsa.register_ip"
        rows = json.loads(CFunction.execute(CPgSqlParam(sql)))
        if rows:
            register_ip = rows[0][0]
        else:
            write_info('register_ip table is NULL')
            return
        for proxypass in proxypass_infos:
            new_proxypass = proxypass % register_ip
            if not proxyUtil.checkPrxoyInfoIsExit(new_proxypass):
                rtn = proxyUtil.addProxyPassInfo(new_proxypass)
                write_info('add proxypass, %s, rtn: %s' % (new_proxypass, rtn))
            else:
                write_info('proxypass is exists, %s' % new_proxypass)
        return

    def update(self):
        if self.backup():
            self.replace_folder()
            self.replace_file()
            self.update_conf()
            self.update_table()
            self.set_proxypass()
        else:
            restart_app()
            sys.exit(3)

    def rollback(self):
        try:
            shutil.rmtree(self.dst_path)
            shutil.copytree(self.backup_filename, self.dst_path)
            write_info("rollback app folder")

            sql = "drop table if exists internal_app_bsatsa.web_threat_score;"
            sql += "drop table if exists internal_app_bsatsa.web_risk_score;"
            sql += "drop table if exists internal_app_bsatsa.web_global_score;"
            sql += "drop function if exists get_website(url text);"
            sql += "drop table if exists internal_app_bsatsa.nti_event;"
            sql += "drop table if exists internal_app_bsatsa.nti_vuls;"
            sql += "drop table if exists internal_app_bsatsa.vul_relate_assets;"
            CFunction.execute(CPgSqlParam(sql))

            #启动应用
            restart_app()

            write_info("rollback pg")
        except Exception, e:
            write_info(traceback.format_exc())
    
def main_update() :
    if os.path.exists(dst_path):
        src_path = os.path.normpath(cur_path+os.sep+app_folder)
        #检查原来的app版本号
        if appApi.get_app_version(app_folder) == "2.1.0":
        # if appApi.get_app_version(app_folder):
            global oldversion
            oldversion = appApi.get_app_version(app_folder)

            updater = Updater(src_path, dst_path)
            try:
                updater.update()
            except Exception,e:
                write_info(traceback.format_exc())
                updater.rollback()
                sys.exit(3)
        else:
            #如果已安装版本比当前版本相同或更高，则升级程序退出
            write_info("Cannot upgrade lower or equal version app.")
            #启动应用
            restart_app()
            sys.exit(6)
    else:
        main()

def CalWight(VerToCalStr):
    ''' calculate version weight used to compare.'''
    import re
    try:
        '''
        satisfy: V2.0R00F00SP01\V2.0\V2.0R00\F00V2.0\SP01V2.0\SP01F00...
        '''
        v = re.search("(?<=V).*?((?=R)|(?=F)|(?=SP)|$)",VerToCalStr)

        vVal = float(v.group()) if v is not None and len(v.group())!= 0 else 0

        r = re.search("(?<=R).*?((?=V)|(?=F)|(?=SP)|$)",VerToCalStr)

        rVal = float(r.group()) if r is not None and len(r.group())!= 0 else 0

        f = re.search("(?<=F).*?((?=V)|(?=R)|(?=SP)|$)",VerToCalStr)

        fVal = float(f.group()) if f is not None and len(f.group())!= 0 else 0

        sp = re.search("(?<=SP).*?((?=V)|(?=R)|(?=F)|$)",VerToCalStr)

        spVal = float(sp.group()) if sp is not None and len(sp.group())!= 0 else 0

        wgt = long(vVal*1000000000000000000)+long(rVal*100000000000000)+long(fVal*1000000000000)+long(spVal*100000)
        return wgt

    except Exception,e:
        raise e


def VersionCompare(VertoCmpStr):
    '''
    compare to given contrast_version (style:'V2.0R32F15SP01.2345'),
    Return True if local version is not lower than contrast_version, False otherwise. 
    '''
    from appsUtils import env
    try:
        #V2.0R00F03
        LocalVersion = env.get_bsa_product_version();
        lwgt = CalWight(LocalVersion)
        cwgt = CalWight(VertoCmpStr)
        return lwgt >= cwgt

    except Exception,e:
        raise e

def restart_app():
    updatesql = CPgSqlParam("update tb_menu set isenable=1 where foldername='%s'"%(app_folder,))
    CFunction.execute(updatesql)
    startscript_path = os.path.normpath(dst_path + "/bin/start.py")
    os.system("python "+startscript_path)
    
if __name__ == '__main__':
    try:
        from appManager import utils
        from appsUtils import env
        import re
        #V2.0R00F00SP01.3456
        #versionlist=['2.0', '00', '00', '01']
        if VersionCompare('V2.0R00F03'):
            pass
        else:
            sys.exit(2)
        #检测证书
        setup_api = utils.AppSetupManagerApi()
        if not setup_api.check_app_is_licenced(app_folder):
            sys.exit(1)
        if is_update=='0':
            main()
            print 'install'
            sys.exit(0)
        elif is_update=='1':
            main_update()
            print 'update '
            sys.exit(0)
        else: 
            pass
            

    except Exception, e:
        #启动应用
        restart_app()
        write_info(traceback.format_exc())
        sys.exit(3)
