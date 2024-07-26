# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""A wrapper over the TensorRT-LLM high level API runner."""


import json
from pathlib import Path
from typing import Dict, Iterable, List, Union

from tensorrt_llm.bindings import executor as tllm
from tensorrt_llm.executor import GenerationExecutor
from tensorrt_llm.hlapi import KvCacheConfig as TRT_KvCacheConfig
from tensorrt_llm.hlapi import SamplingParams
from tensorrt_llm.hlapi.llm import LLM as TRT_LLM
from tensorrt_llm.hlapi.llm_utils import CachedModelLoader
from tensorrt_llm.hlapi.mpi_session import external_mpi_comm_available
from tensorrt_llm.hlapi.tokenizer import TokenizerBase, TransformersTokenizer


class LLM(TRT_LLM):
    """A wrapper over the ``tensorrt_llm.hlapi.llm.LLM`` for LLM profiling and validation."""

    def __init__(
        self,
        engine_dir: Union[str, Path],
        tokenizer: TokenizerBase,
        kv_cache_config: Dict[str, Union[int, float]] = {},
    ):
        """Initializes the LLM runner class.

        Args:
            engine_dir: the directory path of the TensorRT-LLM engine.
            tokenizer: the tokenizer. For example, a tokenizer from the Huggingface model.
            kv_cache_config: the kv cache config as a dict. Please refer to
                https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/performance/perf-best-practices.md
        """
        with open(Path(engine_dir) / "config.json", "r") as engine_config_file:
            engine_config = json.load(engine_config_file)
            build_config = engine_config["build_config"]
            world_size = (
                engine_config.get("pretrained_config", {}).get("mapping", {}).get("world_size", 1)
            )
            max_tokens_in_paged_kv_cache = (
                build_config["max_seq_len"] * build_config["max_batch_size"] // world_size
            )

        trt_kv_cache_config = TRT_KvCacheConfig()

        # If not specified, free_gpu_memory_fraction is set to the default TRT LLM value 0.9
        trt_kv_cache_config.free_gpu_memory_fraction = kv_cache_config.get(
            "free_gpu_memory_fraction", 0.9
        )

        # If not specified, max_tokens is set to the max value calculated above.
        if "max_tokens" in kv_cache_config:
            trt_kv_cache_config.max_tokens = kv_cache_config.get(
                "max_tokens", max_tokens_in_paged_kv_cache
            )

        self.inflight_batch = "Medusa" in engine_config.get("pretrained_config", {}).get(
            "architecture", ""
        )

        super().__init__(
            model=engine_dir,
            tokenizer=TransformersTokenizer(tokenizer),
            kv_cache_config=trt_kv_cache_config,
        )

    @property
    def max_input_len(self):
        """Get the max input length from the LLM instance."""
        return self.args.build_config.max_input_len

    @property
    def max_beam_width(self):
        """Get the max beam width from the LLM instance."""
        return self.args.build_config.max_beam_width

    def _build_model(self):
        model_loader = CachedModelLoader(
            self.args,
            mpi_session=self.mpi_session,
            workspace=self.workspace,
            llm_build_stats=self.llm_build_stats,
        )
        self._engine_dir = model_loader()

        executor_config = tllm.ExecutorConfig(
            max_beam_width=self.args.build_config.max_beam_width,
            scheduler_config=self.args.scheduler_config,
            batching_type=(
                tllm.BatchingType.INFLIGHT if self.inflight_batch else tllm.BatchingType.STATIC
            ),
        )
        if self.args.kv_cache_config is not None:
            executor_config.kv_cache_config = self.args.kv_cache_config
        if self.args.peft_cache_config is not None:
            executor_config.peft_cache_config = self.args.peft_cache_config
        if self.args.decoding_config is not None:
            executor_config.decoding_config = self.args.decoding_config
        if self.args.logits_post_processor_map:
            executor_config.logits_post_processor_map = self.args.logits_post_processor_map
        executor_config.normalize_log_probs = self.args.normalize_log_probs
        executor_config.enable_chunked_context = self.args.enable_chunked_context
        executor_config.max_beam_width = self.args.build_config.max_beam_width

        self._executor = GenerationExecutor.create(
            self._engine_dir,
            executor_config=executor_config,
            model_world_size=self.args.parallel_config.world_size,
            mpi_session=self.mpi_session,
            reuse_mpi_comm=external_mpi_comm_available(self.args.parallel_config.world_size),
        )

    def generate_tokens(
        self,
        prompts: Union[Iterable[str], Iterable[List[int]]],
        max_new_tokens: int,
        temperature: float = 1.0,
        keep_input_prompt: bool = True,
    ) -> Union[List[List[int]], List[List[List[int]]]]:
        """Generates the tokens based on the input prompts.

        Args:
            prompts: The input prompts. Could be a list of strings or token lists.
            max_new_tokens: The max output token length.
            temperature: The sampling temperature
            keep_input_prompt: Set to include input prommpts in the outputs.

        Returns:
            a list of output token lists if max_beam_width is 1 or a 3D list with shape [batch, beam, sequence_len].
        """
        assert temperature >= 0.0, "Temperature must be greater than 0.0."

        # TRT LLM acccepts temperature values only greater than 0.0
        temperature = max(temperature, 0.01)

        beam_width = self.max_beam_width
        sampling_config = SamplingParams(
            temperature=temperature, max_new_tokens=max_new_tokens, beam_width=beam_width
        )

        prompt_ids = [
            self.tokenizer.encode(prompt) if isinstance(prompt, str) else prompt
            for prompt in prompts
        ]
        outputs = self.generate(prompt_ids, sampling_params=sampling_config)

        def _process_output_token_id(output_token_id, prompt_id, with_input, keep_input_prompt):
            if with_input == keep_input_prompt:
                return output_token_id

            elif with_input:  # and not keep_input_prompt
                return output_token_id[len(prompt_id) :]

            else:  # not with_input and keep_input_prompt:
                return prompt_id + output_token_id

        # TODO: check executor of trtllm 0.11 for `with_input``
        with_input = False
        output_tokens = []
        for prompt_id, output in zip(prompt_ids, outputs):
            output_token_ids = [out.token_ids for out in output.outputs]

            for output_token_id in output_token_ids:
                output_tokens.append(
                    _process_output_token_id(
                        output_token_id, prompt_id, with_input, keep_input_prompt
                    )
                )

        return (
            output_tokens
            if beam_width == 1
            else [
                output_tokens[i : i + beam_width] for i in range(0, len(output_tokens), beam_width)
            ]
        )

    def generate_text(
        self,
        prompts: Union[Iterable[str], Iterable[List[int]]],
        max_new_tokens: int,
        temperature: float = 1.0,
        keep_input_prompt: bool = True,
    ) -> Union[List[str], List[List[str]]]:
        """Generates the text based on the input prompts.

        Args:
            prompts: The input prompts. Could be a list of strings or token lists.
            max_new_tokens: The max output token length.
            temperature: The sampling temperature
            keep_input_prompt: Set to include input prommpts in the outputs.

        Returns:
            a list of output text strings if max_beam_width is 1 or a 2D list with shape [batch, beam].
        """
        assert temperature >= 0.0, "Temperature must be greater than 0.0."

        # TRT LLM acccepts temperature values only greater than 0.0
        temperature = max(temperature, 0.01)

        beam_width = self.max_beam_width
        output_tokens = self.generate_tokens(
            prompts, max_new_tokens, temperature, keep_input_prompt
        )
        if beam_width == 1:
            output_text = [self.tokenizer.decode(batch) for batch in output_tokens]
        else:
            output_text = [
                [self.tokenizer.decode(beam) for beam in batch] for batch in output_tokens
            ]
        return output_text
