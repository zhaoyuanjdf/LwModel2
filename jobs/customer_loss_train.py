# -*- coding:utf-8 -*-

import datetime
from common.mysql import *
from datasets.customer import *
from models.customer_loss import *

plat_form_db = get_db(host="127.0.0.1", user="root", password="yuanhua123456")

customer_loss_model = CustomerLoss(2)
validation_data = None
start_time = datetime.datetime.now()
for train_date in Customer(plat_form_db).query_customer_info():
    x = train_date[0]
    y = train_date[1]
    if validation_data is None:
        print(sum(y)*1.0/len(y))
        validation_data = (x, y)
    else:
        print(sum(y)*1.0/len(y))
        customer_loss_model.fit(x=x, y=y, validation_data=validation_data, shuffle=True, batch_size=1, epochs=6)

        now = datetime.datetime.now()
        if (now - start_time).seconds > 600:
            model_save_path = now.strftime("%y%m%d%H")+"customer_loss_train"
            customer_loss_model.save_model(model_save_path)

