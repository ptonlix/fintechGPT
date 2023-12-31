
from chains.local_doc_qa import LocalDocQA
# import os
# import nltk
import argparse
import config
import models.shared as shared
from models.loader import LoaderCheckPoint
# nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path

# Show reply with source text from input document
REPLY_WITH_SOURCE = True


def main():

    llm_model_ins = shared.loaderLLM()
    llm_model_ins.history_len = LLM_HISTORY_LEN

    local_doc_qa = LocalDocQA()
    local_doc_qa.init_cfg(llm_model=llm_model_ins,
                          embedding_model=EMBEDDING_MODEL,
                          embedding_device=EMBEDDING_DEVICE,
                          top_k=VECTOR_SEARCH_TOP_K)
    vs_path = None
    while not vs_path:
        print("注意输入的路径是完整的文件路径，例如knowledge_base/`knowledge_base_id`/content/file.md，多个路径用英文逗号分割")
        filepath = input("Input your local knowledge file path 请输入本地知识文件路径：")
        
        # 判断 filepath 是否为空，如果为空的话，重新让用户输入,防止用户误触回车
        if not filepath:
            continue

        # 支持加载多个文件
        filepath = filepath.split(",")
        # filepath错误的返回为None, 如果直接用原先的vs_path,_ = local_doc_qa.init_knowledge_vector_store(filepath)
        # 会直接导致TypeError: cannot unpack non-iterable NoneType object而使得程序直接退出
        # 因此需要先加一层判断，保证程序能继续运行
        temp,loaded_files = local_doc_qa.init_knowledge_vector_store(filepath)
        if temp is not None:
            vs_path = temp
            # 如果loaded_files和len(filepath)不一致，则说明部分文件没有加载成功
            # 如果是路径错误，则应该支持重新加载
            if len(loaded_files) != len(filepath):
                reload_flag = eval(input("部分文件加载失败，若提示路径不存在，可重新加载，是否重新加载，输入True或False: "))
                if reload_flag:
                    vs_path = None
                    continue

            print(f"the loaded vs_path is 加载的vs_path为: {vs_path}")
        else:
            print("load file failed, re-input your local knowledge file path 请重新输入本地知识文件路径")
        
    history = []
    while True:
        query = input("Input your question 请输入问题：")
        last_print_len = 0
        for resp, history in local_doc_qa.get_knowledge_based_answer(query=query,
                                                                     vs_path=vs_path,
                                                                     chat_history=history,
                                                                     streaming=STREAMING):
            if STREAMING:
                print(resp["result"][last_print_len:], end="", flush=True)
                last_print_len = len(resp["result"])
            else:
                print(resp["result"])
        if REPLY_WITH_SOURCE:
            source_text = [f"""出处 [{inum + 1}] {os.path.split(doc.metadata['source'])[-1]}：\n\n{doc.page_content}\n\n"""
                           # f"""相关度：{doc.metadata['score']}\n\n"""
                           for inum, doc in
                           enumerate(resp["source_documents"])]
            print("\n\n" + "\n\n".join(source_text))


if __name__ == "__main__":

    # 获取配置文件路径
    parser = argparse.ArgumentParser(prog='langchain-ChatGLM',
                                 description=' ChatGLM金融挑战赛Demo ')

    parser.add_argument('--config', default='../conf/fintechgpt.yaml', help='project config path')
 
    args = parser.parse_args()
    args_dict = vars(args)
    print(args_dict)
    # 读取配置文件
    conf = config.Config(args_dict.get('config'))
    # 加载大模型
    llm_model_in = shared.loaderLLM(LoaderCheckPoint(conf.get_llm_model(), conf.get_llm_model()))

    # 加载QA
    local_doc_qa = LocalDocQA(llm_model_in, conf.get_embedding_model())

    # 根据问题定位到具体的VS库
    dataconf = conf.get_data_conf()
    qlist = open(dataconf['question'], 'r').readlines()
    for question in qlist:
        subdir = '/'
        if question['company'] and question['date']:
            subdir += question['company'] + '/' + question['date'][:4]
            for resp, history in local_doc_qa.get_knowledge_based_answer(query=question['question'], vs_path=subdir, streaming=config.STREAMING):
                answer = {'id': question['id'], 'question': question['question'], 'answer': resp['result']}
                print(answer)
        else:
        #    for resp, history in local_doc_qa.get_knowledge_based_answer(query=question['question'], vs_path=subdir, streaming=config.STREAMING):
        #         answer = {'id': question['id'], 'question': question['question'], 'answer': resp['result']}
        #         print(answer) 
            answer = {'id': question['id'], 'question': question['question'], 'answer': ''}
            print('no company and date')


