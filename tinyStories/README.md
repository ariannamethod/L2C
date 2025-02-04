# TinyStories 110M parameters

1. Get hugging face model

    ```bash
    git clone https://huggingface.co/nickypro/tinyllama-110M
    ```

1. Exporting the file

    ```bash
    mkdir tinyStories;

    #normal
    .venv/bin/python3.11 export.py tinyStories/tinyStories-110M.bin --hf /path/to/tinyllama-110M;

    #quantized
    .venv/bin/python3.11 export.py tinyStories/tinyStories-110M_q80.bin --version 2 --hf /path/to/tinyllama-110M;

    ```

1. Run inference

    ```bash
    # make the run and runq files
    make;

    ./run "tinyStories/tinyStories-110M.bin" -z "./tokenizer.bin" -t 0.8 -n 50 -i "Where is Burj Khalifa?";

    ./runq "tinyStories-110M_q80.bin" -z "./tokenizer.bin" -t 0.8 -n 50 -i "Where is Burj Khalifa?";
    ```
