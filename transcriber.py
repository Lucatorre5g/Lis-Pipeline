from nemo.collections.asr.models import EncDecCTCModel
from config_manager import ResourceConfigs
import os

class TranscriptionModel:

    def __init__(self,model_path="it_core_news_lg") -> None:
        self.model = EncDecCTCModel.restore_from(str(model_path))

    def process(self, wav_list:list):
        return self.model.transcribe(paths2audio_files=wav_list)


class ReusableTranscriptionModels(object):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            conf_manager = ResourceConfigs()
            model_conf = conf_manager.get_model_config()['transcription']
            cls._instance = super(ReusableTranscriptionModels, cls).__new__(cls)
            reusable_models = model_conf.get("per_process", 1)#4 # number of parallel processes
            model_path = model_conf.get("path", 1)
            cls._instance = cls.__new__(cls)
            cls._instance.reusable_models = reusable_models
            cls._instance.model_list = []
            for i in range(0, reusable_models+1):
                m = TranscriptionModel(model_path=model_path)
                cls._instance.model_list.append(m)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ReusableTranscriptionModels()
        return cls._instance

    def get_model(self):
        if len(self.model_list) <=0:
            raise RuntimeError('Call instance() instead')
        return self.model_list.pop(0)

    def release_model(self, m:TranscriptionModel):
        self.model_list.append(m)
