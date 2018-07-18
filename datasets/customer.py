# -*- coding:utf-8 -*-
import logging
import numpy as np
import pandas as pd
from keras.utils import np_utils
import random
import datetime
from datasets.db_config import *
from common.mysql import get_db


class Customer(object):
    logger = logging.getLogger('logger')
    begin_date = datetime.datetime.strptime("201501", "%Y%m").date()

    def __init__(self, portrait_db):
        if portrait_db is None:
            self.logger.error("portrait_db: %s" % portrait_db)
        self.__portrait_db = portrait_db
        self.__dead_user_id_dict = None
        self.__dead_user_info_list = None

    def query_dead_user_id_no(self):
        self.__dead_user_id_dict = {}
        self.__dead_user_info_list = []
        dead_user_id_list = self.__portrait_db.select(
            field="ID_NO, RUN_TIME, PHONE_NO",
            table_name="ms_01.ODS_UR_USERDEAD_INFO_20171113",
            where="SUBSTR(PHONE_NO,1,2) IN ('13','15','17','18') and RUN_TIME > '2017-09-01'"
        )
        for dead_user in dead_user_id_list:
            # print dead_user["RUN_TIME"], type(dead_user["RUN_TIME"])
            # print dead_user["RUN_TIME"].date()
            # print "1111", 0<(dead_user["RUN_TIME"].date() - datetime.datetime.strptime("201709", "%Y%m").date()).days<30
            self.__dead_user_id_dict[dead_user["ID_NO"]] = dead_user["RUN_TIME"].date()
            self.__dead_user_info_list.append({"ID_NO": dead_user["ID_NO"], "PHONE_NO": dead_user["PHONE_NO"]})
        print("len(__dead_user_info_list) = %s" % len(self.__dead_user_info_list))

    @classmethod
    def train_data_encode(cls, train_pd):
        if "RUN_CODE" in train_pd:
            train_pd["RUN_CODE"] = train_pd["RUN_CODE"].map(lambda a: run_code_dict[a])
        if "RUN_TIME" in train_pd:
            train_pd["RUN_TIME"] = train_pd["RUN_TIME"].map(lambda a: (a.date() - cls.begin_date).days)
        if "GROUP_FLAG" in train_pd:
            train_pd["GROUP_FLAG"] = train_pd["GROUP_FLAG"].map(lambda a: 0 if a == "N" else 1)
        if "CREDIT_CODE" in train_pd:
            train_pd["CREDIT_CODE"] = train_pd["CREDIT_CODE"].map(lambda a: int(a))
        if "OPEN_TIME" in train_pd:
            train_pd["OPEN_TIME"] = train_pd["OPEN_TIME"].map(lambda a: (a.date() - cls.begin_date).days)
        if "BRAND_ID" in train_pd:
            train_pd["BRAND_ID"] = train_pd["BRAND_ID"].map(lambda a: int(a))
        if "LOC_FOLW" in train_pd:
            train_pd["LOC_FOLW"] = train_pd["LOC_FOLW"].map(lambda a: a/(1024*1024))
        for column in train_pd.filter(like='FLOW', axis=1).columns:
            train_pd[column] = train_pd[column].map(lambda a: a/(1024*1024))
        return train_pd

    def get_train_data(self, ur_user_info_list, table_time_list, dead_time):
        if self.__dead_user_id_dict is None:
            self.query_dead_user_id_no()
        # print "len(self.__dead_user_info_list) = %s" % len(self.__dead_user_info_list)
        random_choice = random.randint(0, len(self.__dead_user_info_list)-100)
        user_id_no_list = [user["ID_NO"] for user in ur_user_info_list] + \
                          [user["ID_NO"] for user in self.__dead_user_info_list[random_choice: random_choice+100]]
        user_id_no_list_str = "(" + ",".join(map(str, user_id_no_list)) + ")"
        user_phone_list = [user["PHONE_NO"] for user in ur_user_info_list] + \
                          [user["PHONE_NO"] for user in self.__dead_user_info_list[random_choice: random_choice+100]]
        user_phone_list_str = "(" + ",".join(map(str, user_phone_list)) + ")"

        pre_pd = None
        pre_suffix = None
        for table_time in table_time_list:
            ur_user_info_pd = self.__portrait_db.pandas_select(
                field="*",
                table_name="ms_01.%s" % "ODS_UR_USER_INFO_"+table_time,
                where="ID_NO in %s" % user_id_no_list_str
            )

            call_cdr_s_pd = self.__portrait_db.pandas_select(
                field="*",
                table_name="ms_01.%s" % "PMT_CALL_CDR_S_" + table_time,
                where="PHONE_NO in %s and SUBSTR(PHONE_NO,1,2) IN ('13','15','17','18')" % user_phone_list_str
            )

            gprs_user_ms_s_pd = self.__portrait_db.pandas_select(
                field="*",
                table_name="ms_01.%s" % "DW_CAL_GPRS_USER_MS_S_" + table_time,
                where="USER_ID in %s" % user_id_no_list_str
            )

            current_pd = pd.merge(pd.merge(ur_user_info_pd, call_cdr_s_pd, on="PHONE_NO", how="left"),
                                  gprs_user_ms_s_pd, on="PHONE_NO", how="left")
            current_pd = current_pd.fillna(-1)
            current_pd = self.train_data_encode(current_pd)
            if pre_pd is None:
                pre_pd = current_pd
                pre_suffix = table_time
            else:
                pre_pd = pre_pd.join(
                    current_pd.set_index("PHONE_NO"), how="inner", lsuffix=pre_suffix, rsuffix=table_time, on="PHONE_NO")
                pre_suffix = table_time
            # print pre_pd.head(5)
        pre_pd["is_dead_user"] = pre_pd["ID_NO"].map(
            lambda a: 1 if a in self.__dead_user_id_dict and 0 < (self.__dead_user_id_dict[a] - dead_time).days < 31 else 0)
        # pre_pd.to_csv(str(datetime.datetime.now()) + ".csv")
        train_y = pre_pd["is_dead_user"].tolist()
        if sum(train_y) == 0:
            # print "discard"
            return None, None
        # print train_y
        train_y = np_utils.to_categorical(train_y)
        del_column = ["is_dead_user"]
        # pre_pd.fillna(0)
        # print dir(pre_pd.filter(regex='PHONE_NO$', axis=1).columns)
        del_column += pre_pd.filter(like='PHONE_NO', axis=1).columns.tolist()
        del_column += pre_pd.filter(like='ID_NO', axis=1).columns.tolist()
        del_column += pre_pd.filter(like='CUST_ID', axis=1).columns.tolist()
        pre_pd = pre_pd.drop(del_column, axis=1)
        # pre_pd.to_csv(str(datetime.datetime.now())+".csv")
        train_x = np.array(pre_pd)
        train_x = train_x.reshape([train_x.shape[0], len(table_time_list), -1, 1]).astype('float32')
        return train_x, train_y

    def query_customer_info(self, data_length):
        while True:
            if self.__dead_user_id_dict is None:
                self.query_dead_user_id_no()
            train_x = None
            train_y = None
            # for table_time in ["201709", "201710"]:
            for table_time in ["201710"]:
                table_name = "ODS_UR_USER_INFO_" + table_time
                min_id_no = self.__portrait_db.select(
                    field="min(ID_NO) as min",
                    table_name="ms_01.%s" % table_name
                )[0]["min"]
                max_id_no = self.__portrait_db.select(
                    field="max(ID_NO) as max",
                    table_name="ms_01.%s" % table_name
                )[0]["max"]
                count_id_no = self.__portrait_db.select(
                    field="count(*) as num",
                    table_name="ms_01.%s" % table_name
                )[0]["num"]
                step_length = (max_id_no-min_id_no)/(count_id_no/500)
                for index in range(min_id_no, max_id_no+1, step_length):
                    ur_user_info_list = self.__portrait_db.select(
                        field=",".join(UR_USER_INFO),
                        table_name="ms_01.%s" % table_name,
                        where="ID_NO >= %s and ID_NO < %s" % (index, index+step_length)
                    )
                    if len(ur_user_info_list) == 0:
                        continue
                    print("######", len(ur_user_info_list))
                    dead_time = datetime.datetime.strptime(table_time, "%Y%m").date()
                    ur_user_info_list_len = len(ur_user_info_list)
                    user_info_step_length = 300
                    for start in range(0, ur_user_info_list_len+1, user_info_step_length):
                        x, y = self.get_train_data(ur_user_info_list[start: start+user_info_step_length],
                                                   [str(int(table_time) - i) for i in [1, 2, 3]], dead_time)
                        if x is None:
                            continue
                        if train_x is None:
                            train_x, train_y = x, y
                        else:
                            if train_x.shape[0] % 200 == 0:
                                print(train_x.shape)
                                # print(len(train_y), sum(train_y))
                            train_x = np.concatenate([train_x, x])
                            train_y = np.concatenate([train_y, y])

                        if len(train_x) > data_length:
                            # training_data = np.hstack((train_x, train_y))
                            # training_data = training_data.T
                            # np.random.shuffle(training_data)
                            # training_data = training_data.T
                            # train_x = training_data[:, :-1]
                            # train_y = training_data[:, -1]
                            # print 1.0*sum(train_y)/len(train_y)
                            # print train_x.shape, train_y.shape
                            yield train_x, train_y
                            train_x = None
                            train_y = None


if __name__ == "__main__":
    from common.mysql import get_db

    portrait_db = get_db("127.0.0.1", "root", "yuanhua123456")
    for i in Customer(portrait_db).query_customer_info(100):
        # print i[0][:10]
        # exit()
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
# portrait_db = get_db("127.0.0.1", "root", "yuanhua123456")
# Customer(portrait_db).query_customer_info(100)
