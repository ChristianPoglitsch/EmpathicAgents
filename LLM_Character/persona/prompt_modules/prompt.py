import sys
sys.path.append('../../')

def generate_prompt(prompt_input:list[str], prompt_path_file:str): 
  """
  Takes in the prompt input and the path to a prompt template file. 
  The template file contains the raw str prompt that
  will be used, which contains the following substr: 
  !<INPUT>!

  This function replaces this substr with the actual input to produce the 
  final promopt. 
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the prompt template file. 
  RETURNS: 
    A filled in prompt.  
  """
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
