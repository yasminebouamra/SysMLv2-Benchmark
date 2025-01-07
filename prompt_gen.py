import litellm
from utilities import read_files

def run_model_generation(model, messages):
    '''
    Run chosen model usin LiteLLM library.
    :param model: model name, has to be ollama/name for local models
    :param messages: list of messages to be passed to the model, should be a dictionnary with {role: str, content: str}
    :return: text response from the model
    '''
    response = litellm.completion(model, messages)
    return response["choices"][0]["message"]["content"]

def generate_model_explanation(model, code):
    '''
    Generates an explanation for a SysMLV2 model.
    :param model: model name, has to be ollama/name for local models
    :param code: SysMLV2 code
    :return: textual explanation of the code
    '''
    template_prompt_explanation[1]["content"] = code
    return run_model_generation(model, template_prompt_explanation)

def prompt_generation(model, code):
    '''
    Generates a prompt for a SysMLV2 model.
    :param model: model name, has to be ollama/name for local models
    :param code: SysMLV2 code
    :return: prompt for the model
    '''
    template_prompt_gen[1]["content"] = f"Code : {code}\nExplanation : {generate_model_explanation(model, code)}"
    return run_model_generation(model, template_prompt_gen)


template_prompt_explanation = [
    {
        "role" : "system",
        "content" : "You are a SysMLV2 Engineer. You are given a code in SysMLV2 and you are asked to explain it in a concise and simple way."
    },
    {
        "role" : "user",
        "content" : ""
    }
]

template_prompt_gen = [
    {
        "role" : "system",
        "content" : "You are a SysMLV2 Engineer. You are given a code and its explanation. Generate a prompt that can be used to generate the code. The prompt should be a short explanation of the model and shouldn't have any instruction. Your output should be the prompt only."
    },
    {
        "role" : "user",
        "content" : ""
    }
]

files = read_files("data/examples")

for file in files:
    with open(file):
        # output path is prompts/<file_name>.txt
        output_path = f"prompts/{file.split("/")[-1].replace(".sysml", ".txt")}"
        
        with open(output_path, "w") as f:
            print(prompt_generation("openai/gpt-4-turbo", open(file).read()))
