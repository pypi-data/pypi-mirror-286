from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

class Slack_Alert:
    def slack_fail_alert(self, context):
        fail_alert = SlackWebhookOperator(
            task_id='fail_notification',
            slack_webhook_conn_id='slack_conn',
            channel='airflow_notifier',
            message="""
                channel
                :red_circle: Task Failed. 
                *Task*: {task}  
                *Dag*: {dag} 
                *Execution Time*: {exec_date}  
                *Log Url*: {log_url} 
                """.format(
                task=context.get('task_instance').task_id,
                dag=context.get('task_instance').dag_id,
                ti=context.get('task_instance'),
                exec_date=context.get('execution_date'),
                log_url=context.get('task_instance').log_url,
            )
        )
        return fail_alert.execute(context=context)
