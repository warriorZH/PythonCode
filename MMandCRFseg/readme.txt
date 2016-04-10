1.本分词器，使用MMSEG 和 CRF 分词方法，MMSEG基于词典，CRF基于统计
2.当前目录下的testExample.py是测试文件，通过设定crf_train_flag标志位来选择是CRF训练模式还是分词模式，
    执行方法： "python testExample.py your_test_file"
    例如: "python testExample.py /home/warrior/Desktop/test.txt"
    crf_train_flag：
        True: CRF训练模式
        False: 分词模式
    CRF模型已经建立好，可以直接进行分词测试。
3.分词结果存放在当前文件夹下tmp子文件夹里面
4.注意：分词数据需要是utf8编码格式
