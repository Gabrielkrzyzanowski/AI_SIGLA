# Report on T01 - Setup Ollama + GPU Offloading + GPU Benchmark

## Ollama download and setup 
Ollama is a lightweight, open-source tool that allows you to easily run, manage, and interact with highly optimized, open-source large language models locally on your own machine. 

To install it, run the following command on your terminial:
``` bash
curl -fsSL https://ollama.com/install.sh | sh 
```

Ollama supports a diverse library of open-source models, including **Llama**, **DeepSeek**, and **Qwen**. For this project, we selected Google DeepMind's **Gemma** family. As noted in the Ollama documentation: *"Gemma 4 models are multimodal, handling text and image input and generating text output"*.

---

We deployed the following specific model tags to test different quantization levels:
- gemma4:e4b-it-qat 
- gemma4:e4b-it-q4_K_M 
- gemma4:e4b-it-q8_0 

> The "e" in "e4b" stands for *Effective Parameters* meaning it has an effective size of 4 Billion parameters (8 Billion with embeddings). The "it" parameter stands for *Instruction Tuned*, meaning that the model is fine-tuned to follow conversational instructions and prompts. The final sufix dictates the specific quantization format: "qat" — Quantization-Aware Training; "q4_K_M" — 4-bit, K-Quant, Medium size; "q8_0" — 8-bit, Block-wise Uniform Quantization.

To install the models the following command must be run:
``` bash 
ollama pull gemma4:e4b-it-qat 
ollama pull gemma4:e4b-it-q4_K_M 
ollama pull gemma4:e4b-it-q8_0
``` 

## Running the model locally 

To execute a model locally and initiate an interactive terminal session, use the base command  `ollama run <model_name>`. For benchmarking, profiling hardware performance, and logging system metrics, appending the `--verbose` flag is preferred.

**Example Input:**
``` bash
ollama run gemma4:e4b-it-qat "Explain neuron communication process in one paragraph"  --verbose
```
**Example Output:** 
```text 
Neuron communication is a complex electrochemical process that occurs primarily at specialized junctions called synapses, allowing signals to pass from one neuron to another. The process begins (...).

total duration:       19.110849351s
load duration:        9.097135249s
prompt eval count:    23 token(s)
prompt eval duration: 241.078ms
prompt eval rate:     95.40 tokens/s
eval count:           599 token(s)
eval duration:        9.768874s
eval rate:            61.32 tokens/s
```

## Benchmarking and Reports

The first layer of benchmark is done by understanding the verbose metrics. When evaluating local deployment efficiency, the output metadata details system perfomance accros two critical phases: `prompt eval rate` indicates how fast the system reads and understand the prompt before it begins its answer; and `eval rate` represents the true generation speed. 


``` bash 
nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.used,temperature.gpu --format=csv -lms 100 -f gpu_report.csv
```  


``` bash 
journalctl -u ollama --no-pager -n 200 > ollama_load_report2.txt
```  

