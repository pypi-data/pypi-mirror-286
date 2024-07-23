"""Deploy a Llama model as an LLM service for text generation and streaming."""

import shutil

import covalent_cloud as cc

cc.save_api_key("your-api-key")

CB_ENV = "llama-chatbot@blueprints"

volume = cc.volume("llama-chatbot")

cc.create_env(
    name=CB_ENV,
    pip=[
        "accelerate",
        "sentencepiece",
        "transformers",
        "covalent-cloud>=0.71.0rc0",
        "covalent-blueprints>=0.0.2rc8",
    ],
    wait=True
)

gpu_executor = cc.CloudExecutor(
    env=CB_ENV,
    num_cpus=8,
    num_gpus=1,
    gpu_type=cc.cloud_executor.GPU_TYPE.V100,
    memory="15 GB",
    time_limit="3 hours",
    volume_id=volume.id,
)


@cc.service(executor=gpu_executor, name="LLM Chatbot Server")
def chatbot_backend(
    model_name,
    device_map="auto",
    torch_dtype="float16",
    use_saved_model=True,
    save_model_to_volume=True,
):
    """Backend service for a Llama-like chatbot.

    Args:
        model_path: Hugging Face model name, e.g. "NousResearch/
            Llama-2-7b-chat-hf".
        device_map: PyTorch device map for model sub-modules. Defaults
            to "auto".
        torch_dtype: PyTorch data type (as string) for model
            parameters. Defaults to "float16".
        use_saved_model: Load the saved model from the cloud volume,
            if available. Defaults to True.
        save_model_to_volume: Save the pretrained model to the cloud
            volume, overwriting if a copy already exists. Defaults to
            True.
    """

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

    saved_model_name = str(model_name).replace("/", "--")
    saved_model_path = volume / saved_model_name
    local_model_path = f"/tmp/{saved_model_path.name}"

    if use_saved_model and saved_model_path.exists():
        print("💿 Loading saved model from", saved_model_path)
        shutil.copytree(saved_model_path, local_model_path)
        model_name = local_model_path

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map=device_map,
        torch_dtype=getattr(torch, torch_dtype),
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if not saved_model_path.exists() or save_model_to_volume:
        shutil.rmtree(saved_model_path, ignore_errors=True)
        print("💾 Saving model to", saved_model_path)
        model.save_pretrained(local_model_path)
        tokenizer.save_pretrained(local_model_path)
        shutil.copytree(local_model_path, saved_model_path)

    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer)

    return {"pipe": pipe}


@chatbot_backend.endpoint("/generate", name="Generate Response")
def generate(
    pipe=None,
    *,
    prompt=None,
    max_new_tokens=200,
    truncation=True,
    temperature=0.9,
):
    """Generate a response to a prompt.

    Kwargs:
        prompt: The prompt to generate a response to.
        max_new_tokens: Maximum number of new tokens to generate.
            Defaults to 200.
        truncation: Whether to truncate the generated text. Defaults to
            True.
        temperature: The temperature for sampling. Defaults to 0.9.

    Returns:
        The generated text.
    """

    if prompt is None:
        return "Please provide a prompt."

    output = pipe(
        prompt,
        max_new_tokens=max_new_tokens,
        truncation=truncation,
        temperature=temperature,
    )
    return output[0]['generated_text']


@chatbot_backend.endpoint("/stream", name="Stream Response", streaming=True)
def generate_stream(
    pipe=None,
    *,
    prompt=None,
    max_new_tokens=200,
    temperature=0.9,
):
    """Generate and stream a response to a prompt.

    Kwargs:
        prompt: The prompt to generate a response to.
        max_new_tokens: Maximum number of new tokens to generate.
            Defaults to 200.
        temperature: The temperature for sampling. Defaults to 0.9.

    Yields:
        Tokens of the generated text.
    """

    if prompt is None:
        yield "Please provide a prompt."

    else:
        import torch

        def _starts_with_space(tokenizer, token_id):
            token = tokenizer.convert_ids_to_tokens(token_id)
            return token.startswith('▁')

        model = pipe.model
        tokenizer = pipe.tokenizer
        _input = tokenizer(prompt, return_tensors='pt').to("cuda")

        for output_length in range(max_new_tokens):
            # Generate next token
            output = model.generate(
                **_input,
                max_new_tokens=1,
                temperature=temperature,
                pad_token_id=tokenizer.eos_token_id
            )
            # Check for stopping condition
            current_token_id = output[0][-1]
            if current_token_id == tokenizer.eos_token_id:
                break
            # Decode token
            current_token = tokenizer.decode(
                current_token_id, skip_special_tokens=True
            )
            if _starts_with_space(tokenizer, current_token_id.item()) and output_length > 1:
                current_token = ' ' + current_token

            yield current_token

            # Update input for next iteration.
            # Output grows in size with each iteration.
            _input = {
                'input_ids': output.to("cuda"),
                'attention_mask': torch.ones(1, len(output[0])).to("cuda"),
            }


info = cc.deploy(chatbot_backend, volume=volume)(
    model_name="NousResearch/Llama-2-7b-chat-hf"
)
info = cc.get_deployment(info.function_id, wait=True)
