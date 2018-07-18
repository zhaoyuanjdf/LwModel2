# -*- coding:utf-8 -*-

from multiprocessing import Process, Queue
import datetime
from common.mysql import *
from datasets.customer import *
from models.customer_loss import *


class RunTool(object):

    def __init__(self, queue_size, generator, model, validation_data, epochs):
        self.queue = Queue(queue_size)
        self.generator = generator
        self.model = model
        self.validation_data = validation_data
        self.epochs = epochs
        self.start_time = datetime.datetime.now()


# 写数据进程执行的代码:
def data_producer(run_tool):
    while True:
        run_tool.queue.put(run_tool.generator.next())


# 读数据进程执行的代码:
def data_consumer(run_tool):
    validation_data = run_tool.validation_data
    while True:
        train_data = run_tool.queue.get(True)
        for i in range(run_tool.epochs):
            run_tool.model.train_on_batch(train_data[0], train_data[1])
        print("train_data %s" % (1.0*sum(train_data[1])/len(train_data[1])))
        print("train acc %s" % str(float(np.sum(np.argmax(run_tool.model.predict_on_batch(train_data[0]), axis=1)
                                                == np.argmax(train_data[1], axis=1))) / len(train_data[1])))
        print("validation_data %s" % (1.0*sum(validation_data[1])/len(validation_data[1])))
        print("validation_data acc %s" % str(float(np.sum(np.argmax(
            customer_loss_model.predict_on_batch(validation_data[0]), axis=1) ==
                                               np.argmax(validation_data[1], axis=1))) / len(validation_data[0])))
        if (datetime.datetime.now() - run_tool.start_time).seconds % 300 == 0:
            model_save_path = datetime.datetime.now().strftime("%y%m%d%H") + "customer_loss_train"
            run_tool.model.save_model(model_save_path)


if __name__ == '__main__':
    plat_form_db = get_db(host="127.0.0.1", user="root", password="yuanhua123456")

    customer_loss_model = CustomerLoss(2)

    initial_epoch = 0
    data_length = 500
    generator = Customer(plat_form_db).query_customer_info(data_length)

    validation_data = generator.next()
    run_tool = RunTool(10, generator, customer_loss_model, validation_data, 5)
    producer = Process(target=data_producer, args=(run_tool,))
    consumer = Process(target=data_consumer, args=(run_tool,))

    producer.start()
    consumer.start()

    consumer.join()

    print ('训练完成')






git remote add LwModel git@github.com:zhaoyuanjdf/LwModel.git

git push -u LwModel master