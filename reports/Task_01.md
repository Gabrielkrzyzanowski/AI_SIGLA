# Report on T01 - Setup Ollama + GPU Offloading + GPU Benchmark

## Ollama download and setup 
Ollama is a lightweight, open-source tool that allows you to easily run, manage, and interact with highly optimized, open-source large language models locally on your own machine. 

To install it, run the following command on your terminal:
``` bash
curl -fsSL https://ollama.com/install.sh | sh 
```

Ollama supports a diverse library of open-source models, including **Llama**, **DeepSeek**, and **Qwen**. For this task, we selected Google DeepMind's **Gemma** family. As noted in the Ollama documentation: *"Gemma 4 models are multimodal, handling text and image input and generating text output"*.

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

## Running models locally 

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

The first layer of benchmarking is achieved by analyzing verbose metrics. When evaluating local deployment efficiency, the output metadata details system perfomance accros two critical phases: 
- `prompt eval rate` indicates how fast the system reads and understand the prompt before it begins its answer; and
- `eval rate` represents the true generation speed. 

To monitor and manage hardware metrics, such as GPU temperature, power draw, memory usage, and compute utilization, developers can use the `nvidia-smi` utility. The following command recods these perfomance metrics directly into a CSV file for long-term analysis:

``` bash 
nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.used,temperature.gpu --format=csv -lms 100 -f gpu_report.csv
```  

Further optimization can be achieved by verifying layer offloading and VRAM allocation. To determine how many layers of the model are residing in the GPU versus being spilled over to system RAM, one must peek at the Ollama server logs. On WSL Ubuntu, this is managed via `journalctl`, a component of Linux's **systemd** ecosystem used for querying system logs. The following command filters only logs from ollama unit and exports the most recent 200 lines to a text file:
``` bash 
journalctl -u ollama --no-pager -n 200 > ollama_load_report2.txt
```  

The expected output provides critical architectural telemetry, including GPU offload counts, model specifications, and the initialization performance baseline.

**Example Output:** 
```text 
(...)
load_tensors: offloading output layer to GPU
load_tensors: offloading 41 repeating layers to GPU
load_tensors: offloaded 43/43 layers to GPU
load_tensors: CPU_Mapped model buffer size =  2730.00 MiB
load_tensors: CUDA0 model buffer size =  2696.06 MiB 
(...)
slot print_timing: id  0 | task 335 | prompt eval time =     396.54 ms /    23 tokens (   17.24 ms per token,    58.00 tokens per second)
slot print_timing: id  0 | task 335 |        eval time =    6254.97 ms /   389 tokens (   16.08 ms per token,    62.19 tokens per second)
slot print_timing: id  0 | task 335 |       total time =    6651.52 ms /   412 tokens
```

## Example on Collecting Metrics 

To see a practical example of a benchmarking report let us analyse the performance of a given model changing quantization parameters. That is going to be achieved by calling the models previously installed (*gemma4:e4b-it-qa*, *gemma4:e4b-it-q4_K_M* and *gemma4:e4b-it-q8_0*) with the same task. 

**Task Input:**
``` bash
ollama run <model> "Explain Landau-de Gennes Theory of Phase transition in one paragraph"  --verbose
``` 

### Report  

* **Layers Offloaded:** The number of neural network layers compiled directly into GPU VRAM versus those handled by system RAM/CPU fallback.
* **Prompt Eval Rate (TTFT):** Time to First Token. Measures how quickly the model processes the initial prompt context before starting text generation.
* **Eval Rate (Generation Speed):** The performance threshold during sustained token generation. 

| Model Variant | Layers Offloaded | Prompt Eval Rate (TTFT) | Eval Rate (Gen Speed) | Max GPU Util | Max VRAM Util | Max GPU Temp |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`gemma4:e4b-it-qa`** | 43 / 43 | 126.45 tokens/s | 61.72 tokens/s | 88% | 90% | 66°C |
| **`gemma4:e4b-it-q4_K_M`** | 43 / 43 | 2.23 tokens/s | 59.85 tokens/s | 87% | 90% | 66°C |
| **`gemma4:e4b-it-q8_0`** | 41 / 43 | 5.84 tokens/s | 32.36 tokens/s | 76% | 80% | 63°C |

### Raw Log Data

#### gemma4:e4b-it-qa

**Verbose Output:**
``` text
total duration:       22.517333998s
load duration:        8.982784225s
prompt eval count:    29 token(s)
prompt eval duration: 229.336ms
prompt eval rate:     126.45 tokens/s
eval count:           821 token(s)
eval duration:        13.301345s
eval rate:            61.72 tokens/s
```

**nvidia-smi Output:**
``` text
max utilization.gpu [%]: 88%
max utilization.memory [%]: 90% 
max temperature.gpu [°C]: 66
``` 

**Journalctl Output:**
``` text
model type            = E4B
model params          = 7.46 B

load_tensors: offloaded 43/43 layers to GPU

prompt eval time =     229.34 ms /    29 tokens (    7.91 ms per token,   126.45 tokens per second)
eval time =   13301.34 ms /   821 tokens (   16.20 ms per token,    61.72 tokens per second)
total time =   13530.68 ms /   850 tokens
```  

#### gemma4:e4b-it-q4_K_M

**Verbose Output:**
``` text
total duration:       29.604861272s
load duration:        10.52344364s
prompt eval count:    29 token(s)
prompt eval duration: 12.996894s
prompt eval rate:     2.23 tokens/s
eval count:           364 token(s)
eval duration:        6.081823s
eval rate:            59.85 tokens/s
```

**nvidia-smi Output:**
``` text
max utilization.gpu [%]: 87%
max utilization.memory [%]: 90% 
max temperature.gpu [°C]: 66
``` 

**Journalctl Output:**
``` text
model type            = E4B
model params          = 7.52 B

load_tensors: offloaded 43/43 layers to GPU

prompt eval time =   12996.89 ms /    29 tokens (  448.17 ms per token,     2.23 tokens per second)
eval time =    6081.82 ms /   364 tokens (   16.71 ms per token,    59.85 tokens per second)
total time =   19078.72 ms /   393 tokens
```  

#### gemma4:e4b-it-q8_0

**Verbose Output:**
``` text
total duration:       35.397247552s
load duration:        18.497802714s
prompt eval count:    29 token(s)
prompt eval duration: 4.966982s
prompt eval rate:     5.84 tokens/s
eval count:           386 token(s)
eval duration:        11.929411s
eval rate:            32.36 tokens/s
```

**nvidia-smi Output:**
``` text
max utilization.gpu [%]: 76%
max utilization.memory [%]: 80% 
max temperature.gpu [°C]: 63
``` 

**Journalctl Output:**
``` text
model type            = E4B
model params          = 7.52 B

load_tensors: offloaded 41/43 layers to GPU

prompt eval time =   4966.98 ms /    29 tokens (  171.28 ms per token,     5.84 tokens per second)
eval time =    11929.41 ms /   386 tokens (   30.91 ms per token,    32.36 tokens per second)
total time =   16896.39 ms /   415 tokens
``` 

