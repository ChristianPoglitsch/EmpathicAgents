﻿from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, BitsAndBytesConfig, TextIteratorStreamer
from trl.trainer.utils import PeftSavingCallback
from peft import prepare_model_for_kbit_training
from peft import LoraConfig, get_peft_model, PeftModel
from peft.tuners.lora import LoraLayer
from datasets import load_dataset
from threading import Thread
import gradio as gr
import transformers
import torch
import os
from datasets import load_dataset

#!pip install accelerate==0.21.0 bitsandbytes==0.41.0 datasets==2.14.2 einops==0.6.1 gradio==3.37.0 peft==0.4.0 protobuf==4.23.4 scipy==1.11.1 sentencepiece==0.1.99 transformers==4.31.0 trl==0.5.0> /dev/null 2>&1

#Current versions
#transformers==4.38.2 accelerate==0.28.0
#https://github.com/TimDettmers/bitsandbytes/issues/822
#pip install https://github.com/jllllll/bitsandbytes-windows-webui/releases/download/wheels/bitsandbytes-0.41.1-py3-none-win_amd64.whl


def generate_text(prompt, model, tokenizer, generation_config):
    inputs = tokenizer(prompt, return_tensors="pt")['input_ids']
    output_tokens = model.generate(
        input_ids=inputs.to(model.device),
        generation_config=generation_config,
        max_new_tokens=30,
    )
    output_text = tokenizer.decode(output_tokens.squeeze(), skip_special_tokens=True)
    return output_text


def get_formatted_prompt(prompt):
    return f"### Human: {prompt} ### Assistant:"


def RundModel(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id, padding_side="right", use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(model_id,
                                                 load_in_4bit=True, # Lade Modell 4-Bit quantisiert
                                                 torch_dtype=torch.bfloat16, # Verwende BFloat16-Datentyp für Berechnungen
                                                 device_map="auto" # Weise Modellgewichtungen automatisch zu: GPU > CPU > Festplatte
                                                 )

    torch.manual_seed(1337)

    generation_config = GenerationConfig(
        temperature=0.1, # Diversität des generierten Texts (<1 sorgt für eher deterministische Ergebnisse, während >1 die Kreativität und Zufälligkeit erhöht)
        top_k=40, # Wähle den nächsten Token aus den 40 wahrscheinlichsten nächsten Token
        top_p=0.75, # Wähle den nächsten Ausgabe-Token aus einer Teilmenge aller wahrscheinlichsten nächsten Token aus, wobei die kumulative Wahrscheinlichkeit der Teilmenge größer als 0.75 ist. Da top_k ebenfalls definiert ist enthält die Teilmenge maximal 40 Token.
    )


    prompt = "Frage: Wie viele Bundesländer hat Deutschland? Antwort:"
    generated_text = generate_text(prompt, model, tokenizer, generation_config)
    print(generated_text)

    prompt = "Ich habe extreme Schmerzen im unteren Rücken."
    formatted_prompt = get_formatted_prompt(prompt)

    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(inputs=inputs.input_ids, max_new_tokens=60)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))


