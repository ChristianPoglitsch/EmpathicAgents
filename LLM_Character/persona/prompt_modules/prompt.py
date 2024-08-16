import sys
sys.path.append('../../')

def generate_prompt(prompt_input:list[str], prompt_path_file:str): 
  if type(prompt_input) == type("string"): 
    curr_input = [prompt_input]
  curr_input = [str(i) for i in prompt_input]

  f = open(prompt_path_file,"r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):   
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt: 
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()


if __name__ == "__main__":
    pass
