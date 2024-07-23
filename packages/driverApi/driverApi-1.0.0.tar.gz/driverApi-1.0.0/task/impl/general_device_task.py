# author: haoliqing
# date: 2023/9/22 10:11
# desc:
import traceback

from model.task_model.device_task import DeviceTask
from model.task_model.base_task import TaskStatus, TaskRetryType
from model.task_model.step_model import Step
from model.task_model.step_model.step_result import StepResult, StepStatus
from model.task_model.response.response import ResponseState
from logger.device_logger import logger
import time


class GeneralDeviceTask(DeviceTask):
    step_index: int = 0

    def execute(self):
        if self.status == TaskStatus.HALT:
            # 挂起状态下不执行，等待外部触发
            time.sleep(0.5)
            return
        step = self.__get_current_step()
        if step:
            result: StepResult = StepResult(step.id)
            logger.info("[请求ID：{0}]执行任务{1}，步骤{2}".format(self.request_context.request_id, self.id, step.id))
            try:
                step.execute(self.request_context, result)
                self.request_context.last_step_result = result
            except Exception as e:
                logger.error("[请求ID：{0}]执行外设调用任务{1}，步骤{2}时发生异常: {3}, 异常信息：{4}"
                             .format(self.request_context.request_id, self.id, step.id, str(e), traceback.format_exc()))
                result.status = StepStatus.FAIL
                result.data = "发生未知异常"
            self.__handle_step_result(result)
        else:
            # 没有后续步骤则认为任务执行完成
            self.__on_task_success()

    def __handle_step_result(self, result: StepResult):
        if result.status == StepStatus.SUCCESS:
            logger.info("[请求ID：{0}]任务{1}，步骤{2} 执行完成"
                        .format(self.request_context.request_id, self.id, result.step_id))
            self.step_index += 1
        elif result.status == StepStatus.FAIL:
            logger.error("[请求ID：{0}]任务{1}，步骤{2}执行错误,错误信息：{3}"
                         .format(self.request_context.request_id, self.id, result.step_id, result.data))
            if self.__on_step_fail(result):
                if self.is_manual_retry_on_halt():
                    self.__on_task_halt()
                else:
                    self.__on_task_fail()

    def __on_task_success(self):
        self.status = TaskStatus.SUCCESS
        self.request_context.get_response().state = ResponseState.SUCCESS
        if self.task_notifier:
            self.task_notifier.on_success(self.request_context)

    def __on_task_fail(self):
        if self.reset_step:
            reset_result: StepResult = StepResult(self.reset_step.id)
            self.reset_step.execute(self.request_context, reset_result)
        self.status = TaskStatus.FAIL
        self.request_context.get_response().state = ResponseState.FAIL
        if self.request_context.last_step_result:
            self.request_context.get_response().ret_code = self.request_context.last_step_result.code
            self.request_context.get_response().ret_msg = self.request_context.last_step_result.data
        if self.task_notifier:
            self.task_notifier.on_fail(self.request_context)

    def __on_task_halt(self):
        self.status = TaskStatus.HALT
        if self.task_notifier:
            self.task_notifier.on_halt(self.request_context)

    def __on_step_fail(self, step_ret: StepResult) -> bool:
        """
        :param step_ret:
        :return: 任务是否失败
        """
        if self.status == TaskStatus.CANCEL:
            return True
        if self.is_auto_retry_on_halt() and self.auto_retry_num > 0:
            logger.info("[请求ID：{0}]任务{1}，步骤{2} 剩余可自动重试次数{3}，执行自动重试"
                        .format(self.request_context.request_id, self.id, step_ret.step_id, self.auto_retry_num))
            self.auto_retry_num -= 1
            return False
        return True

    def __get_current_step(self) -> Step:
        if self.steps and len(self.steps) > self.step_index:
            return self.steps[self.step_index]
        else:
            return None

    def restart_task(self):
        self.status = TaskStatus.RUN

    def finish_task(self):
        self.__on_task_fail()
