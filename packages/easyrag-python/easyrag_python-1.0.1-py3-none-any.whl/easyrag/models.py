
import os
import sys
import torch
from typing import Tuple
from pydantic import SecretStr
from easyrag.utils import (
    pdf_loader, 
    store_user_chat_history, 
    transform_and_store, 
    get_answer,
    youtube_url_loader
    )
from transformers import (
    BitsAndBytesConfig, 
    AutoConfig, 
    AutoModelForCausalLM, 
    AutoTokenizer, 
    pipeline
    )
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings



class HuggingFaceModel:
    def __init__(
            self,
            model_id: str = None,
            hf_token: SecretStr = None,
            embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
            temperature: float = 0.5,
            max_token: int = 1000,
            trust_remote_code: bool = False,
            repetition_penalty: float = 1,
            return_full_text: bool = False,
            do_sample: bool = True
            ) -> None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if device.type == "cuda":
            self._llm, self._embedding = self._huggingface(
                model_id,
                embedding_model,
                temperature,
                max_token,
                hf_token,
                trust_remote_code,
                repetition_penalty,
                return_full_text,
                do_sample
                )
        else:
            raise RuntimeError(
                """Please use GPU to use the Open-Source model 
                or Use API Based Model(E.g. GoogleGemini, OpenAI)"""
                )

    def _huggingface(
            self, model_id: str,
            embedding_model: str,
            temperature: float,
            max_token: int,
            hf_token: SecretStr,
            trust_remote_code: bool,
            repetition_penalty: float,
            return_full_text: bool,
            do_sample: bool
            ) -> Tuple:
  
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            #bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
            )

        model_config = AutoConfig.from_pretrained(
            pretrained_model_name_or_path=model_id,
            token=hf_token
            )

        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=model_id,
            token=hf_token,
            config=model_config,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=trust_remote_code,
            cache_dir=os.getcwd()
            )

        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=model_id,
            token=hf_token
            )

        hf_pipeline = pipeline(
            model=model,
            task="text-generation",
            tokenizer=tokenizer,
            return_full_text=return_full_text,
            temperature=temperature,
            max_new_tokens=max_token,
            repetition_penalty=repetition_penalty,
            trust_remote_code=trust_remote_code,
            do_sample=do_sample
            )
        
        llm = HuggingFacePipeline(pipeline=hf_pipeline)
        embedding = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": "cuda"}
            )
        return llm, embedding

    def retrieve_answer(self, query: str=None, chat_mode: bool = False):
        get_answer(
            llm_model=self._llm,
            vector_store=self._vector_store.as_retriever(),
            query=query,
            chat_mode=chat_mode
            )
        
        #clear memory cache    
        torch.cuda.empty_cache()

    def from_pdf(self, pdf_path: str)->"HuggingFaceModel":
        raw_texts = pdf_loader(pdf_path)
        self._vector_store = transform_and_store(
            documents=raw_texts, 
            embedding=self._embedding
            )
        return self

    def from_youtube(self, video_url: str)->"HuggingFaceModel":
        content = youtube_url_loader(url=video_url)
        self._vector_store = transform_and_store(
            documents=content, 
            embedding=self._embedding
            )
        return self


class GoogleGemini:
    def __init__(
            self,
            google_api_key: SecretStr,
            temperature: float = 0.1,
            max_token: int = 200
            ) -> None:
        self._llm, self._embedding = self._google_gen_ai(
            google_api_key,
            temperature,
            max_token
            )

    def _google_gen_ai(
            self,
            api_key: SecretStr,
            temperature: float,
            max_token: int
            ) -> Tuple:

        llm = GoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=temperature,
            max_output_tokens=max_token
            )
        embedding = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
            )
        return llm, embedding

    def retrieve_answer(self, query: str=None, chat_mode: bool = False):
        get_answer(
            llm_model=self._llm,
            vector_store=self._vector_store.as_retriever(),
            query=query,
            chat_mode=chat_mode
            )

    def from_pdf(self, pdf_path: str)->"GoogleGemini":
        raw_texts = pdf_loader(pdf_path)
        self._vector_store = transform_and_store(
            documents=raw_texts, 
            embedding=self._embedding
            )
        return self

    def from_youtube(self, video_url: str)->"GoogleGemini":
        content = youtube_url_loader(url=video_url)
        self._vector_store = transform_and_store(
            documents=content, 
            embedding=self._embedding
            )
        return self


class OpenAI:
    def __init__(
            self,
            openai_api_key: SecretStr, 
            temperature: float = 0.1
            ) -> None:
        self._llm, self._embedding = self._openai(
            openai_api_key, temperature)

    def _openai(
            self, 
            openai_api_key: SecretStr, 
            temperature: float
            ) -> Tuple:

        llm = ChatOpenAI(
            model="gpt-3.5-turbo", 
            openai_api_key=openai_api_key, 
            temperature=temperature
            )
        embedding = OpenAIEmbeddings(
            model="text-embedding-ada-002", 
            openai_api_key=openai_api_key
            )
        return llm, embedding

    def retrieve_answer(self, query: str=None, chat_mode: bool = False):
        get_answer(
            llm_model=self._llm,
            vector_store=self._vector_store.as_retriever(),
            query=query,
            chat_mode=chat_mode
            )
    def from_pdf(self, pdf_path: str)->"OpenAI":
        raw_texts = pdf_loader(pdf_path)
        self._vector_store = transform_and_store(
            documents=raw_texts, 
            embedding=self._embedding
            )
        return self

    def from_youtube(self, video_url: str)->"OpenAI":
        content = youtube_url_loader(url=video_url)
        self._vector_store = transform_and_store(
            documents=content, 
            embedding=self._embedding
            )
        return self



class OllamaLLM:
    def __init__(
            self, 
            model: str = "phi3", 
            embedding_model: str = "all-minilm", 
            temperature: float = 0.2
            ) -> None:
        self._model = model
        self._embedding_model = embedding_model
        self._chat_history = store_user_chat_history()
        try:
            self._llm, self._embedding = self._ollama_local(temperature)
        except Exception as e:
            raise RuntimeError("Make sure Ollama is running on your system.")

    def _ollama_local(self, temperature: float)->Tuple:
        llm = Ollama(
            model=self._model, 
            temperature=temperature
            )
        embedding = OllamaEmbeddings(
            model=self._embedding_model
            )
        return llm, embedding

    def retrieve_answer(self, query: str=None, chat_mode: bool = False):
        get_answer(
            llm_model=self._llm,
            vector_store=self._vector_store.as_retriever(),
            query=query,
            chat_mode=chat_mode
            )

    def from_pdf(self, pdf_path: str)->"OllamaLLM":
        raw_texts = pdf_loader(pdf_path)
        self._vector_store = transform_and_store(
            documents=raw_texts, 
            embedding=self._embedding
            )
        return self

    def from_youtube(self, video_url: str)->"OllamaLLM":
        content = youtube_url_loader(url=video_url)
        self._vector_store = transform_and_store(
            documents=content, 
            embedding=self._embedding
            )
        return self


# Export all classes
__all__ = ['HuggingFaceModel', 'GoogleGemini', 'OpenAI', 'OllamaLLM']