def TrainModel(model_id, trained_path):

    tokenizer = AutoTokenizer.from_pretrained(model_id, padding_side="right", use_fast=False)

    def preprocess_function(sample):
        MAX_SEQUENCE_LENGTH = 512
        preprocessed_prompt = ""

        # Jeder Turn besteht aus menschlicher Anweisung und Antwort vom Assistenten
        turn_delimiter = "### Human:"
        turns = [turn_delimiter + turn for turn in sample['text'].split(turn_delimiter) if turn]
        for turn in turns:
            # Verarbeite Turn nur wenn Antwort vom Assistenten ebenfalls enthalten ist
            if "### Assistant:" in turn:
                # Jeder Turn beginnt mit einem Satzbeginn- und endet mit einem Satzende-Token
                preprocessed_prompt += tokenizer.bos_token + turn + tokenizer.eos_token
        result = tokenizer(preprocessed_prompt, max_length=MAX_SEQUENCE_LENGTH, truncation=True, add_special_tokens=False)

        result["labels"] = result["input_ids"].copy()
        return result

    # Datensatz vorverarbeiten
    dataset = load_dataset("thisserand/health_care_german", split="train") # "../../../f/Development/LLM/thisserand/health_care_german"
    dataset = dataset.map(preprocess_function, remove_columns=["text"])

    # ---
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True, # Modell wird 4-Bit quantisiert geladen
        bnb_4bit_use_double_quant=True, # Quantisiuerungskonstanten werden ebenfalls quantisiert (reduziert Speicherbedarf)
        bnb_4bit_quant_type="nf4", # spezifischer Datentyp 'nf4' wird als 4-Bit Datentyp verwendet (optimal für normalverteilte Modellgewichtungen)
        bnb_4bit_compute_dtype=torch.bfloat16 # Datentyp 'bfloat16' wird für Berechnungen verwendet. Hierfür werden 4-Bit Modellgewichtungen bzw. Teile der Gewichtungen zur Laufzeit zu BFloat16 dequantisiert sodass Matrizenmultiplikation mit 16-bit Genauigkeit durchgeführt werden können
    )

    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto", torch_dtype=torch.bfloat16)
    model.config.torch_dtype = torch.bfloat16

    # Modell für QLoRA Fine-Tuning vorbereiten
    model = prepare_model_for_kbit_training(model)

    # Low Rank Adapter (LoRA) konfigurieren
    lora_config = LoraConfig(
        r=64, # Rang der Matrixfaktorisierungen
        lora_alpha=16, # LoRA Skalierungsfaktor
        target_modules=['_proj'], # Schichten in denen Adapter hinzugefügt werden
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )

    # Adapter zum Modell hinzufügen
    model = get_peft_model(model, lora_config)

    # Hinzugefügte Adapter zu Datentyp BFloat16 konvertieren
    for name, module in model.named_modules():
        if isinstance(module, LoraLayer):
            module = module.to(torch.bfloat16)
        if 'norm' in name:
            # Normierung benötigt wenige Parameter, höhere Genauigkeit der Normierung sorgt für stabileres Fine-Tuning
            module = module.to(torch.float32)
        if 'lm_head' in name or 'embed_tokens' in name:
            if hasattr(module, 'weight'):
                if module.weight.dtype == torch.float32:
                    module = module.to(torch.bfloat16)


    # ---
    training_arguments = transformers.TrainingArguments(
            per_device_train_batch_size=1, # Batchgröße je GPU
            gradient_accumulation_steps=16, # Gradienten werden über zwei Batches (2*16=32) akkumuliert und Low-Rank-Adapter werden erst dann aktualisiert (nicht per Batch); Methode um Speicher-effizient die Batchgröße zu vergößern
            max_steps=1875, # maximale Anzahl an Trainingsiterationen (pro Iteration werden Modellgewichtungen optimiert) -- 1875
            learning_rate=2e-4, # Lernrate (2e-4 liefert gute Ergebnisse für 7B-LLMs)
            warmup_ratio=0.03, # Anzahl Iterationen in denen tatsächliche Lernrate linear von 0 zu definierter Lernrate erhöht wird (stabilisiert Trainingsprozess)
            lr_scheduler_type = "constant", # Nachdem Warmup-Phase abgeschlossen ist bleibt die Lernrate konstant
            bf16=True, # sorgt für 16-Bit (anstatt 32-Bit) Fine-Tuning, betrifft zu optimierende Low-Rank Adapter sowie die zur Optimierung benötigten Gradienten
            logging_steps=10, # Interval in dem Trainingsfortschritt geloggt wird
            output_dir="outputs", # Ausgabeordner in dem die Low Rank Adapter gespeichert werden
            optim="paged_adamw_32bit", # Zu verwendender Optimizer (aktualisiert/optimiert Modellgewichtungen während des Fine-Tunings) -- paged_adamw_32bit
            gradient_checkpointing=True, # Verringert Speicherbedarf und vermeidet OOM-Errors, macht das Training jedoch langsamer
            max_grad_norm = 0.3, # Vermeidet das Gradienten während des Trainings zu groß werden (dient der Stabilisierung des Trainings)
    )

    training_arguments.max_steps = 200
    training_arguments.output_dir = trained_path
    training_arguments.optim = "paged_adamw_8bit"

    # code updates 22.3.2024
    tokenizer.pad_token = '0'   

    trainer = transformers.Trainer(
                model=model,
                args=training_arguments,
                data_collator=transformers.DataCollatorForSeq2Seq(tokenizer, pad_to_multiple_of=8, return_tensors="pt"),
                train_dataset=dataset,
                tokenizer=tokenizer,
                callbacks=[PeftSavingCallback]
            )

    # Deaktivieren des Caches verringert Speicherverbrauch. Sollte bei Inferenz jedoch wieder aktiviert werden, da es für schnellere Textgenerierung sorgt
    model.config.use_cache = False

    trainer.train()

    # Speichern der gefinetuneten Low Rank Adapter
    trainer.save_model()


def load_base_model(model_id):
    return AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type='nf4'
        )
    )

def get_formatted_prompt(prompt):
    return f"### Human: {prompt} ### Assistant:"


def RunTrainedModel(model_id, trained_path):

    adapters_id = trained_path
    base_model = load_base_model(model_id)
    model = PeftModel.from_pretrained(base_model, adapters_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id, padding_side="right", use_fast=False)

    prompt = "Ich habe extreme Schmerzen im unteren Rücken."
    formatted_prompt = get_formatted_prompt(prompt)

    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(inputs=inputs.input_ids, max_new_tokens=300)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))


#path = os.getcwd() 
## Extracting all the contents in the directory corresponding to path
#l_files = os.listdir(path) 
#print(l_files)

model_id = "openlm-research/open_llama_7b_v2"
# TODO: Change path
trained_path = "C:\\Development/LLM_Character/trained/thisserand/outputs_health_care"

#RundModel(model_id)
#TrainModel(model_id, trained_path)
RunTrainedModel(model_id, trained_path)