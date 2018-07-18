Table_list = ["ODS_UR_USERDEAD_INFO_20171113", "ODS_UR_USER_INFO_201706", "ODS_UR_USER_INFO_201707",
              "ODS_UR_USER_INFO_201708", "ODS_UR_USER_INFO_201709", "ODS_UR_USER_INFO_201710", "PMT_CALL_CDR_S_201706",
              "PMT_CALL_CDR_S_201707", "PMT_CALL_CDR_S_201708", "PMT_CALL_CDR_S_201709",
              "PMT_CALL_CDR_S_201710"]

UR_USER_INFO = ["ID_NO", "RUN_CODE", "CUST_ID", "PHONE_NO", "RUN_TIME", "OWNER_TYPE", "GROUP_FLAG", "CREDIT_CODE",
                "LIMIT_OWE", "OPEN_TIME", "CARD_TYPE"]

CALL_CDR_S = ["PHONE_NO", "T_Z_DURATION", "T_Z_FEE", "T_B_DURATION", "T_B_FEE", "ALL_Z_COUNT", "ALL_B_COUNT"]
CAL_GRPS_USER_MS_S = ["USER_ID", "PHONE_NO", "CITY_ID", "BRAND_ID",
                      "GPRS_TD_FLOW", "PHONE_FLOW", "PHONE_TD_FLOW", "FLOW",
                      "TIMES", "DUR", "FEE", "CFEE",
                      "BILL_FLOW", "BILL_UP_FLOW", "BILL_DOWN_FLOW", "LOC_FOLW",
                      "LOC_DUR", "LOC_TIMES", "UP_FLOW", "DOWN_FLOW",
                      "BUSY_FLOW", "BUSY_GSM_FLOW", "BUSY_TD_FLOW", "BUSY_4G_FLOW",
                      "IDLE_FLOW", "IDLE_GSM_FLOW", "IDLE_TD_FLOW", "IDLE_4G_FLOW",
                      "CMNET_UP_FLOW", "CMNET_DOWN_FLOW", "CMNET_TIMES", "CMWAP_UP_FLOW",
                      "CMWAP_DOWN_FLOW", "CMWAP_TIMES", "TD_FLOW", "TD_UP_FLOW",
                      "TD_DOWN_FLOW", "TD_DUR", "TD_TIMES", "TD_FEE",
                      "GSM_FLOW", "GSM_UP_FLOW", "GSM_DOWN_FLOW", "GSM_DUR",
                      "GSM_TIMES", "GSM_FEE", "G4_FLOW", "G4_UP_FLOW",
                      "G4_DOWN_FLOW", "G4_DUR", "G4_TIMES", "G4_FEE",
                      "ROAM_FLOW", "ROAM_UP_FLOW", "ROAM_DOWN_FLOW", "ROAM_INTL_FLOW",
                      "ROAM_PROV_FLOW", "ROAM_DOMST_FLOW", "ROAM_INTL_BILL_FLOW", "ROAM_PROV_BILL_FLOW",
                      "ROAM_DOMST_BILL_FLOW", "ROAM_TIMES", "ROAM_TD_TIMES", "ROAM_GSM_TIMES",
                      "ROAM_INTER_TIMES", "ROAM_LOC_TIMES", "ROAM_LAND_TIMES", "ROAM_INTER_FEE",
                      "ROAM_LOC_FEE", "ROAM_LAND_FEE", "ROAM_INTER_CFEE", "ROAM_LOC_CFEE",
                      "ROAM_LAND_CFEE", "MMS_CONTENT_FLOW", "OTHER_CONTENT_FLOW", "OTHER_CONTENT_2G_FLOW",
                      "OTHER_CONTENT_3G_FLOW", "TALK_FLOW", "TALK_UP_FLOW", "TALK_DOWN_FLOW",
                      "MAS_FLOW", "MAS_UP_FLOW", "MAS_DOWN_FLOW", "PHONE_4G_FLOW"]
run_code_dict = {
    "A": 0, "B": 1, "C": 2, "D": 3, "F": 4, "G": 5, "H": 6, "I": 7, "J": 8, "K": 9,
    "L": 10, "M": 11, "O": 12, "P": 13, "a": 14, "b": 15, "0": 16, "9": 17, "N": 18,
    "Q": 19, "R": 20, "S": 21, "T": 22, "U": 23, "Z": 24, "d": 25, "E": 26, "c": 27,
    "X": 28, "Y": 29, -1: -1
}