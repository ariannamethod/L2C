# TinyLlama/TinyLlama-1.1B-intermediate-step-480k-1T

1. Git Clone:

    ```bash
    # git clone
    git clone https://huggingface.co/TinyLlama/TinyLlama-1.1B-intermediate-step-480k-1T

    ## OR

    # hugging face download
    huggingface-cli download TinyLlama/TinyLlama-1.1B-intermediate-step-480k-1T --local-dir ./ --include original/*

    ```

1. Exporting the file

    ```bash
    cd llama2.c

    mkdir TinyLlama

    # model export
    .venv/bin/python3.11 export.py TinyLlama/TinyLlama-1.1B-intermediate-step-480k-1T.bin --hf /path/to/TinyLlama-1.1B-intermediate-step-480k-1T

    # quantize model export
    .venv/bin/python3.11 export.py TinyLlama/TinyLlama-1.1B-intermediate-step-480k-1T_q80.bin --version 2 --hf /path/to/TinyLlama-1.1B-intermediate-step-480k-1T

    ```

1. Running inference:

    ```bash
    ./run "TinyLlama/TinyLlama-1.1B-intermediate-step-480k-1T.bin" -z "./tokenizer.bin" -t 0.8 -n 50 -i "Where is Burj Khalifa?"

    ./runq "TinyLlama/TinyLlama-1.1B-intermediate-step-480k-1T_q80.bin" -z "./tokenizer.bin" -t 0.8 -n 50 -i "Where is Burj Khalifa?"
    ```
