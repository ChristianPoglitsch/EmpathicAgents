from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x7B-Instruct-v0.1")

# seems like there is an internal problem with loading the Mixtral tokenizer

# Ibrahim@DESKTOP-EN2SI6N MINGW64 ~/Documents/EmpathicAgents/LLM_Character (main)
# $ python bruh.py
# C:\Users\Ibrahim\Documents\EmpathicAgents\venv\lib\site-packages\huggingface_hub\file_download.py:1132: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
#   warnings.warn(
# Traceback (most recent call last):
#   File "C:\Users\Ibrahim\Documents\EmpathicAgents\LLM_Character\bruh.py", line 6, in <module>
#     tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x7B-Instruct-v0.1")
#   File "C:\Users\Ibrahim\Documents\EmpathicAgents\venv\lib\site-packages\transformers\models\auto\tokenization_auto.py", line 825, in from_pretrained
#     return tokenizer_class.from_pretrained(pretrained_model_name_or_path, *inputs, **kwargs)
#   File "C:\Users\Ibrahim\Documents\EmpathicAgents\venv\lib\site-packages\transformers\tokenization_utils_base.py", line 2048, in from_pretrained
#     return cls._from_pretrained(
#   File "C:\Users\Ibrahim\Documents\EmpathicAgents\venv\lib\site-packages\transformers\tokenization_utils_base.py", line 2287, in _from_pretrained
#     tokenizer = cls(*init_inputs, **init_kwargs)
#   File "C:\Users\Ibrahim\Documents\EmpathicAgents\venv\lib\site-packages\transformers\models\llama\tokenization_llama_fast.py", line 133, in __init__
#     super().__init__(
#   File "C:\Users\Ibrahim\Documents\EmpathicAgents\venv\lib\site-packages\transformers\tokenization_utils_fast.py", line 111, in __init__
#     fast_tokenizer = TokenizerFast.from_file(fast_tokenizer_file)
# Exception: data did not match any variant of untagged enum PyPreTokenizerTypeWrapper at line 40 column 3

# https://github.com/huggingface/transformers/issues/31789

# upgraded tokenizer to  0.19.1
# which meant upgrading also transformers. (4.42.4)