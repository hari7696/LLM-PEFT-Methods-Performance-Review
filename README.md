# LLM-PEFT-Performance-Review

In this study, I aimed to evaluate the complexity of customizing LLM Models.

First thing I met is the ICL(in-context learning). It’s the technique where you provide some examples to the model with every user prompt. so that model can infer the example and tries to replicate the same for the given prompt as well. 
Its sounds like a great option. But you are wasting your invaluable context length, smaller models usually have context length of 512, with ICL examples, you wasting nearly half of the context length. Also, you might not have sufficient space for RAG information to include. Apart from all this, computing costs and response times are higher for this method.

Keeping in mind that ICL isn’t suitable for all scenarios, I explored further.

I stumbled upon Andrews NGs LLM course which provided lots of insights into PEFT models, RL Methods and LLM deployments. The course gave me inspiration to do this evaluation

I further explored the Customization methods, focusing on instruction finetuning and PEFT(Parameter efficient fine-tuning methods).

For all the methods I chose 'google/flan-t5-base' as my base model. Models are tuned on 12460 training samples and evaluated 1500 sample hold out dataset.
I was able to tune all models, under $10 on Google Colab Enterprise.

### Instruction finetuning:
* Generally, this approach is compute expensive and prone to catastrophic forgetting
* Works best for single task or few task use cases.
* I performed instruction tuning using a dialog sum dataset("knkarthick/dialogsum")
* I tuned the model for 6 epochs on Google colab enterprise (g2-standard-4). I started with recommend small learning rate 1e5. ( Its 1.1 hours, surprisingly low)
* Ideally, it should be able to provide far better results than what I have achieved. I wasn’t able to fine tune due to compute budget restrictions

### Low-Rank Adaptation (LoRA) - a PEFT Method.
* It operates by decomposing a large matrix into smaller lower rank matrices in the attention layers.
* [100,000 * 100,000] -> [100,000  * 1] ,  [1 * 100,000]
* Basically, a 10k million parameters are reduced to 200k parameters. The lower rank matrices are multiplied and added to original matrix. Thus, we are training only <0.1 of the models parameters
* I don’t exactly know where to start with learning rate( mixed opinions on internet, most say start with higher 1e3), so I used a non-parametric optimizer Prodigy.
* Trained it with 3 epochs and got amazing result of 18.38% absolute difference(rougeLsum) compared to original model
* Training time : 32 minutes

### Infused Adapter by Inhibiting and Amplifying Inner Activations ( IA3) - a PEFT Method
* It operates by rescaling the inner activations with learned vectors( thus further reducing the number trainable parameters than Lora)
* Same prodigy optimizer used in this method as well.
* Trained it with 3 epochs and got absolute difference of 13.41 absolute difference(rougeLsum) compared to original model. Although its less then Lora, it’s still good.
* Training time : 32 minutes.


### Results

The models’ completions are saved on the "models_evaluaiton.csv" file and trained models are saved in hugging face repos. The evaluation is made on test data which contains 1500 prompts
| Model           | ROUGE-1   | ROUGE-2   | ROUGE-L   | ROUGE-Lsum |
|-----------------|-----------|-----------|-----------|------------|
| Original Model  | 0.1936    | 0.0558    | 0.1653    | 0.1655     |
| Instruct Model*  | 0.2094    | 0.0729    | 0.1836    | 0.1840     |
| PEFT IA3 Model  | 0.3751    | 0.1414    | 0.2998    | 0.2996     |
| PEFT LoRa Model | 0.4341    | 0.1779    | 0.3494    | 0.3493     |

* Don’t mind the Instruct model scores, the scores would be higher than LoRa and IA3 if its finetuned well. The reason I included that score is to showcase, the difficulty of instruction tuning.
* I haven’t experimented with inference settings like random sampling, top-k, top-n, temperature. I observed some lack of creativity in some of PEFT models answers. Furhter evaluation needed by adjusting the inference settings.




