# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from typing import List

from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.finance_ic_card_rwer import FinanceICCardRWer, FinanceICInfo, DetailInfo, TranInfo
import time


class ReadFinanceICCardStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        ic_reader: FinanceICCardRWer = context.get_device()
        if not ic_reader:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        tran_info: TranInfo = TranInfo()
        tran_info.tran_amt = context.get_request_param_data("tranAmt")
        tran_info.tran_ccy = context.get_request_param_data("tranCcy")
        tran_info.tran_type = context.get_request_param_data("tranType")
        tran_info.org_name = context.get_request_param_data("orgName")
        tran_info.inputAid = context.get_request_param_data("inputAid")
        tran_info.tran_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        tran_info.tran_time = time.strftime('%H%M%S', time.localtime(time.time()))

        ic_info: FinanceICInfo = ic_reader.read_finance_ic_info(tran_info)
        if ic_info and ic_info.err_code >= 0:
            self.__set_ret_value(context, "cardNoID", ic_info.card_no)
            self.__set_ret_value(context, "cardSerialNoID", ic_info.card_serial_no)
            self.__set_ret_value(context, "ownerNameID", ic_info.owner_name)
            self.__set_ret_value(context, "certTypeID", ic_info.cert_type)
            self.__set_ret_value(context, "certNoID", ic_info.cert_no)
            self.__set_ret_value(context, "balanceID", ic_info.balance)
            self.__set_ret_value(context, "ccyID", ic_info.ccy)
            self.__set_ret_value(context, "arqcID", ic_info.arqc)
            self.__set_ret_value(context, "issueBankDataID", ic_info.issue_branch_data)
            self.__set_ret_value(context, "balanceLimitID", ic_info.balance_limit)
            self.__set_ret_value(context, "singleLimitID", ic_info.single_limit)
            self.__set_ret_value(context, "aidID", ic_info.aid)
            self.__set_ret_value(context, "arqcSourceID", ic_info.arqc_source)
            self.__set_ret_value(context, "tranCounterID", ic_info.tran_counter)
            self.__set_ret_value(context, "verifyResultID", ic_info.verify_result)
            self.__set_ret_value(context, "arqcOnlyID", ic_info.arqc_only)
            self.__set_ret_value(context, "track2DataID", ic_info.track2Data)
            self.__set_ret_value(context, "effectiveDateID", ic_info.effective_date)
            self.__set_ret_value(context, "overdueDateID", ic_info.overdue_date)
            self.__set_ret_value(context, "pbocVerID", ic_info.pboc_ver.value)
            if context.get_request_param_data("tranDetailID"):
                self.__create_tran_detail_info(context, ic_info)
            if context.get_request_param_data("creditDetailID"):
                self.__create_credit_detail_info(context, ic_info)
            context.get_response().ret_code = str(ic_info.err_code)
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.code = ic_info.err_code
            result.data = "读取IC卡信息失败"
            return

    def __set_ret_value(self, context: DeviceRequestContext, param_id, value):
        if context.get_request_param_data(param_id):
            context.get_response().add_response_value(context.get_request_param_data(param_id), value)

    def __create_tran_detail_info(self, context: DeviceRequestContext, ic_info: FinanceICInfo):
        """构建交易日志信息"""
        tran_detail: List[DetailInfo] = ic_info.tran_detail
        details = []
        if tran_detail and len(tran_detail) > 0:
            for detail_info in tran_detail:
                detail: dict = {}
                self.__set_detail_value(context, detail, "detailCcyID", detail_info.ccy)
                self.__set_detail_value(context, detail, "detailAuthAmtID", detail_info.auth_amt)
                self.__set_detail_value(context, detail, "detailOtherAmtID", detail_info.other_amt)
                self.__set_detail_value(context, detail, "detailTranDateID", detail_info.tran_date)
                self.__set_detail_value(context, detail, "detailTranTimeID", detail_info.tran_time)
                self.__set_detail_value(context, detail, "detailTranTypeID", detail_info.tran_type)
                self.__set_detail_value(context, detail, "detailOrgNameID", detail_info.org_name)
                self.__set_detail_value(context, detail, "detailCountryID", detail_info.country)
                self.__set_detail_value(context, detail, "detailCounterAppID", detail_info.counter_app)
                details.append(detail)
        context.get_response().add_response_value(context.get_request_param_data("tranDetailID"), details)

    def __create_credit_detail_info(self, context: DeviceRequestContext, ic_info: FinanceICInfo):
        """构建圈存明细信息"""
        credit_details = []
        if ic_info.credit_detail and len(ic_info.credit_detail) > 0:
            for credit_info in ic_info.credit_detail:
                detail: dict = {}
                self.__set_detail_value(context, detail, "creditBeforeAmtID", credit_info.before_amt)
                self.__set_detail_value(context, detail, "creditAfterAmtID", credit_info.after_amt)
                self.__set_detail_value(context, detail, "creditTranDateID", credit_info.tran_date)
                self.__set_detail_value(context, detail, "creditTranTimeID", credit_info.tran_time)
                self.__set_detail_value(context, detail, "creditOrgNameID", credit_info.org_name)
                self.__set_detail_value(context, detail, "creditCountryID", credit_info.country)
                self.__set_detail_value(context, detail, "creditCounterAppID", credit_info.counter_app)
                credit_details.append(detail)

        context.get_response().add_response_value(context.get_request_param_data("creditDetailID"), credit_details)

    def __set_detail_value(self, context: DeviceRequestContext, detail: dict, param_id, value):
        if context.get_request_param_data(param_id):
            detail[context.get_request_param_data(param_id)] = value
