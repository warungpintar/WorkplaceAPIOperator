#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:51:45 2019

@author: adamwidibagaskarta
"""

import requests
import json
import pendulum
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class WorkplaceAPIOperator(BaseOperator):
    """Airflow operator for Notify task whether its error or succeed
    
    :param recipientId: workplace id group
    :type recipientId: string
    :param type_user: profile user of operator usually group of people
    :type type_user: string, optional
    :param token: token id for credential in workplace
    :type token: string
    :raises AirflowException: if workplace token id was empty not supplied
    """
    @apply_defaults
    def __init__(self,
                 recipientId,
                 type_user,
                 token,
                 *args, **kwargs):
        """Constructor method
        """
        self.token = token
        super(WorkplaceAPIOperator, self).__init__(*args, **kwargs)
        
        if self.token is None:
            raise AirflowException('No valid workplace token supplied.')
            
    def execute(self,context):
        """failed task notification
        
        :param context: callback context provide by airflow like on_failure_callback or on success callback
        :type context: notificationCallback: function
        """
        ti=context.get('task_instance')
        task=context.get('task_instance').task_id
        dag=context.get('task_instance').dag_id
        exec_date=context.get('execution_date')
        log_url=context.get('task_instance').log_url
        
        #convert
        dt = pendulum.parse(str(exec_date))
        dt = dt.in_tz('Asia/Jakarta')
        exec_date = dt.to_datetime_string()

        message = '''ðŸ”´ Oops Task failed ''' + str(ti) + '''\\n\\n'''
        message += '''âž¡ *Task*: ''' + str(task) +'''\\n'''
        message += '''âž¡ *DAG* : ''' + str(dag) + '''\\n'''
        message += '''âž¡ *Execution Time*: ''' + str(exec_date) + '''\\n'''
        message += '''âž¡ *Log Url*: ''' + str(log_url) + '''\\n'''
            
        session_requests = requests.session()
        WARBOT = "https://api.warungpintar.co/warbot/v1/send?recipent="+self.recipientId+"&type="+self.type_user+"&gitlab_token="+self.token
        session_requests.post(WARBOT, data=json.dumps({"message": message}))
    
    def execute_success(self,context):
        """success task notification
        
        :param context: callback context provide by airflow like on_failure_callback or on_success_callback
        :type context: notificationCallback: function
        """
        dag=context.get('task_instance').dag_id
        exec_date=context.get('execution_date')
        
        #convert
        dt = pendulum.parse(str(exec_date))
        dt = dt.in_tz('Asia/Jakarta')
        exec_date = dt.to_datetime_string()

        message = '''âœ… Congratulation, your DAG succeeded \\n\\n'''
        message += '''âž¡ *DAG* : ''' + str(dag) + '''\\n'''
        message += '''âž¡ *Execution Time*: ''' + str(exec_date) + '''\\n\\n'''
        message += '''Akhirnya bisa tidur dengan nyenyak ðŸ›Œ ðŸ˜´'''
            
        session_requests = requests.session()
        WARBOT = "https://api.warungpintar.co/warbot/v1/send?recipent=4387182371307936"+"&type="+self.type_user+"&gitlab_token="+self.token
        session_requests.post(WARBOT, data=json.dumps({"message": message}))
    
    def check_params(self):
        """attribute for debugging by checking parameter of object
        
        :return: string text of token recipientId and type_user
        :rtype: string
        """
        return print(self.token + self.recipientId + self.type_user)
        
class WorkplaceAPIPostOperator(WorkplaceAPIOperator):
    """just inherit from WorkplaceAPIOperator countering airflow bugs
    
    :param recipientId: workplace id group
    :type recipientId: string
    :param type_user: profile user of operator usually group of people
    :type type_user: string, optional
    :param token: token id for credential in workplace
    :type token: string
    """
    
    @apply_defaults
    def __init__(self,
                 recipientId,
                 type_user,
                 token,
                 **kwargs):
        """Constructor method
        """
        self.recipientId = recipientId
        self.type_user = type_user
        self.token = token

        super(WorkplaceAPIPostOperator, self).__init__( recipientId=self.recipientId,
                                                        type_user = self.type_user,
                                                        token = self.token,
                                                        **kwargs)