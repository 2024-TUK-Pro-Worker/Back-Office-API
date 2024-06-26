# Python 모듈
import os
import yaml
from kubernetes import utils
from kubernetes import config
from kubernetes import client as kubernetes_client

# 소스 파일 선언
from Model.Auth.User import User as userModel
from Model.Account.Schedule import Schedule as scheduleModel


def getJobScheduleInfo(uuid):
    try:
        return scheduleModel().getSchedule(uuid)
    except:
        return None


def setJobScheduleInfo(uuid, cronSchedule):
    try:
        return scheduleModel().setSchedule(uuid, cronSchedule)
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

        if scheduleInfo is None:
            raise 'jobschedule info call fail'

        userInfo = userModel().getUser(uuid)

        if userInfo['trial'] == 'Y':
            if userInfo['trialCount'] < 1:
                raise Exception('trial is end')

            trialPodCreateResult = __createTrialDeployment(uuid)

            if trialPodCreateResult:
                userModel().minusTrialCount(uuid)

            return trialPodCreateResult
        else:
            return __createCronjob(uuid, scheduleInfo['cronSchedule'])
    except Exception as e:
        return {
            'result': False,
            'message': e if e is not None else 'scheduler create fail'
        }


def deleteScheduler(uuid):
    try:
        return __deleteCronjob(uuid)
    except:
        return {
            'result': False,
            'message': 'scheduler delete fail'
        }


def __createCronjob(uuid, schedule='*/20 * * * *'):
    config.load_kube_config('Config/Kubernetes/kube.yaml')

    k8s_client = kubernetes_client.api_client.ApiClient()
    k8s_batch_client = kubernetes_client.BatchV1Api()

    try:
        k8s_batch_client.read_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
        k8s_batch_client.delete_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
    except Exception as e:
        exceptReson = e.__dict__
        if exceptReson['status'] != 404:
            return {
                'result': False,
                'message': 'scheduler recreate fail'
            }

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
    cronjob_yaml['spec']['jobTemplate']['spec']['template']['spec']['volumes'][0]['hostPath']['path'] = \
        cronjob_yaml['spec']['jobTemplate']['spec']['template']['spec']['volumes'][0]['hostPath']['path'].replace(
            '{UUID}', uuid)

    for env in cronjob_yaml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['env']:
        if env['name'] == 'UUID':
            env['value'] = uuid
        elif env['name'] == 'RESOURCE_PATH':
            env['value'] = f'./Resource'
        else:
            env['value'] = os.getenv(env['name'])

    utils.create_from_yaml(k8s_client, yaml_objects=[cronjob_yaml], namespace="default")

    try:
        k8s_batch_client.read_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
        return {
            'result': True
        }
    except:
        return {
            'result': False,
            'message': 'scheduler create fail'
        }

def __createTrialDeployment(uuid):
    config.load_kube_config('Config/Kubernetes/kube.yaml')

    k8s_client = kubernetes_client.api_client.ApiClient()
    k8s_pod_client = kubernetes_client.CoreV1Api()

    with open("Config/Kubernetes/TrialDeployment.yaml") as f:
        trialYaml = yaml.safe_load(f)
        f.close()

    trialYaml['metadata']['name'] = f'{uuid}-trial'
    trialYaml['spec']['containers'][0]['image'] = os.getenv('K8S_DOCKER_IMAGE')
    trialYaml['spec']['containers'][0]['volumeMounts'][0]['mountPath'] = trialYaml['spec']['containers'][0]['volumeMounts'][0]['mountPath'].replace('{UUID}', uuid)
    trialYaml['spec']['volumes'][0]['hostPath']['path'] = trialYaml['spec']['volumes'][0]['hostPath']['path'].replace('{UUID}', uuid)

    for env in trialYaml['spec']['containers'][0]['env']:
        if env['name'] == 'UUID':
            env['value'] = uuid
        elif env['name'] == 'RESOURCE_PATH':
            env['value'] = f'./Resource'
        else:
            env['value'] = os.getenv(env['name'])

    utils.create_from_yaml(k8s_client, yaml_objects=[trialYaml], namespace="default")

    try:
        k8s_pod_client.read_namespaced_pod(f'{uuid}-trial', os.getenv('K8S_NAMESPACE'))
        return {
            'result': True
        }
    except:
        return {
            'result': False,
            'message': 'trial pod create fail'
        }


def __deleteCronjob(uuid):
    config.load_kube_config('Config/Kubernetes/kube.yaml')

    k8s_batch_client = kubernetes_client.BatchV1Api()

    try:
        k8s_batch_client.read_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
    except:
        return {
            'result': False,
            'message': 'already scheduler deleted'
        }

    try:
        k8s_batch_client.delete_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))
    except:
        return {
            'result': False,
            'message': 'scheduler delete fail'
        }

    try:
        k8s_batch_client.read_namespaced_cron_job(uuid, os.getenv('K8S_NAMESPACE'))

        return {
            'result': False,
            'message': 'scheduler delete fail'
        }
    except:
        return {
            'result': True
        }
