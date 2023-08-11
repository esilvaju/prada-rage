import logging
from pathlib import Path
import torch
from auto_gptq import AutoGPTQForCausalLM
from huggingface_hub import hf_hub_download
from langchain.chains import RetrievalQAWithSourcesChain, RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import HuggingFacePipeline, LlamaCpp
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    LlamaForCausalLM,
    LlamaTokenizer,
    pipeline,
)

from lib.infrastructure.config.devices import DeviceType
from lib.infrastructure.gateway.localgpt.llm_models import supported_models

class LocalGPTInferenceQueryService:
    def __init__(self, llm_model: str, root_dir: Path, db_dir: Path, embedding_model_name: str, device_type: DeviceType) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._root_dir = root_dir
        self._db_dir = db_dir
        self._embedding_model_name = embedding_model_name
        self._device_type = DeviceType(device_type)
        self._llm_model = llm_model
        self._supported_models = supported_models

    def load_model(self, device_type, model_id, model_basename=None):
        """
        Select a model for text generation using the HuggingFace library.
        If you are running this for the first time, it will download a model for you.
        subsequent runs will use the model from the disk.

        Args:
            device_type (str): Type of device to use, e.g., "cuda" for GPU or "cpu" for CPU.
            model_id (str): Identifier of the model to load from HuggingFace's model hub.
            model_basename (str, optional): Basename of the model if using quantized models.
                Defaults to None.

        Returns:
            HuggingFacePipeline: A pipeline object for text generation using the loaded model.

        Raises:
            ValueError: If an unsupported model or device type is provided.
        """
        self.logger.info(f"Loading Model: {model_id}, on: {device_type}")
        self.logger.info("This action can take a few minutes!")

        if model_basename is not None:
            if ".ggml" in model_basename:
                self.logger.info("Using Llamacpp for GGML quantized models")
                model_path = hf_hub_download(repo_id=model_id, filename=model_basename)
                max_ctx_size = 2048
                kwargs = {
                    "model_path": model_path,
                    "n_ctx": max_ctx_size,
                    "max_tokens": max_ctx_size,
                }
                if device_type.lower() == "mps":
                    kwargs["n_gpu_layers"] = 1000
                if device_type.lower() == "cuda":
                    kwargs["n_gpu_layers"] = 1000
                    kwargs["n_batch"] = max_ctx_size
                return LlamaCpp(**kwargs)

            else:
                # The code supports all huggingface models that ends with GPTQ and have some variation
                # of .no-act.order or .safetensors in their HF repo.
                self.logger.info("Using AutoGPTQForCausalLM for quantized models")

                if ".safetensors" in model_basename:
                    # Remove the ".safetensors" ending if present
                    model_basename = model_basename.replace(".safetensors", "")

                tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
                self.logger.info("Tokenizer loaded")

                model = AutoGPTQForCausalLM.from_quantized(
                    model_id,
                    model_basename=model_basename,
                    use_safetensors=True,
                    trust_remote_code=True,
                    device="cuda:0",
                    use_triton=False,
                    quantize_config=None,
                )
        elif (
            device_type.lower() == "cuda"
        ):  # The code supports all huggingface models that ends with -HF or which have a .bin
            # file in their HF repo.
            self.logger.info("Using AutoModelForCausalLM for full models")
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.logger.info("Tokenizer loaded")

            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                device_map="auto",
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                trust_remote_code=True,
                # max_memory={0: "15GB"} # Uncomment this line with you encounter CUDA out of memory errors
            )
            model.tie_weights()
        else:
            self.logger.info("Using LlamaTokenizer")
            tokenizer = LlamaTokenizer.from_pretrained(model_id)
            model = LlamaForCausalLM.from_pretrained(model_id)

        # Load configuration from the model to avoid warnings
        generation_config = GenerationConfig.from_pretrained(model_id)
        # see here for details:
        # https://huggingface.co/docs/transformers/
        # main_classes/text_generation#transformers.GenerationConfig.from_pretrained.returns

        # Create a pipeline for text generation
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=2048,
            temperature=0,
            top_p=0.95,
            repetition_penalty=1.15,
            generation_config=generation_config,
        )

        local_llm = HuggingFacePipeline(pipeline=pipe)
        self.logger.info("Local LLM Loaded")

        return local_llm
    
    @property
    def db_dir(self):
        return str(self._root_dir / self._db_dir)
    
    @property
    def model_name(self):
        return self._embedding_model_name
    
    @property
    def embedding_fn(self):
        return HuggingFaceInstructEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device_type},
        )
    
    @property
    def db(self):
        return Chroma(
            persist_directory=self.db_dir,
            embedding_function=self.embedding_fn
        )
    
    @property
    def model_name(self):
        return self._embedding_model_name
    
    @property
    def device_type(self):
        return self._device_type.value
    
    @property
    def llm_model(self):
        if self._llm_model not in list(self._supported_models.keys()):
            raise ValueError(f"LLM model {self._llm_model} is not supported")
        return (
            self._llm_model,
            self._supported_models[self._llm_model]['model_id'],
            self._supported_models[self._llm_model]['model_basename']
        )
    
    @property
    def llm(self):
        llm_model, model_id, model_basename = self.llm_model
        llm = self.load_model(self.device_type, model_id=model_id, model_basename=model_basename)
        return llm

    @property
    def retriever(self):
        return self.db.as_retriever()
    
    @property
    def prompt_template(self):
        template = """Use the following pieces of context to answer the question at the end. If you don't know the answer,\
just say that you don't know, don't try to make up an answer.

{context}

{history}
Question: {question}
Helpful Answer:
"""
        return PromptTemplate(input_variables=["history", "context", "question"], template=template)
    
    @property
    def memory(self):
        return ConversationBufferMemory(
            input_key="question",
            memory_key="history"
        )
    
    @property
    def qa(self):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template, "memory": self.memory},
        )