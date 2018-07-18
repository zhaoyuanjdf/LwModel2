# -*- coding:utf-8 -*-

import datetime
from common.mysql import *
from datasets.customer import *
from models.customer_loss import *

plat_form_db = get_db(host="127.0.0.1", user="root", password="yuanhua123456")

customer_loss_model = CustomerLoss(2)
customer_loss_model.load_model("/LwModel/17112009customer_loss_train")
# validation_data = None
start_time = datetime.datetime.now()
initial_epoch = 0
data_length = 500
generator = Customer(plat_form_db).query_customer_info(data_length)
validation_data = generator.next()
# customer_loss_model.fit_generator(generator, steps_per_epoch=10, epochs=2, validation_data=validation_data)
for train_data in generator:
    # for i in range(20):
    #     customer_loss_model.train_on_batch(train_data[0], train_data[1])
    print("train_data %s" % (1.0 * sum(train_data[1]) / len(train_data[1])))
    print("train acc %s" % str(float(np.sum(np.argmax(customer_loss_model.predict_on_batch(train_data[0]), axis=1)
                                            == np.argmax(train_data[1], axis=1))) / len(train_data[1])))
    predict_result = np.argmax(customer_loss_model.predict_on_batch(train_data[0]), axis=1)
    true_result = np.argmax(train_data[1], axis=1)
    if sum(true_result) > 0:
        train_dead_user_recall = 1.0*sum([1 if true_result[i] == 1 and predict_result[i] == 1 else 0
                                       for i in range(len(train_data[1]))])/sum(true_result)
        print("train_dead_user_recall %s" % train_dead_user_recall)
    if sum(predict_result) > 0:
        predict_dead_user_precise = 1.0*sum([1 if  [i] == 1 and predict_result[i] == 1 else 0
                                       for i in range(len(train_data[1]))])/sum(predict_result)
        print("predict_dead_user_precise %s" % predict_dead_user_precise)

    # print("validation_data %s" % (1.0 * sum(validation_data[1]) / len(validation_data[1])))
    # print("validation_data acc %s" % str(float(np.sum(np.argmax(
    #         customer_loss_model.predict_on_batch(validation_data[0]), axis=1) ==
    #                                            np.argmax(validation_data[1], axis=1))) / len(validation_data[0])))
    # predict_result = np.argmax(customer_loss_model.predict_on_batch(validation_data[0]), axis=1)
    # true_result = np.argmax(validation_data[1], axis=1)
    # validation_dead_user_acc = 1.0 * sum([1 if true_result[i] == 1 and predict_result[i] == 1 else 0
    #                                       for i in range(len(validation_data[1]))]) / sum(true_result)
    # print("validation_dead_user_predict_acc %s" % validation_dead_user_acc)
    # now = datetime.datetime.now()
    # print((now - start_time).seconds > 300)
    # if (now - start_time).seconds > 300:
    #     start_time = now
    #     model_save_path = now.strftime("%y%m%d%H") + "customer_loss_train"
    #     customer_loss_model.save_model(model_save_path)



# for train_date in Customer(plat_form_db).query_customer_info():
#     x = train_date[0]
#     y = train_date[1]
#     if validation_data is None:
#         print(sum(y) * 1.0 / len(y))
#         validation_data = (x, y)
#     else:
#         print(sum(y) * 1.0 / len(y))
#         epochs = 30
#         print("initial_epoch %s" % initial_epoch)
#         customer_loss_model.fit(
#             x=x, y=y, shuffle=True, batch_size=200, epochs=epochs,
#             initial_epoch=initial_epoch)
#         print(customer_loss_model.get_model_para().shape())
#         initial_epoch += epochs
#         print("train acc %s" % str(float(np.sum(np.argmax(customer_loss_model.predict_on_batch(x), axis=1)
#                                                 == np.argmax(y, axis=1))) / len(y)))
#         print("test acc %s" % str(float(np.sum(np.argmax(
#             customer_loss_model.predict_on_batch(validation_data[0]), axis=1) ==
#                                                np.argmax(validation_data[1], axis=1))) / len(validation_data[0])))
#         # print customer_loss_model.predict_on_batch(validation_data[0])
#
