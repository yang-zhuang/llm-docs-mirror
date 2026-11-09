# Mistral 3

[Mistral 3](https://mistral.ai/news/mistral-small-3) is a latency optimized model with a lot fewer layers to reduce the time per forward pass. This model adds vision understanding and supports long context lengths of up to 128K tokens without compromising performance.

You can find the original Mistral 3 checkpoints under the [Mistral AI](https://huggingface.co/mistralai/models?search=mistral-small-3) organization.

> [!TIP]
> This model was contributed by [cyrilvallez](https://huggingface.co/cyrilvallez) and [yonigozlan](https://huggingface.co/yonigozlan).
> Click on the Mistral3 models in the right sidebar for more examples of how to apply Mistral3 to different tasks.
>
> Set `use_kernels=True` in [from_pretrained()](/docs/transformers/v5.22.2/en/main_classes/model#transformers.PreTrainedModel.from_pretrained) to replace supported layers with optimized kernels from the Hub. Refer to [Loading kernels](../kernel_doc/loading_kernels) to learn more.

The example below demonstrates how to generate text for an image with [Pipeline](/docs/transformers/v5.22.2/en/main_classes/pipelines#transformers.Pipeline) and the [AutoModel](/docs/transformers/v5.22.2/en/model_doc/auto#transformers.AutoModel) class.

```python
from transformers import pipeline

messages = [
    {"role": "user",
        "content":[
            {"type": "image",
            "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",},
            {"type": "text", "text": "Describe this image."}
        ,]
    ,}
,]

pipeline = pipeline(
    task="image-text-to-text",
    model="mistralai/Mistral-Small-3.1-24B-Instruct-2503",
    device=0
)
outputs = pipeline(text=messages, max_new_tokens=50, return_full_text=False)

outputs[0]["generated_text"]
'The image depicts a vibrant and lush garden scene featuring a variety of wildflowers and plants. The central focus is on a large, pinkish-purple flower, likely a Greater Celandine (Chelidonium majus), with a'
```

```python
from transformers import AutoModelForImageTextToText, AutoProcessor

model_checkpoint = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
processor = AutoProcessor.from_pretrained(model_checkpoint)
model = AutoModelForImageTextToText.from_pretrained(
    model_checkpoint,
    device_map="auto",
)

messages = [
    {"role": "user",
        "content":[
            {"type": "image",
            "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",},
            {"type": "text", "text": "Describe this image."}
        ,]
    ,}
,]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True, return_dict=True,
    return_tensors="pt").to(model.device)

generate_ids = model.generate(**inputs, max_new_tokens=20)
decoded_output = processor.decode(generate_ids[0, inputs["input_ids"].shape[1] :], skip_special_tokens=True)

decoded_output
'The image depicts a vibrant and lush garden scene featuring a variety of wildflowers and plants. The central focus is on a large, pinkish-purple flower, likely a Greater Celandine (Chelidonium majus), with a'
```

## Notes

- Mistral 3 supports text-only generation.

```py
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

model_checkpoint = ".mistralai/Mistral-Small-3.1-24B-Instruct-2503"
processor = AutoProcessor.from_pretrained(model_checkpoint)
model = AutoModelForImageTextToText.from_pretrained(model_checkpoint, device_map="auto")

SYSTEM_PROMPT = "You are a conversational agent that always answers straight to the point, always end your accurate response with an ASCII drawing of a cat."
user_prompt = "Give me 5 non-formal ways to say 'See you later' in French."

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_prompt},
]

text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = processor(text=text, return_tensors="pt").to(0)
generate_ids = model.generate(**inputs, max_new_tokens=50, do_sample=False)
decoded_output = processor.batch_decode(generate_ids[:, inputs["input_ids"].shape[1] :], skip_special_tokens=True)[0]

print(decoded_output)
"1. À plus tard!
 2. Salut, à plus!
 3. À toute!
 4. À la prochaine!
 5. Je me casse, à plus!

```

 /\_/\
( o.o )
 > ^ <

```"
````

- Mistral 3 accepts batched image and text inputs.

```py
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

model_checkpoint = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
processor = AutoProcessor.from_pretrained(model_checkpoint)
model = AutoModelForImageTextToText.from_pretrained(model_checkpoint, device_map="auto")

messages = [
     [
         {
             "role": "user",
             "content": [
                 {"type": "image", "url": "https://huggingface.co/datasets/hf-internal-testing/transformers-synthetic-assets/resolve/main/images/llava_view.jpg"},
                 {"type": "text", "text": "Write a haiku for this image"},
             ],
         },
     ],
     [
         {
             "role": "user",
             "content": [
                 {"type": "image", "url": "https://www.ilankelman.org/stopsigns/australia.jpg"},
                 {"type": "text", "text": "Describe this image"},
             ],
         },
     ],
 ]

 inputs = processor.apply_chat_template(messages, padding=True, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt").to(model.device)

 output = model.generate(**inputs, max_new_tokens=25)

 decoded_outputs = processor.batch_decode(output, skip_special_tokens=True)
 decoded_outputs
["Write a haiku for this imageCalm waters reflect\nWhispers of the forest's breath\nPeace on wooden path"
, "Describe this imageThe image depicts a vibrant street scene in what appears to be a Chinatown district. The focal point is a traditional Chinese"]
```

- Mistral 3 also supported batched image and text inputs with a different number of images for each text. The example below quantizes the model with bitsandbytes.

```py
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText, BitsAndBytesConfig

model_checkpoint = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
processor = AutoProcessor.from_pretrained(model_checkpoint)
quantization_config = BitsAndBytesConfig(load_in_4bit=True)
model = AutoModelForImageTextToText.from_pretrained(
     model_checkpoint, quantization_config=quantization_config
 device_map="auto")

messages = [
     [
         {
             "role": "user",
             "content": [
                 {"type": "image", "url": "https://huggingface.co/datasets/hf-internal-testing/transformers-synthetic-assets/resolve/main/images/llava_view.jpg"},
                 {"type": "text", "text": "Write a haiku for this image"},
             ],
         },
     ],
     [
         {
             "role": "user",
             "content": [
                 {"type": "image", "url": "https://huggingface.co/datasets/hf-internal-testing/transformers-synthetic-assets/resolve/main/images/statue_of_liberty.jpg"},
                 {"type": "image", "url": "https://huggingface.co/datasets/hf-internal-testing/transformers-synthetic-assets/resolve/main/images/dreamstime_golden_gate_flowers.jpg"},
                 {"type": "text", "text": "These images depict two different landmarks. Can you identify them?"},
             ],
         },
     ],
 ]

 inputs = processor.apply_chat_template(messages, padding=True, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt").to(model.device)

 output = model.generate(**inputs, max_new_tokens=25)

 decoded_outputs = processor.batch_decode(output, skip_special_tokens=True)
 decoded_outputs
["Write a haiku for this imageSure, here is a haiku inspired by the image:\n\nCalm lake's wooden path\nSilent forest stands guard\n", "These images depict two different landmarks. Can you identify them? Certainly! The images depict two iconic landmarks:\n\n1. The first image shows the Statue of Liberty in New York City."]
```

## Mistral3Config[[transformers.Mistral3Config]]

#### transformers.Mistral3Config[[transformers.Mistral3Config]]

```python
transformers.Mistral3Config(transformers_version: str | None = None, architectures: list[str] | None = None, output_hidden_states: bool | None = False, return_dict: bool | None = True, dtype: str | torch.dtype | None = None, chunk_size_feed_forward: int = 0, is_encoder_decoder: bool = False, id2label: dict[int, str] | dict[str, str] | None = None, label2id: dict[str, int] | dict[str, str] | None = None, problem_type: Literal['regression', 'single_label_classification', 'multi_label_classification'] | None = None, vision_config: dict | transformers.configuration_utils.PreTrainedConfig | None = None, text_config: dict | transformers.configuration_utils.PreTrainedConfig | None = None, image_token_index: int = 10, projector_hidden_act: str = 'gelu', vision_feature_layer: int | list[int] = -1, multimodal_projector_bias: bool = False, spatial_merge_size: int = 2, tie_word_embeddings: bool = True)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/models/mistral3/configuration_mistral3.py#L26)

**Parameters:**

vision_config (`Union[dict, ~configuration_utils.PreTrainedConfig]`, *optional*) : The config object or dictionary of the vision backbone.

text_config (`Union[dict, ~configuration_utils.PreTrainedConfig]`, *optional*) : The config object or dictionary of the text backbone.

image_token_index (`int`, *optional*, defaults to `10`) : The image token index used as a placeholder for input images.

projector_hidden_act (`str`, *optional*, defaults to `gelu`) : The activation function used by the multimodal projector.

vision_feature_layer (`Union[int, list[int]]`, *optional*, defaults to `-1`) : The index of the layer to select the vision feature. If multiple indices are provided, the vision feature of the corresponding indices will be concatenated to form the vision features.

multimodal_projector_bias (`bool`, *optional*, defaults to `False`) : Whether to use bias in the multimodal projector.

spatial_merge_size (`int`, *optional*, defaults to `2`) : The size of the spatial merge window used to reduce the number of visual tokens by merging neighboring patches.

tie_word_embeddings (`bool`, *optional*, defaults to `True`) : Whether to tie weight embeddings according to model's `tied_weights_keys` mapping.

This is the configuration class to store the configuration of a Mistral3Model. It is used to instantiate a Mistral3
model according to the specified arguments, defining the model architecture. Instantiating a configuration with the
defaults will yield a similar configuration to that of the [mistralai/Mistral-Small-3.1-24B-Instruct-2503](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503)

Configuration objects inherit from [PreTrainedConfig](/docs/transformers/v5.22.2/en/main_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the
documentation from [PreTrainedConfig](/docs/transformers/v5.22.2/en/main_classes/configuration#transformers.PreTrainedConfig) for more information.

Example:

```python
>>> from transformers import Mistral3ForConditionalGeneration, Mistral3Config, PixtralVisionConfig, MistralConfig

>>> # Initializing a Pixtral-vision config
>>> vision_config = PixtralVisionConfig()

>>> # Initializing a Mistral config
>>> text_config = MistralConfig()

>>> # Initializing a Mistral3 configuration
>>> configuration = Mistral3Config(vision_config, text_config)

>>> # Initializing a model from the mistral3.1 configuration
>>> model = Mistral3ForConditionalGeneration(configuration)

>>> # Accessing the model configuration
>>> configuration = model.config
```

## MistralCommonBackend[[transformers.MistralCommonBackend]]

#### transformers.MistralCommonBackend[[transformers.MistralCommonBackend]]

```python
transformers.MistralCommonBackend(tokenizer_path: str | os.PathLike | pathlib.Path, mode: str | ValidationMode = 'test', model_max_length: int = 1000000000000000019884624838656, padding_side: str = 'left', truncation_side: str = 'right', model_input_names: list[str] | None = None, clean_up_tokenization_spaces: bool = False, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L194)

Class to wrap `mistral-common` tokenizers.

`mistral-common` is the official tokenizer library for Mistral AI models. To use it, you need to install it with:

```bash
pip install transformers[mistral-common]
```

Otherwise the tokenizer falls back to the Transformers implementation of the tokenizer.

For more info on `mistral-common`, see [mistral-common](https://github.com/mistralai/mistral-common).

This class is a wrapper around a `mistral_common.tokens.tokenizers.mistral.MistralTokenizer`.
It provides a Hugging Face compatible interface to tokenize using the official mistral-common tokenizer and inherits from the `PreTrainedTokenizerBase` class.

Here are the key behavior differences with the `PythonBackend` class:

- Pair of sequences are not supported. The signature has been kept for compatibility but all arguments related to pair of sequences are ignored. The return values for pairs are returned as `None`.
- The `is_split_into_words` argument is not supported.
- It is not possible to add new tokens to the tokenizer. Special tokens are handled differently from Transformers. In `mistral-common`, special tokens are never encoded directly. This means that: `tokenizer.encode("<s>")` will not return the ID of the `<s>` token. Instead, it will return a list of IDs corresponding to the tokenization of the string `"<s>"`. For more information, see the [mistral-common documentation](https://mistralai.github.io/mistral-common/usage/tokenizers/#special-tokens).

If you have suggestions to improve this class, please open an issue on the [mistral-common GitHub repository](https://github.com/mistralai/mistral-common/issues) if it is related to the tokenizer or on the [Transformers GitHub repository](https://github.com/huggingface/transformers/issues) if it is related to the Hugging Face interface.

#### add_special_tokens[[transformers.MistralCommonBackend.add_special_tokens]]

```python
add_special_tokens(special_tokens_dict: dict, replace_extra_special_tokens: bool = True)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1679)

`MistralCommonBackend` does not implement `add_special_tokens` by design.

If you would like this behaviour to be implemented, please open an issue in the `Transformers` or `mistral-common` repositories to request it.

#### add_tokens[[transformers.MistralCommonBackend.add_tokens]]

```python
add_tokens(special_tokens_dict: dict, replace_extra_special_tokens: bool = True)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1691)

`MistralCommonBackend` does not implement `add_special_tokens` by design.

If you would like this behaviour to be implemented, please open an issue in the `Transformers` or `mistral-common` repositories to request it.

#### apply_chat_template[[transformers.MistralCommonBackend.apply_chat_template]]

```python
apply_chat_template(conversation: list[dict[str, str]] | list[list[dict[str, str]]], tools: list[dict | collections.abc.Callable] | None = None, add_generation_prompt: bool = False, continue_final_message: bool = False, tokenize: bool = True, padding: bool | str | transformers.utils.generic.PaddingStrategy = False, truncation: bool = False, max_length: int | None = None, return_tensors: str | transformers.utils.generic.TensorType | None = None, return_dict: bool = True, reasoning_effort: ReasoningEffort | None = None, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1038)

**Parameters:**

conversation (Union[List[Dict[str, str]], List[List[Dict[str, str]]]]) : A list of dicts with "role" and "content" keys, representing the chat history so far.

tools (`List[Union[Dict, Callable]]`, *optional*) : A list of tools (callable functions) that will be accessible to the model. If the template does not support function calling, this argument will have no effect. Each tool should be passed as a JSON Schema, giving the name, description and argument types for the tool. See our [chat templating guide](https://huggingface.co/docs/transformers/main/en/chat_templating#automated-function-conversion-for-tool-use) for more information.

add_generation_prompt (`bool`, *optional*) : This argument is a no-op for `MistralCommonBackend`. However, it cannot be used at the same time as `continue_final_message` to keep the API consistent. If any conversation ends with an assistant message, it will raise an error. In such cases, use `continue_final_message` instead.

continue_final_message (bool, *optional*) : If this is set, the chat will be formatted so that the final message in the chat is open-ended, without any EOS tokens. The model will continue this message rather than starting a new one. This allows you to "prefill" part of the model's response for it. Cannot be used at the same time as `add_generation_prompt`.

tokenize (`bool`, defaults to `True`) : Whether to tokenize the output. If `False`, the output will be a string.

padding (`bool`, `str` or [PaddingStrategy](/docs/transformers/v5.22.2/en/internal/file_utils#transformers.utils.PaddingStrategy), *optional*, defaults to `False`) : Select a strategy to pad the returned sequences (according to the model's padding side and padding index) among:  - `True` or `'longest'`: Pad to the longest sequence in the batch (or no padding if only a single sequence if provided). - `'max_length'`: Pad to a maximum length specified with the argument `max_length` or to the maximum acceptable input length for the model if that argument is not provided. - `False` or `'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of different lengths).

truncation (`bool`, defaults to `False`) : Whether to truncate sequences at the maximum length. Has no effect if tokenize is `False`.

max_length (`int`, *optional*) : Maximum length (in tokens) to use for padding or truncation. Has no effect if tokenize is `False`. If not specified, the tokenizer's `max_length` attribute will be used as a default.

return_tensors (`str` or [TensorType](/docs/transformers/v5.22.2/en/internal/file_utils#transformers.TensorType), *optional*) : If set, will return tensors of a particular framework. Has no effect if tokenize is `False`. Acceptable values are: - `'pt'`: Return PyTorch `torch.Tensor` objects.

return_dict (`bool`, defaults to `False`) : Whether to return a dictionary with named outputs. Has no effect if tokenize is `False`. If at least one conversation contains an image, its pixel values will be returned in the `pixel_values` key and image sizes in the `image_sizes` key.

reasoning_effort (`ReasoningEffort`, *optional*) : The reasoning effort to use for the chat completion for models that support it. Possible values are: - `ReasoningEffort.none`: The model will not reason. - `ReasoningEffort.high`: The model will use a reasoning approach. If not specified, the default reasoning effort will be used. 

kwargs (additional keyword arguments, *optional*) : Additional arguments passed to the mistral-common `ChatCompletionRequest.from_openai` method.

**Returns:** `Union[str, list[int], list[str], list[list[int]], BatchEncoding]`

The tokenized chat so far, including control tokens. This output is ready to pass to the model, either directly or via methods like `generate()`.

Converts a list of dictionaries with `"role"` and `"content"` keys to a list of token
ids.

#### batch_decode[[transformers.MistralCommonBackend.batch_decode]]

```python
batch_decode(sequences: typing.Union[list[int], list[list[int]], numpy.ndarray, ForwardRef('torch.Tensor')], skip_special_tokens: bool = False, clean_up_tokenization_spaces: bool | None = None, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L512)

**Parameters:**

sequences (`Union[list[int], list[list[int]], np.ndarray, torch.Tensor]`) : List of tokenized input ids. Can be obtained using the `__call__` method.

skip_special_tokens (`bool`, *optional*, defaults to `False`) : Whether or not to remove special tokens in the decoding.

clean_up_tokenization_spaces (`bool`, *optional*) : Whether or not to clean up the tokenization spaces. If `None`, will default to `self.clean_up_tokenization_spaces`.

kwargs (additional keyword arguments, *optional*) : Not supported by `MistralCommonBackend.batch_decode`. Will raise an error if used.

**Returns:** `list[str]`

The list of decoded sentences.

Convert a list of lists of token ids into a list of strings by calling decode.

This method is provided for backwards compatibility. The `decode` method now handles batched input natively,
so you can use `decode` directly instead of `batch_decode`.

#### build_inputs_with_special_tokens[[transformers.MistralCommonBackend.build_inputs_with_special_tokens]]

```python
build_inputs_with_special_tokens(token_ids_0: list, token_ids_1: None = None)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1284)

**Parameters:**

token_ids_0 (`list[int]`) : List of IDs to which the special tokens will be added.

token_ids_1 (`None`, *optional*) : None, kept to match Transformers' signature.

**Returns:** `list[int]`

List of input IDs with the appropriate special tokens.

Build model inputs from a sequence by adding special tokens.

This method dynamically builds inputs based on the tokenizer's `mode`:
- `"test"`: seq0 [EOS]
- `"finetuning"`: [BOS] seq0

#### convert_added_tokens[[transformers.MistralCommonBackend.convert_added_tokens]]

```python
convert_added_tokens(obj: tokenizers.AddedToken | typing.Any, save: bool = False, add_type_field: bool = True)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1704)

`MistralCommonBackend` does not implement `convert_added_tokens` by design.

If you would like this behaviour to be implemented, please open an issue in the `Transformers` or `mistral-common` repositories to request it.

#### create_token_type_ids_from_sequences[[transformers.MistralCommonBackend.create_token_type_ids_from_sequences]]

```python
create_token_type_ids_from_sequences(token_ids_0: list, token_ids_1: None = None)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1313)

**Parameters:**

token_ids_0 (`list[int]`) : List of IDs.

token_ids_1 (`None`, *optional*) : None, kept to match Transformers' signature.

**Returns:** `list[int]`

Token type IDs according to the configured pattern.

Create a mask of zeroes from the token ids with special tokens added.

Kept to match Transformers' implementation.

#### decode[[transformers.MistralCommonBackend.decode]]

```python
decode(token_ids: typing.Union[int, list[int], list[list[int]], numpy.ndarray, ForwardRef('torch.Tensor')], skip_special_tokens: bool = False, clean_up_tokenization_spaces: bool | None = None, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L475)

**Parameters:**

token_ids (`Union[int, list[int], list[list[int]], np.ndarray, torch.Tensor]`) : A single sequence or a batch (list of sequences) of tokenized input ids. Can be obtained using the `__call__` method.

skip_special_tokens (`bool`, *optional*, defaults to `False`) : Whether or not to remove special tokens in the decoding.

clean_up_tokenization_spaces (`bool`, *optional*) : Whether or not to clean up the tokenization spaces. If `None`, will default to `self.clean_up_tokenization_spaces`.

kwargs (additional keyword arguments, *optional*) : Not supported by `MistralCommonBackend.decode`. Will raise an error if used.

**Returns:** `Union[str, list[str]]`

The decoded string for a single sequence, or a list of decoded strings for a
batch of sequences.

Converts a sequence of ids in a string, using the tokenizer and vocabulary with options to remove special
tokens and clean up tokenization spaces.

#### encode[[transformers.MistralCommonBackend.encode]]

```python
encode(text: str | list[int], text_pair: None = None, add_special_tokens: bool = True, padding: bool | str | transformers.utils.generic.PaddingStrategy = False, truncation: bool | str | transformers.tokenization_utils_base.TruncationStrategy | None = None, max_length: int | None = None, stride: int = 0, pad_to_multiple_of: int | None = None, padding_side: str | None = None, return_tensors: str | transformers.utils.generic.TensorType | None = None, verbose: bool = True, return_offsets_mapping: typing.Literal[False] = False, split_special_tokens: typing.Literal[False] = False, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L378)

**Parameters:**

text (`str` or `list[int]`) : The first sequence to be encoded. This can be a string or a list of integers (tokenized string ids).

text_pair (`None`, *optional*) : Not supported by `MistralCommonBackend.encode`. Kept to match `PreTrainedTokenizerBase.encode` signature. 

add_special_tokens (`bool`, *optional*, defaults to `True`) : Whether or not to add special tokens when encoding the sequences. This will use the underlying `PretrainedTokenizerBase.build_inputs_with_special_tokens` function, which defines which tokens are automatically added to the input ids. This is useful if you want to add `bos` or `eos` tokens automatically. When Tokenizer is loading with `finetuning` mode it adds both `bos` and `eos`. Else, for "test" mode it only adds `bos`.

padding (`bool`, `str` or [PaddingStrategy](/docs/transformers/v5.22.2/en/internal/file_utils#transformers.utils.PaddingStrategy), *optional*, defaults to `False`) : Activates and controls padding. Accepts the following values:  - `True` or `'longest'`: Pad to the longest sequence in the batch (or no padding if only a single sequence is provided). - `'max_length'`: Pad to a maximum length specified with the argument `max_length` or to the maximum acceptable input length for the model if that argument is not provided. - `False` or `'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of different lengths).

truncation (`bool`, `str` or [TruncationStrategy](/docs/transformers/v5.22.2/en/internal/tokenization_utils#transformers.tokenization_utils_base.TruncationStrategy), *optional*, defaults to `False`) : Activates and controls truncation. Accepts the following values:  - `True` or `'longest_first'`: Truncate to a maximum length specified with the argument `max_length` or to the maximum acceptable input length for the model if that argument is not provided. - `False` or `'do_not_truncate'` (default): No truncation (i.e., can output batch with sequence lengths greater than the model maximum admissible input size).

max_length (`int`, *optional*) : Controls the maximum length to use by one of the truncation/padding parameters.  If left unset or set to `None`, this will use the predefined model maximum length if a maximum length is required by one of the truncation/padding parameters. If the model has no specific maximum input length (like XLNet) truncation/padding to a maximum length will be deactivated.

stride (`int`, *optional*, defaults to 0) : If set to a number along with `max_length`, the overflowing tokens returned when `return_overflowing_tokens=True` will contain some tokens from the end of the truncated sequence returned to provide some overlap between truncated and overflowing sequences. The value of this argument defines the number of overlapping tokens.

pad_to_multiple_of (`int`, *optional*) : If set will pad the sequence to a multiple of the provided value. Requires `padding` to be activated. This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability `>= 7.5` (Volta).

padding_side (`str`, *optional*) : The side on which the model should have padding applied. Should be selected between ['right', 'left']. Default value is picked from the class attribute of the same name.

return_tensors (`str` or [TensorType](/docs/transformers/v5.22.2/en/internal/file_utils#transformers.TensorType), *optional*) : If set, will return tensors instead of list of python integers. Acceptable values are:  - `'pt'`: Return PyTorch `torch.Tensor` objects. 

- ****kwargs** : Not supported by `MistralCommonBackend.encode`. Will raise an error if used.

**Returns:** `list[int]`, `torch.Tensor`

The tokenized ids of the text.

Converts a string to a sequence of ids (integer), using the tokenizer and vocabulary.

#### from_pretrained[[transformers.MistralCommonBackend.from_pretrained]]

```python
from_pretrained(pretrained_model_name_or_path: str | os.PathLike, *init_inputs, mode: str | ValidationMode = 'test', cache_dir: str | os.PathLike | None = None, force_download: bool = False, local_files_only: bool = False, token: str | bool | None = None, revision: str = 'main', model_max_length: int = 1000000000000000019884624838656, padding_side: str = 'left', truncation_side: str = 'right', model_input_names: list[str] | None = None, clean_up_tokenization_spaces: bool = False, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1437)

**Parameters:**

pretrained_model_name_or_path (`str` or `os.PathLike`) : Can be either:  - A string, the *model id* of a predefined tokenizer hosted inside a model repo on huggingface.co. - A path to a *directory* containing the tokenizer config, for instance saved using the `MistralCommonBackend.tokenization_mistral_common.save_pretrained` method, e.g., `./my_model_directory/`.

mode (`Union[str, ValidationMode]`, *optional*, defaults to `ValidationMode.test`) : Validation mode for the `MistralTokenizer` tokenizer. Possible values are: - `"finetuning"` or `ValidationMode.finetuning`: The fine-tuning mode. - `"test"` or `ValidationMode.test`: The test mode. It changes how the tokenizer validates the input and prepares the request to the model.

cache_dir (`str` or `os.PathLike`, *optional*) : Path to a directory in which a downloaded predefined tokenizer vocabulary files should be cached if the standard cache should not be used.

force_download (`bool`, *optional*, defaults to `False`) : Whether or not to force the (re-)download the vocabulary files and override the cached versions if they exist.

token (`str` or *bool*, *optional*) : The token to use as HTTP bearer authorization for remote files. If `True`, will use the token generated when running `hf auth login` (stored in `~/.huggingface`).

local_files_only (`bool`, *optional*, defaults to `False`) : Whether or not to only rely on local files and not to attempt to download any files.

revision (`str`, *optional*, defaults to `"main"`) : The specific model version to use. It can be a branch name, a tag name, or a commit id, since we use a git-based system for storing models and other artifacts on huggingface.co, so `revision` can be any identifier allowed by git.

max_length (`int`, *optional*) : Controls the maximum length to use by one of the truncation/padding parameters.  If left unset or set to `None`, this will use the predefined model maximum length if a maximum length is required by one of the truncation/padding parameters. If the model has no specific maximum input length (like XLNet) truncation/padding to a maximum length will be deactivated.

padding_side (`str`, *optional*, defaults to `"left"`) : The side on which the model should have padding applied. Should be selected between ['right', 'left']. Default value is picked from the class attribute of the same name.

truncation_side (`str`, *optional*, defaults to `"right"`) : The side on which the model should have truncation applied. Should be selected between ['right', 'left'].

model_input_names (`List[str]`, *optional*) : The list of inputs accepted by the forward pass of the model (like `"token_type_ids"` or `"attention_mask"`). Default value is picked from the class attribute of the same name.

clean_up_tokenization_spaces (`bool`, *optional*, defaults to `False`) : Whether or not the model should clean up the spaces that were added when splitting the input text during the tokenization process.

kwargs (additional keyword arguments, *optional*) : Not supported by `MistralCommonBackend.from_pretrained`. Will raise an error if used.

Instantiate a `MistralCommonBackend` from a predefined
tokenizer.

#### get_chat_template[[transformers.MistralCommonBackend.get_chat_template]]

```python
get_chat_template(chat_template: str | None = None, tools: list[dict] | None = None)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1713)

`MistralCommonBackend` does not implement `get_chat_template` by design as `mistral-common` does not use chat templates.

#### get_special_tokens_mask[[transformers.MistralCommonBackend.get_special_tokens_mask]]

```python
get_special_tokens_mask(token_ids_0: list, token_ids_1: None = None, already_has_special_tokens: bool = False)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L691)

**Parameters:**

token_ids_0 (`list[int]`) : List of ids of the sequence.

token_ids_1 (`None`, *optional*) : None, kept to match Transformers' implementation.

already_has_special_tokens (`bool`, *optional*, defaults to `False`) : Whether or not the token list is already formatted with special tokens for the model.

**Returns:** A list of integers in the range [0, 1]

1 for a special token, 0 for a sequence token.

Retrieves sequence ids from a token list that has no special tokens added. This method is called when adding
special tokens using the tokenizer `prepare_for_model` or `encode_plus` methods.

#### get_vocab[[transformers.MistralCommonBackend.get_vocab]]

```python
get_vocab()
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L352)

**Returns:** `Dict[str, int]`

The vocabulary.

Returns the vocabulary as a dictionary of token to index.

This is a lossy conversion. There may be multiple token ids that decode to the same
string due to partial UTF-8 byte sequences being converted to �.

#### num_special_tokens_to_add[[transformers.MistralCommonBackend.num_special_tokens_to_add]]

```python
num_special_tokens_to_add(pair: typing.Literal[False] = False)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1337)

**Parameters:**

pair (`Literal[False]`, *optional*) : False, kept to match Transformer's signature.

**Returns:** `int`

Number of special tokens added to sequences.

Returns the number of added tokens when encoding a sequence with special tokens.

This encodes a dummy input and checks the number of added tokens, and is therefore not efficient. Do not put
this inside your training loop.

#### prepare_for_model[[transformers.MistralCommonBackend.prepare_for_model]]

```python
prepare_for_model(ids: list, pair_ids: None = None, add_special_tokens: bool = True, padding: bool | str | transformers.utils.generic.PaddingStrategy = False, truncation: bool | str | transformers.tokenization_utils_base.TruncationStrategy | None = None, max_length: int | None = None, stride: int = 0, pad_to_multiple_of: int | None = None, padding_side: str | None = None, return_tensors: str | transformers.utils.generic.TensorType | None = None, return_token_type_ids: bool | None = None, return_attention_mask: bool | None = None, return_overflowing_tokens: bool = False, return_special_tokens_mask: bool = False, return_length: bool = False, verbose: bool = True, prepend_batch_axis: bool = False, return_offsets_mapping: typing.Literal[False] = False, split_special_tokens: typing.Literal[False] = False, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L844)

**Parameters:**

ids (`list[int]`) : Tokenized input ids of the first sequence.

pair_ids (`None`, *optional*) : Not supported by `MistralCommonBackend`. Kept to match the interface of `PreTrainedTokenizerBase`. 

add_special_tokens (`bool`, *optional*, defaults to `True`) : Whether or not to add special tokens when encoding the sequences. This will use the underlying `PretrainedTokenizerBase.build_inputs_with_special_tokens` function, which defines which tokens are automatically added to the input ids. This is useful if you want to add `bos` or `eos` tokens automatically. When Tokenizer is loading with `finetuning` mode it adds both `bos` and `eos`. Else, for "test" mode it only adds `bos`.

padding (`bool`, `str` or [PaddingStrategy](/docs/transformers/v5.22.2/en/internal/file_utils#transformers.utils.PaddingStrategy), *optional*, defaults to `False`) : Activates and controls padding. Accepts the following values:  - `True` or `'longest'`: Pad to the longest sequence in the batch (or no padding if only a single sequence is provided). - `'max_length'`: Pad to a maximum length specified with the argument `max_length` or to the maximum acceptable input length for the model if that argument is not provided. - `False` or `'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of different lengths).

truncation (`bool`, `str` or [TruncationStrategy](/docs/transformers/v5.22.2/en/internal/tokenization_utils#transformers.tokenization_utils_base.TruncationStrategy), *optional*, defaults to `False`) : Activates and controls truncation. Accepts the following values:  - `True` or `'longest_first'`: Truncate to a maximum length specified with the argument `max_length` or to the maximum acceptable input length for the model if that argument is not provided. - `False` or `'do_not_truncate'` (default): No truncation (i.e., can output batch with sequence lengths greater than the model maximum admissible input size).

max_length (`int`, *optional*) : Controls the maximum length to use by one of the truncation/padding parameters.  If left unset or set to `None`, this will use the predefined model maximum length if a maximum length is required by one of the truncation/padding parameters. If the model has no specific maximum input length (like XLNet) truncation/padding to a maximum length will be deactivated.

stride (`int`, *optional*, defaults to 0) : If set to a number along with `max_length`, the overflowing tokens returned when `return_overflowing_tokens=True` will contain some tokens from the end of the truncated sequence returned to provide some overlap between truncated and overflowing sequences. The value of this argument defines the number of overlapping tokens.

pad_to_multiple_of (`int`, *optional*) : If set will pad the sequence to a multiple of the provided value. Requires `padding` to be activated. This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability `>= 7.5` (Volta).

padding_side (`str`, *optional*) : The side on which the model should have padding applied. Should be selected between ['right', 'left']. Default value is picked from the class attribute of the same name.

return_tensors (`str` or [TensorType](/docs/transformers/v5.22.2/en/internal/file_utils#transformers.TensorType), *optional*) : If set, will return tensors instead of list of python integers. Acceptable values are:  - `'pt'`: Return PyTorch `torch.Tensor` objects. 

return_token_type_ids (`bool`, *optional*) : Whether to return token type IDs. For `MistralCommonBackend` it returns a list of zeros of the sequence length as only one sequence is supported.  [What are token type IDs?](../glossary#token-type-ids)

return_attention_mask (`bool`, *optional*) : Whether to return the attention mask. If left to the default, will return the attention mask according to the specific tokenizer's default, defined by the `return_outputs` attribute.  [What are attention masks?](../glossary#attention-mask)

return_overflowing_tokens (`bool`, *optional*, defaults to `False`) : Whether or not to return overflowing token sequences. If a pair of sequences of input ids (or a batch of pairs) is provided with `truncation_strategy = longest_first` or `True`, an error is raised instead of returning overflowing tokens.

return_special_tokens_mask (`bool`, *optional*, defaults to `False`) : Whether or not to return special tokens mask information.

return_length  (`bool`, *optional*, defaults to `False`) : Whether or not to return the lengths of the encoded inputs.

verbose (`bool`, *optional*, defaults to `True`) : Whether or not to print more information and warnings.

return_offsets_mapping (`Literal[False]`, *optional*) : False, kept to match Transformers' signature.

split_special_tokens (`Literal[False]`, *optional*) : False, kept to match Transformers' signature.

- ****kwargs** : passed to the `self.tokenize()` method

**Returns:** [BatchEncoding](/docs/transformers/v5.22.2/en/main_classes/tokenizer#transformers.BatchEncoding)

A [BatchEncoding](/docs/transformers/v5.22.2/en/main_classes/tokenizer#transformers.BatchEncoding) with the following fields:

- **input_ids** -- List of token ids to be fed to a model.

  [What are input IDs?](../glossary#input-ids)

- **attention_mask** -- List of indices specifying which tokens should be attended to by the model (when
  `return_attention_mask=True` or if *"attention_mask"* is in `self.model_input_names`).

  [What are attention masks?](../glossary#attention-mask)

- **overflowing_tokens** -- List of overflowing tokens sequences (when a `max_length` is specified and
  `return_overflowing_tokens=True`).
- **num_truncated_tokens** -- Number of tokens truncated (when a `max_length` is specified and
  `return_overflowing_tokens=True`).
- **special_tokens_mask** -- List of 0s and 1s, with 1 specifying added special tokens and 0 specifying
  regular sequence tokens (when `add_special_tokens=True` and `return_special_tokens_mask=True`).
- **length** -- The length of the inputs (when `return_length=True`)

Prepares a sequence of input id so that it can be used by the model. It
adds special tokens, truncates sequences if overflowing while taking into account the special tokens and
manages a moving window (with user defined stride) for overflowing tokens.

#### save_chat_templates[[transformers.MistralCommonBackend.save_chat_templates]]

```python
save_chat_templates(save_directory: str | os.PathLike, tokenizer_config: dict, filename_prefix: str | None, save_jinja_files: bool)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1718)

`MistralCommonBackend` does not implement `save_chat_templates` by design as `mistral-common` does not use chat templates.

#### save_pretrained[[transformers.MistralCommonBackend.save_pretrained]]

```python
save_pretrained(save_directory: str | os.PathLike | pathlib.Path, push_to_hub: bool = False, token: str | bool | None = None, commit_message: str | None = None, repo_id: str | None = None, private: bool | None = None, save_format: str | None = None, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1552)

**Parameters:**

save_directory (`str | os.PathLike | Path`) : Directory where the tokenizer will be saved.

push_to_hub (`bool`, *optional*, defaults to `False`) : Push to the HF Hub after saving.

token (`str` or `bool`, *optional*) : Token for Hub authentication.

commit_message (`str`, *optional*) : Commit message when pushing.

repo_id (`str`, *optional*) : Hub repository id.

private (`bool`, *optional*) : Whether the repository is private.

save_format (`str`, *optional*) : `"mistral"` to save native tekken format, `"hf"` for HuggingFace format.  *None* preserves the original format.

kwargs (`dict`, *optional*) : Not supported — will raise an error.

**Returns:** `tuple[str, ...]`

Paths of the saved files.

Save the full tokenizer state.

When `save_format` is `"mistral"` (or *None* for a tekken tokenizer),
the original tokenizer file (e.g. `tekken.json`) is written to
*save_directory*.  When `save_format` is `"hf"`, HF-format files
(`tokenizer.json` + `tokenizer_config.json`) are produced instead.

#### save_vocabulary[[transformers.MistralCommonBackend.save_vocabulary]]

```python
save_vocabulary(save_directory: str, filename_prefix: str | None = None)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L1729)

`MistralCommonBackend` does not implement `save_vocabulary` by design.

This is because `mistral-common` is configured by one tokenizer file. If you'd like to save the vocabulary, please consider using the `save_pretrained` method instead.

#### tokenize[[transformers.MistralCommonBackend.tokenize]]

```python
tokenize(text: str, return_offsets_mapping: typing.Literal[False] = False, split_special_tokens: typing.Literal[False] = False, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L645)

**Parameters:**

text (`str`) : The sequence to be encoded.

return_offsets_mapping (`Literal[False]`, *optional*) : False, kept to match Transformers' signature.

split_special_tokens (`Literal[False]`, *optional*) : False, kept to match Transformers' signature.

- ****kwargs** (additional keyword arguments) : Not supported by `MistralCommonBackend.tokenize`. Will raise an error if used.

**Returns:** `list[str]`

The list of tokens.

Converts a string into a sequence of tokens, using the tokenizer.

Split in words for word-based vocabulary or sub-words for sub-word-based vocabularies.

#### truncate_sequences[[transformers.MistralCommonBackend.truncate_sequences]]

```python
truncate_sequences(ids: list, pair_ids: None = None, num_tokens_to_remove: int = 0, truncation_strategy: str | transformers.tokenization_utils_base.TruncationStrategy = 'longest_first', stride: int = 0, **kwargs)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/tokenization_mistral_common.py#L974)

**Parameters:**

ids (`list[int]`) : Tokenized input ids. Can be obtained from a string by chaining the `tokenize` and `convert_tokens_to_ids` methods.

pair_ids (`None`, *optional*) : Not supported by `MistralCommonBackend`. Kept to match the signature of `PreTrainedTokenizerBase.truncate_sequences`.

num_tokens_to_remove (`int`, *optional*, defaults to 0) : Number of tokens to remove using the truncation strategy.

truncation_strategy (`str` or [TruncationStrategy](/docs/transformers/v5.22.2/en/internal/tokenization_utils#transformers.tokenization_utils_base.TruncationStrategy), *optional*, defaults to `'longest_first'`) : The strategy to follow for truncation. Can be:  - `'longest_first'`: Truncate to a maximum length specified with the argument `max_length` or to the maximum acceptable input length for the model if that argument is not provided. - `'do_not_truncate'` (default): No truncation (i.e., can output batch with sequence lengths greater than the model maximum admissible input size).

stride (`int`, *optional*, defaults to 0) : If set to a positive number, the overflowing tokens returned will contain some tokens from the main sequence returned. The value of this argument defines the number of additional tokens.

**Returns:** `Tuple[list[int], None, list[int]]`

The truncated `ids` and the list of
overflowing tokens. `None` is returned to match Transformers signature.

Truncates a sequence pair in-place following the strategy.

## Mistral3Model[[transformers.Mistral3Model]]

#### transformers.Mistral3Model[[transformers.Mistral3Model]]

```python
transformers.Mistral3Model(config: Mistral3Config)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/models/mistral3/modeling_mistral3.py#L199)

**Parameters:**

config ([Mistral3Config](/docs/transformers/v5.22.2/en/model_doc/mistral3#transformers.Mistral3Config)) : Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the [from_pretrained()](/docs/transformers/v5.22.2/en/main_classes/model#transformers.PreTrainedModel.from_pretrained) method to load the model weights.

The Mistral3 model which consists of a vision backbone and a language model, without a language modeling head.

This model inherits from [PreTrainedModel](/docs/transformers/v5.22.2/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)

This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.

#### forward[[transformers.Mistral3Model.forward]]

```python
forward(input_ids: typing.Optional[torch.LongTensor] = None, pixel_values: typing.Optional[torch.FloatTensor] = None, attention_mask: typing.Optional[torch.Tensor] = None, position_ids: typing.Optional[torch.LongTensor] = None, past_key_values: transformers.cache_utils.Cache | None = None, inputs_embeds: typing.Optional[torch.FloatTensor] = None, vision_feature_layer: int | list[int] | None = None, use_cache: bool | None = None, image_sizes: typing.Optional[torch.Tensor] = None, mm_encoder_outputs: dict[str, transformers.modeling_outputs.BaseModelOutputWithPooling] | None = None, **kwargs: *<class 'transformers.utils.generic.TransformersKwargs'>)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/models/mistral3/modeling_mistral3.py#L269)

**Parameters:**

input_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*) : Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.  Indices can be obtained using [AutoTokenizer](/docs/transformers/v5.22.2/en/model_doc/auto#transformers.AutoTokenizer). See [PreTrainedTokenizer.encode()](/docs/transformers/v5.22.2/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode) and [PreTrainedTokenizer.__call__()](/docs/transformers/v5.22.2/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__) for details.  [What are input IDs?](../glossary#input-ids)

pixel_values (`torch.FloatTensor` of shape `(batch_size, num_channels, image_size, image_size)`, *optional*) : The tensors corresponding to the input images. Pixel values can be obtained using [PixtralImageProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralImageProcessor). See [PixtralImageProcessor.__call__()](/docs/transformers/v5.22.2/en/model_doc/molmo2#transformers.Molmo2ImageProcessor.__call__) for details ([PixtralProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralProcessor) uses [PixtralImageProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralImageProcessor) for processing images).

attention_mask (`torch.Tensor` of shape `(batch_size, sequence_length)`, *optional*) : Mask to avoid performing attention on padding token indices. Mask values selected in `[0, 1]`:  - 1 for tokens that are **not masked**, - 0 for tokens that are **masked**.  [What are attention masks?](../glossary#attention-mask)

position_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*) : Indices of positions of each input sequence tokens in the position embeddings. Selected in the range `[0, config.n_positions - 1]`.  [What are position IDs?](../glossary#position-ids)

past_key_values (`~cache_utils.Cache`, *optional*) : Pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention blocks) that can be used to speed up sequential decoding. This typically consists in the `past_key_values` returned by the model at a previous stage of decoding, when `use_cache=True` or `config.use_cache=True`.  Only [Cache](/docs/transformers/v5.22.2/en/internal/generation_utils#transformers.Cache) instance is allowed as input, see our [kv cache guide](https://huggingface.co/docs/transformers/en/kv_cache). If no `past_key_values` are passed, [DynamicCache](/docs/transformers/v5.22.2/en/internal/generation_utils#transformers.DynamicCache) will be initialized by default.  The model will output the same cache format that is fed as input.  If `past_key_values` are used, the user is expected to input only unprocessed `input_ids` (those that don't have their past key value states given to this model) of shape `(batch_size, unprocessed_length)` instead of all `input_ids` of shape `(batch_size, sequence_length)`.

inputs_embeds (`torch.FloatTensor` of shape `(batch_size, sequence_length, hidden_size)`, *optional*) : Optionally, instead of passing `input_ids` you can choose to directly pass an embedded representation. This is useful if you want more control over how to convert `input_ids` indices into associated vectors than the model's internal embedding lookup matrix.

vision_feature_layer (`Union[int, list[int]]`, *optional*) : The index of the layer to select the vision feature. If multiple indices are provided, the vision feature of the corresponding indices will be concatenated to form the vision features.

use_cache (`bool`, *optional*) : If set to `True`, `past_key_values` key value states are returned and can be used to speed up decoding (see `past_key_values`).

image_sizes (`torch.Tensor` of shape `(batch_size, 2)`, *optional*) : The sizes of the images in the batch, being (height, width) for each image.

mm_encoder_outputs (`dict[str, ~modeling_outputs.BaseModelOutputWithPooling]`, *optional*) : Dict where keys are supported modalities and values are encoded outputs for that modality. Each encoded output is a tuple that consists of (`pooler_output`, *optional*: `last_hidden_states`, *optional*: `hidden_states`, *optional*: `attentions`) `pooler_output` of shape `(batch_size, sequence_length, hidden_size)`, *optional*) is a sequence of multimmodal features of the encoder merged into text embeddings.

**Returns:** `Mistral3ModelOutputWithPast` or `tuple(torch.FloatTensor)`

A `Mistral3ModelOutputWithPast` or a tuple of
`torch.FloatTensor` (if `return_dict=False` is passed or when `config.return_dict=False`) comprising various
elements depending on the configuration ([Mistral3Config](/docs/transformers/v5.22.2/en/model_doc/mistral3#transformers.Mistral3Config)) and inputs.

The [Mistral3Model](/docs/transformers/v5.22.2/en/model_doc/mistral3#transformers.Mistral3Model) forward method, overrides the `__call__` special method.

Although the recipe for forward pass needs to be defined within this function, one should call the `Module`
instance afterwards instead of this since the former takes care of running the pre and post processing steps while
the latter silently ignores them.

- **last_hidden_state** (`torch.FloatTensor` of shape `(batch_size, sequence_length, hidden_size)`) -- Sequence of hidden-states at the output of the last layer of the model.

  If `past_key_values` is used only the last hidden-state of the sequences of shape `(batch_size, 1,
  hidden_size)` is output.
- **past_key_values** (`Cache`, *optional*, returned when `use_cache=True` is passed or when `config.use_cache=True`) -- It is a [Cache](/docs/transformers/v5.22.2/en/internal/generation_utils#transformers.Cache) instance. For more details, see our [kv cache guide](https://huggingface.co/docs/transformers/en/kv_cache).

  Contains pre-computed hidden-states (key and values in the self-attention blocks) that can be used (see
  `past_key_values` input) to speed up sequential decoding.
- **hidden_states** (`tuple(torch.FloatTensor)`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +
  one for the output of each layer) of shape `(batch_size, sequence_length, hidden_size)`.

  Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.
- **attentions** (`tuple(torch.FloatTensor)`, *optional*, returned when `output_attentions=True` is passed or when `config.output_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch_size, num_heads, sequence_length,
  sequence_length)`.

  Attentions weights after the attention softmax, used to compute the weighted average in the self-attention
  heads.
- **image_hidden_states** (`torch.FloatTensor`, *optional*) -- A `torch.FloatTensor` of size `(batch_size, num_images, sequence_length, hidden_size)`.
  image_hidden_states of the model produced by the vision encoder and after projecting the last hidden state.

#### get_image_features[[transformers.Mistral3Model.get_image_features]]

```python
get_image_features(pixel_values: FloatTensor, image_sizes: Tensor, vision_feature_layer: int | list[int] | None = None, **kwargs: *<class 'transformers.utils.generic.TransformersKwargs'>)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/models/mistral3/modeling_mistral3.py#L208)

**Parameters:**

pixel_values (`torch.FloatTensor` of shape `(batch_size, num_channels, image_size, image_size)`) : The tensors corresponding to the input images. Pixel values can be obtained using [PixtralImageProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralImageProcessor). See [PixtralImageProcessor.__call__()](/docs/transformers/v5.22.2/en/model_doc/molmo2#transformers.Molmo2ImageProcessor.__call__) for details ([PixtralProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralProcessor) uses [PixtralImageProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralImageProcessor) for processing images).

image_sizes (`torch.Tensor` of shape `(batch_size, 2)`) : The sizes of the images in the batch, being (height, width) for each image.

vision_feature_layer (`Union[int, list[int]]`, *optional*) : The index of the layer to select the vision feature. If multiple indices are provided, the vision feature of the corresponding indices will be concatenated to form the vision features.

**Returns:** [BaseModelOutputWithPooling](/docs/transformers/v5.22.2/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)`

A [BaseModelOutputWithPooling](/docs/transformers/v5.22.2/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or a tuple of
`torch.FloatTensor` (if `return_dict=False` is passed or when `config.return_dict=False`) comprising various
elements depending on the configuration ([Mistral3Config](/docs/transformers/v5.22.2/en/model_doc/mistral3#transformers.Mistral3Config)) and inputs.

Obtains image last hidden states from the vision tower and apply multimodal projection.

- **last_hidden_state** (`torch.FloatTensor` of shape `(batch_size, sequence_length, hidden_size)`) -- Sequence of hidden-states at the output of the last layer of the model.
- **pooler_output** (`torch.FloatTensor` of shape `(batch_size, hidden_size)`) -- Last layer hidden-state of the first token of the sequence (classification token) after further processing
  through the layers used for the auxiliary pretraining task. E.g. for BERT-family of models, this returns
  the classification token after processing through a linear layer and a tanh activation function. The linear
  layer weights are trained from the next sentence prediction (classification) objective during pretraining.
- **hidden_states** (`tuple(torch.FloatTensor)`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +
  one for the output of each layer) of shape `(batch_size, sequence_length, hidden_size)`.

  Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.
- **attentions** (`tuple(torch.FloatTensor)`, *optional*, returned when `output_attentions=True` is passed or when `config.output_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch_size, num_heads, sequence_length,
  sequence_length)`.

  Attentions weights after the attention softmax, used to compute the weighted average in the self-attention
  heads.

#### get_placeholder_mask[[transformers.Mistral3Model.get_placeholder_mask]]

```python
get_placeholder_mask(input_ids: LongTensor, inputs_embeds: FloatTensor, image_features: FloatTensor)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/models/mistral3/modeling_mistral3.py#L245)

Obtains multimodal placeholder mask from `input_ids` or `inputs_embeds`, and checks that the placeholder token count is
equal to the length of multimodal features. If the lengths are different, an error is raised.

## Mistral3ForConditionalGeneration[[transformers.Mistral3ForConditionalGeneration]]

#### transformers.Mistral3ForConditionalGeneration[[transformers.Mistral3ForConditionalGeneration]]

```python
transformers.Mistral3ForConditionalGeneration(config: Mistral3Config)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/models/mistral3/modeling_mistral3.py#L336)

**Parameters:**

config ([Mistral3Config](/docs/transformers/v5.22.2/en/model_doc/mistral3#transformers.Mistral3Config)) : Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the [from_pretrained()](/docs/transformers/v5.22.2/en/main_classes/model#transformers.PreTrainedModel.from_pretrained) method to load the model weights.

The MISTRAL3 model which consists of a vision backbone and a language model.

This model inherits from [PreTrainedModel](/docs/transformers/v5.22.2/en/main_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the
library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads
etc.)

This model is also a PyTorch [torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.
Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage
and behavior.

#### forward[[transformers.Mistral3ForConditionalGeneration.forward]]

```python
forward(input_ids: typing.Optional[torch.LongTensor] = None, pixel_values: typing.Optional[torch.FloatTensor] = None, attention_mask: typing.Optional[torch.Tensor] = None, position_ids: typing.Optional[torch.LongTensor] = None, past_key_values: transformers.cache_utils.Cache | None = None, inputs_embeds: typing.Optional[torch.FloatTensor] = None, labels: typing.Optional[torch.LongTensor] = None, use_cache: bool | None = None, logits_to_keep: typing.Union[int, torch.Tensor] = 0, image_sizes: typing.Optional[torch.Tensor] = None, mm_encoder_outputs: dict[str, transformers.modeling_outputs.BaseModelOutputWithPooling] | None = None, **kwargs: *<class 'transformers.utils.generic.TransformersKwargs'>)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/models/mistral3/modeling_mistral3.py#L366)

**Parameters:**

input_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*) : Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.  Indices can be obtained using [AutoTokenizer](/docs/transformers/v5.22.2/en/model_doc/auto#transformers.AutoTokenizer). See [PreTrainedTokenizer.encode()](/docs/transformers/v5.22.2/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.encode) and [PreTrainedTokenizer.__call__()](/docs/transformers/v5.22.2/en/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__) for details.  [What are input IDs?](../glossary#input-ids)

pixel_values (`torch.FloatTensor` of shape `(batch_size, num_channels, image_size, image_size)`, *optional*) : The tensors corresponding to the input images. Pixel values can be obtained using [PixtralImageProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralImageProcessor). See [PixtralImageProcessor.__call__()](/docs/transformers/v5.22.2/en/model_doc/molmo2#transformers.Molmo2ImageProcessor.__call__) for details ([PixtralProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralProcessor) uses [PixtralImageProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralImageProcessor) for processing images).

attention_mask (`torch.Tensor` of shape `(batch_size, sequence_length)`, *optional*) : Mask to avoid performing attention on padding token indices. Mask values selected in `[0, 1]`:  - 1 for tokens that are **not masked**, - 0 for tokens that are **masked**.  [What are attention masks?](../glossary#attention-mask)

position_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*) : Indices of positions of each input sequence tokens in the position embeddings. Selected in the range `[0, config.n_positions - 1]`.  [What are position IDs?](../glossary#position-ids)

past_key_values (`~cache_utils.Cache`, *optional*) : Pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention blocks) that can be used to speed up sequential decoding. This typically consists in the `past_key_values` returned by the model at a previous stage of decoding, when `use_cache=True` or `config.use_cache=True`.  Only [Cache](/docs/transformers/v5.22.2/en/internal/generation_utils#transformers.Cache) instance is allowed as input, see our [kv cache guide](https://huggingface.co/docs/transformers/en/kv_cache). If no `past_key_values` are passed, [DynamicCache](/docs/transformers/v5.22.2/en/internal/generation_utils#transformers.DynamicCache) will be initialized by default.  The model will output the same cache format that is fed as input.  If `past_key_values` are used, the user is expected to input only unprocessed `input_ids` (those that don't have their past key value states given to this model) of shape `(batch_size, unprocessed_length)` instead of all `input_ids` of shape `(batch_size, sequence_length)`.

inputs_embeds (`torch.FloatTensor` of shape `(batch_size, sequence_length, hidden_size)`, *optional*) : Optionally, instead of passing `input_ids` you can choose to directly pass an embedded representation. This is useful if you want more control over how to convert `input_ids` indices into associated vectors than the model's internal embedding lookup matrix.

labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*) : Labels for computing the masked language modeling loss. Indices should either be in `[0, ..., config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

use_cache (`bool`, *optional*) : If set to `True`, `past_key_values` key value states are returned and can be used to speed up decoding (see `past_key_values`).

logits_to_keep (`Union[int, torch.Tensor]`, *optional*, defaults to `0`) : If an `int`, compute logits for the last `logits_to_keep` tokens. If `0`, calculate logits for all `input_ids` (special case). Only last token logits are needed for generation, and calculating them only for that token can save memory, which becomes pretty significant for long sequences or large vocabulary size. If a `torch.Tensor`, must be 1D corresponding to the indices to keep in the sequence length dimension. This is useful when using packed tensor format (single dimension for batch and sequence length).

image_sizes (`torch.Tensor` of shape `(batch_size, 2)`, *optional*) : The sizes of the images in the batch, being (height, width) for each image.

mm_encoder_outputs (`dict[str, ~modeling_outputs.BaseModelOutputWithPooling]`, *optional*) : Dict where keys are supported modalities and values are encoded outputs for that modality. Each encoded output is a tuple that consists of (`pooler_output`, *optional*: `last_hidden_states`, *optional*: `hidden_states`, *optional*: `attentions`) `pooler_output` of shape `(batch_size, sequence_length, hidden_size)`, *optional*) is a sequence of multimmodal features of the encoder merged into text embeddings.

**Returns:** `Mistral3CausalLMOutputWithPast` or `tuple(torch.FloatTensor)`

A `Mistral3CausalLMOutputWithPast` or a tuple of
`torch.FloatTensor` (if `return_dict=False` is passed or when `config.return_dict=False`) comprising various
elements depending on the configuration ([Mistral3Config](/docs/transformers/v5.22.2/en/model_doc/mistral3#transformers.Mistral3Config)) and inputs.

The [Mistral3ForConditionalGeneration](/docs/transformers/v5.22.2/en/model_doc/mistral3#transformers.Mistral3ForConditionalGeneration) forward method, overrides the `__call__` special method.

Although the recipe for forward pass needs to be defined within this function, one should call the `Module`
instance afterwards instead of this since the former takes care of running the pre and post processing steps while
the latter silently ignores them.

- **loss** (`torch.FloatTensor` of shape `(1,)`, *optional*, returned when `labels` is provided) -- Language modeling loss (for next-token prediction).
- **logits** (`torch.FloatTensor` of shape `(batch_size, sequence_length, config.vocab_size)`) -- Prediction scores of the language modeling head (scores for each vocabulary token before SoftMax).
- **past_key_values** (`Cache`, *optional*, returned when `use_cache=True` is passed or when `config.use_cache=True`) -- It is a [Cache](/docs/transformers/v5.22.2/en/internal/generation_utils#transformers.Cache) instance. For more details, see our [kv cache guide](https://huggingface.co/docs/transformers/en/kv_cache).

  Contains pre-computed hidden-states (key and values in the self-attention blocks) that can be used (see
  `past_key_values` input) to speed up sequential decoding.
- **hidden_states** (`tuple[torch.FloatTensor]`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +
  one for the output of each layer) of shape `(batch_size, sequence_length, hidden_size)`.

  Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.
- **attentions** (`tuple[torch.FloatTensor]`, *optional*, returned when `output_attentions=True` is passed or when `config.output_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch_size, num_heads, sequence_length,
  sequence_length)`.

  Attentions weights after the attention softmax, used to compute the weighted average in the self-attention
  heads.
- **image_hidden_states** (`torch.FloatTensor`, *optional*) -- A `torch.FloatTensor` of size `(batch_size, num_images, sequence_length, hidden_size)`.
  image_hidden_states of the model produced by the vision encoder and after projecting the last hidden state.

Example:

```python
>>> from PIL import Image
>>> from huggingface_hub.utils import httpx
>>> from io import BytesIO
>>> from transformers import AutoProcessor, Mistral3ForConditionalGeneration

>>> model = Mistral3ForConditionalGeneration.from_pretrained("mistralai/Mistral-Small-3.1-24B-Instruct-2503")
>>> processor = AutoProcessor.from_pretrained("mistralai/Mistral-Small-3.1-24B-Instruct-2503")

>>> prompt = "<s>[INST][IMG]What is the image?[/INST]"
>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"
>>> with httpx.stream("GET", url) as response:
...     image = Image.open(BytesIO(response.read()))

>>> inputs = processor(images=image, text=prompt, return_tensors="pt")

>>> # Generate
>>> generate_ids = model.generate(**inputs, max_new_tokens=15)
>>> processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
"What is the image?The image depicts two cats lying on a pink blanket."
```

#### get_image_features[[transformers.Mistral3ForConditionalGeneration.get_image_features]]

```python
get_image_features(pixel_values: FloatTensor, image_sizes: Tensor, vision_feature_layer: int | list[int] | None = None, **kwargs: *<class 'transformers.utils.generic.TransformersKwargs'>)
```

[Source](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/models/mistral3/modeling_mistral3.py#L349)

**Parameters:**

pixel_values (`torch.FloatTensor` of shape `(batch_size, num_channels, image_size, image_size)`) : The tensors corresponding to the input images. Pixel values can be obtained using [PixtralImageProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralImageProcessor). See [PixtralImageProcessor.__call__()](/docs/transformers/v5.22.2/en/model_doc/molmo2#transformers.Molmo2ImageProcessor.__call__) for details ([PixtralProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralProcessor) uses [PixtralImageProcessor](/docs/transformers/v5.22.2/en/model_doc/pixtral#transformers.PixtralImageProcessor) for processing images).

image_sizes (`torch.Tensor` of shape `(batch_size, 2)`) : The sizes of the images in the batch, being (height, width) for each image.

vision_feature_layer (`Union[int, list[int]]`, *optional*) : The index of the layer to select the vision feature. If multiple indices are provided, the vision feature of the corresponding indices will be concatenated to form the vision features.

**Returns:** [BaseModelOutputWithPooling](/docs/transformers/v5.22.2/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)`

A [BaseModelOutputWithPooling](/docs/transformers/v5.22.2/en/main_classes/output#transformers.modeling_outputs.BaseModelOutputWithPooling) or a tuple of
`torch.FloatTensor` (if `return_dict=False` is passed or when `config.return_dict=False`) comprising various
elements depending on the configuration ([Mistral3Config](/docs/transformers/v5.22.2/en/model_doc/mistral3#transformers.Mistral3Config)) and inputs.

- **last_hidden_state** (`torch.FloatTensor` of shape `(batch_size, sequence_length, hidden_size)`) -- Sequence of hidden-states at the output of the last layer of the model.
- **pooler_output** (`torch.FloatTensor` of shape `(batch_size, hidden_size)`) -- Last layer hidden-state of the first token of the sequence (classification token) after further processing
  through the layers used for the auxiliary pretraining task. E.g. for BERT-family of models, this returns
  the classification token after processing through a linear layer and a tanh activation function. The linear
  layer weights are trained from the next sentence prediction (classification) objective during pretraining.
- **hidden_states** (`tuple(torch.FloatTensor)`, *optional*, returned when `output_hidden_states=True` is passed or when `config.output_hidden_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +
  one for the output of each layer) of shape `(batch_size, sequence_length, hidden_size)`.

  Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.
- **attentions** (`tuple(torch.FloatTensor)`, *optional*, returned when `output_attentions=True` is passed or when `config.output_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch_size, num_heads, sequence_length,
  sequence_length)`.

  Attentions weights after the attention softmax, used to compute the weighted average in the self-attention
  heads.

Example:

```python
>>> from PIL import Image
>>> from transformers import AutoProcessor, Mistral3ForConditionalGeneration

>>> model = Mistral3ForConditionalGeneration.from_pretrained("mistralai/Mistral-Small-3.1-24B-Instruct-2503")
>>> processor = AutoProcessor.from_pretrained("mistralai/Mistral-Small-3.1-24B-Instruct-2503")

>>> messages = [
...     {
...         "role": "user", "content": [
...             {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"},
...             {"type": "text", "text": "Where is the cat standing?"},
...         ]
...     },
... ]

>>> inputs = processor.apply_chat_template(
...     messages,
...     tokenize=True,
...     return_dict=True,
...     return_tensors="pt",
...     add_generation_prompt=True
... )
>>> # Generate
>>> generate_ids = model.generate(**inputs)
>>> processor.batch_decode(generate_ids, skip_special_tokens=True)[0]
```

