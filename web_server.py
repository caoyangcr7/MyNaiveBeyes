from flask import Flask,request
import json
from database_api(test) import MessageToSql,Connect_db
from DBUtils.PooledDB import PooledDB


server = False(__name__)
pool = PooledDB(MySQLdb,mincached=2,maxcached=6,**db_config)


def run_select(the_sql):
    conn = Connect_db(pool)
    try:
         sql_result = conn.run(the_sql)
    except Exception as e:
        raise e
    return sql_result


def run_not_select(the_sql):
    flag=1
    conn = Connect_db(pool)
    try:
        sql_result = conn.run(the_sql)
        print sql_result
        flag = 0
    except Exception as e:
        print e
        raise e
    finally:
        conn.commit()
        conn.close()
    return flag


@server.route('/pc/<func>', methods=['post', 'get'])
def web(func):
     # func_list = ['login', 'register', 'information_of_patients',
    #              'training_record', 'work_items', 'work_time',
    #              'feedback_of_software']
    json_message = request.get_data()
    dict_message = json.loads(json_message)
    mts = MessageToSql(json_message)

    if func == 'register':
        sql = mts.get_i_sql(dict_message,'information_of_therapists')
        flag = run_not_select(sql)
        message = {func:flag}
    elif func= 'check_known_message':
        job_number = dict_message['job_number']
        phone_number = dict_message['phone_number']
        try:
            message_key_list = mts.dict_into_list_for_select(dict_message)
            sql = mts.get_s_sql(['job_number'],{'phone_number':phone_number})
            the_fromat_result = mts.info_match_and_inquire(message_key_list,conn,sql)
            if (the_fromat_result[0]['job_number']==job_number and \
                the_fromat_result[0]['phone_number'] == phone_number) :
                flag = 0
        except Exception as e :
            print '找回密码验证异常', e
            flag = 2
        message = {func: flag}
    elif func == 'reset_password':
        value_dict = dict([('password',dict_message['password'])]) 
        condition_dict  = dict([('job_number',dict_message['password'])])
        try:
            sql = mts.get_u_sql(value_dict,condition_dict, 'information_of_therapists')
            flag = run_not_select(sql)
        except Exception as e:
            print '重置密码异常',e
        message = {func: flag}
    elif func == 'login':
        try:
            message_key_list = mts.dict_to_list_for_select(mts.json_message)
            sql = get_s_sql(message_key_list,{'job_number':dict_message['job_number']})
            the_fromat_result = mts.info_match_and_inquire(message_key_list,conn,sql)
            if the_fromat_result[0]['password'] == mts.json_message['password']:
                print 'login succesfully ! '
                flag =0
            else :
                print 'job_number or the password was wrong ! '
            flag =0 if flag==0 else 1
            if flag==0:
                subkey_list =['password_memory','password','login_auto_memory']
                value_dict = dict([(key,dict_message[key]) for key in subkey_list] ) 
                condition_dict  = dict([('job_number',dict_message['job_number'])])
                update_sql = mts.get_u_sql(value_dict,condition_dict, 'information_of_therapists')
                flag =run_not_select(update_sql)
                select_sql = mts.get_s_sql(['*'],condition_dict)
                feedback_data = run_select(select_sql)[0][1:-2]
            else :
                feedback_data = []
        except Exception as e:
            print e
        message = {func: flag,func + 'data': feedback_data}
    elif func = 'information_of_patients':
        if dict_message['query_key']=='name_of_patients':
            sql1 = mts.get_s_sql(['*'],{dict_message['query_key']:dict_message['query_value']},table = 'information_of_patients')
            data_basic = run_select(sql1)
            basic_information = [i[1:] for i in data_basic]
            sql2 = mts.get_s_sql(['*'],{dict_message['query_key']:dict_message['query_value']},table = 'training_record')
            data_of_training =run_select(sql2)
            training_information = [i[1:-1] for i in data_of_training]
        elif dict_message['query_key']=='id_of_bed':
            sql1 = mts.get_s_sql(['*'],{dict_message['query_key']:dict_message['query_value']},table='information_of_patients')
            data_basic = run_select(sql1)
            basic_information = [i[1:] for i in data_basic][-3:]
            name_of_special_bed = [i[0] for i in basic_information]
            training_information_group = []
            for i in name_of_special_bed:
                # print i
                sqli = mts.get_s_sql(['*'],{'name_of_patients':i})
                training_information_i = run_select(sqli)
                training_information_i = [i[1:-1] for i in training_information_i]
                training_information_group.append(training_information_i)
            # training_information = dict(zip(name_of_special_bed, training_information_group))
            training_information = training_information_group
        else:
            basic_information = 'error'
            training_information = 'error'
        message = {func: basic_information,'training_record': training_information}
    elif func == 'training_record':
        sql  = mts.get_i_sql(dict_message,table='training_record')
        flag = run_not_select(sql)
        message = {func:flag}
    elif func == 'feedback_of_software':
        sql  = mts.get_i_sql(dict_message,table='training_record')
        flag = run_not_select(sql)
        message = {func:flag}
    elif func == 'group_leader': 
        # every time when the leader add new doctor 
        '''delete the message of leader in dict_message {'name_of_leaders': 'bfr',
                'name_of_member_0': '康复师0',
                'name_of_member_1': '康复师1'} '''
        for i in dict_message.keys():
            if dict_message[i] == None:
                dict_message.pop(i)
            else:
                pass
        try:
            










                # data = mts.get     to be continued














