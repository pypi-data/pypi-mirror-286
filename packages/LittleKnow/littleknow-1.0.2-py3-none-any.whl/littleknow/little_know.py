#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/20 16:15
# @Author  : 沈复
# @File    : little_know.py
# @Software: PyCharm
# @desc:
import os.path
import sys
import jieba
import shortuuid
from haystack_bm25.rank_bm25 import BM25Okapi
from modelscope import snapshot_download, Tasks, pipeline
from modelscope.outputs import OutputKeys
from diskcache import  Cache
from littleknow.know_search import BaiduSearch


# jieba.enable_paddle()
def get_calling_module_path(dir):
    calling_module_path = os.path.dirname(sys.argv[0])
    cache_dir = os.path.join(calling_module_path, "know")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, dir)

class LittleKnow():
    def __init__(self, know_name, know_data_cache_dir=get_calling_module_path("know_data"), model_cache_dir=get_calling_module_path("model"), lazy_training=False):
        """

        :param know_name:  知识库名称
        :param know_data_cache_dir:   知识库数据目录
        :param model_cache_dir:  模型缓存目录
        :param is_offline:  是否离线模式
        :param lazy_training:  是否后台懒训练 这里的懒训练其实不是训练的意思 而是空闲时候 会在当前目录下生成语料参数  会自动统计问的最多的资料 结合答案去生成东西
        """
        # 如果这俩都是none  则 根据调用路径去生成
        self.cache=Cache(str(os.path.join(know_data_cache_dir,know_name)))

        print(os.path.join(know_data_cache_dir,know_name))
        # 数据缓存路径 一定要有
        self.seg_model_path = snapshot_download('damo/nlp_bert_document-segmentation_chinese-base',cache_dir=model_cache_dir)
        self.seg_model = pipeline(task=Tasks.document_segmentation,model='damo/nlp_bert_document-segmentation_chinese-base')

        self.knwo_search = BaiduSearch()
        # bs.search("汽车")



        self.know_datas=set()
        for key in self.cache.iterkeys():
            self.know_datas.add(self.cache.get(key).get("content",""))

        # self.offline()



    def _init_cache_dir(self, cache_dir):
        if cache_dir:
            return cache_dir
        else:
            calling_module_path =  os.path.dirname(sys.argv[0])
            cache_dir = os.path.join(calling_module_path, "know")
            os.makedirs(cache_dir, exist_ok=True)
            return cache_dir


    def seg(self,doc):
        """
        文本分割
        :param doc:
        :return:
        """
        result = self.seg_model(documents = doc )
        seg_list = [r.strip() for r in result[OutputKeys.TEXT].split("\n\t") if r.strip() ]
        return seg_list


    def know_net_work_search(self,key_word,is_save=True):
        """
        知识搜索功能  接入百度接口  默认直接保存到本地知识库
        :param key_word:
        :return:
        """
        results = self.knwo_search.search(key_word)
        if is_save:
            for r in results:
                publish=r.pop("url","")
                content = r.pop("content","")
                title = r.pop("title", "")
                fingerprint=f"{title}_{content}_{publish}"
                seg_txt_id = self.get_uuid(fingerprint)
                seg_texts=self.seg(content)
                for seg_text in seg_texts:

                    self.cache.set(seg_txt_id, {"seg_id":seg_txt_id,"content": seg_text, "source": "net","meta_data":r})
                    self.know_datas.add(seg_text)
        return results

    def get_uuid(self,text):
        return shortuuid.ShortUUID().uuid(text)[0:16]
    def add_know(self,text):
        """
        目前暂定的是text  后续会增加 图像 音频等检索
        :param text:
        :return:
        """
        seg_texts=self.seg(text)
        for seg_text in seg_texts:
            if seg_text:
                seg_txt_id = self.get_uuid(seg_text)
                self.cache.set(seg_txt_id,{"content":seg_text,"source":"local","meta_data":{}})
                self.know_datas.add( seg_text )

    def query(self,query_key_word,top_k=5):
        """
        切记 如果query_key太小的话 会出现hash稀疏导致结果不确定
        :param query_key_word:
        :param top_k:
        :return:
        """

        datas = list(self.know_datas)
        tokenized_corpus = [list(jieba.cut(text, use_paddle=True)) for text in datas]

        bm25 = BM25Okapi(tokenized_corpus)

        tokenized_query = list(jieba.cut(query_key_word, use_paddle=True))

        s = bm25.get_top_n(tokenized_query, datas, n=top_k)

        return s



if __name__ == '__main__':
    lk=LittleKnow(know_name="大语言模型测试知识库2")
    text="""
           移动
       移动端语音唤醒模型，
       检测关键词为“小云小云”。模型主体为4层FSMN结构，使用CTC训练准则，参数量750K，适用于移动端设备运行。模型输入为Fbank特征，输出为基于char建模的中文全集token预测，测试工具根据每一帧的预测数据进行后处理得到输入音频的实时检测结果。模型训练采用“basetrain + finetune”的模式，basetrain过程使用大量内部移动端数据，在此基础上，使用1万条设备端录制安静场景“小云小云”数据进行微调，得到最终面向业务的模型。后续用户可在basetrain模型基础上，使用其他关键词数据进行微调，得到新的语音唤醒模型，但暂时未开放模型finetune功能。

       张三张三

       123
       doc1 = "这是一个示例文档。"
       doc2 = "这是另一个示例文档。"
    """
    # lk.add_know(text)

    # res = lk.know_net_work_search("大语言模型")
    # print(res)
    results = lk.query("移动端数据",top_k=5)
    print(results)
    pass

