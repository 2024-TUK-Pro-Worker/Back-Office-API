import os
import time
import yaml
from kubernetes import utils
from kubernetes import config
from kubernetes import client as kubernetes_client
from app.Model.Account.Schedule import Schedule as scheduleModel


def getJobScheduleInfo(uuid):
    try:
        return scheduleModel().getSchedule(uuid)
    except:
        return {'uuid': uuid, 'cron_schedule': '*/20 * * * *'}


def setJobScheduleInfo(uuid, cron_schedule):
    try:
        scheduleModel().setSchedule(uuid, cron_schedule)
        return True
    except:
        return False


def getSchedulerStatus(uuid):
    try:
        config.load_kube_config('Config/Kubernetes/kube.yaml')

        k8s_batch_client = kubernetes_client.BatchV1Api()

        try:
            return k8s_batch_client.read_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE')).status
        except:
            return None
    except:
        return None


def createScheduler(uuid):
    try:
        scheduleInfo = getJobScheduleInfo(uuid)

        return __createCronjob(uuid, scheduleInfo['cron_schedule'])
    except:
        return False


def deleteScheduler(uuid):
    try:
        return __deleteCronjob(uuid)
    except:
        return False


def __createCronjob(uuid, schedule='*/20 * * * *'):
    config.load_kube_config('Config/Kubernetes/kube.yaml')

    k8s_client = kubernetes_client.api_client.ApiClient()
    k8s_batch_client = kubernetes_client.BatchV1Api()

    try:
        k8s_batch_client.read_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
        alreadyCreated = True
    except:
        alreadyCreated = False

    if alreadyCreated:
        k8s_batch_client.delete_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
        # 동작하고 있는 스케줄러가 종료 될 때까지 대기
        time.sleep(5)

    with open("Config/Kubernetes/BaseCronjob.yaml") as f:
        cronjob_yaml = yaml.safe_load(f)
        f.close()

    # cronjob 세부 설정
    cronjob_yaml['metadata']['name'] = uuid
    cronjob_yaml['spec']['schedule'] = schedule
    cronjob_yaml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['image'] = os.getenv(
        'K8S_DOCKER_IMAGE')
    cronjob_yaml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['volumeMounts'][0]['mountPath'] = \
        cronjob_yaml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['volumeMounts'][0][
            'mountPath'].replace('{UUID}', uuid)
    for env in cronjob_yaml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['env']:
        if env['name'] == 'UUID':
            env['value'] = uuid
        elif env['name'] == 'RESOURCE_PATH':
            env['value'] = './Resource'
        else:
            env['value'] = os.getenv(env['name'])

    utils.create_from_yaml(k8s_client, yaml_objects=[cronjob_yaml], namespace="default")

    try:
        k8s_batch_client.read_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
        return True
    except:
        return False


def __deleteCronjob(uuid):
    config.load_kube_config('Config/Kubernetes/kube.yaml')

    k8s_batch_client = kubernetes_client.BatchV1Api()

    try:
        k8s_batch_client.read_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
        alreadyCreated = True
    except:
        return True

    if alreadyCreated:
        k8s_batch_client.delete_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))

    try:
        k8s_batch_client.read_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
        return False
    except:
        return True