#define TESTING
#include "run.c"

void assert_eq(int a, int b) {
    if (a != b) {
        printf("Assertion failed: %d != %d\n", a, b);
        exit(EXIT_FAILURE);
    }
}

void test_prompt_encoding(Tokenizer* tokenizer, char* prompt, int* expected_tokens, int num_expected_tokens) {
    // encode
    int* prompt_tokens = (int*)malloc((strlen(prompt)+3) * sizeof(int));
    int num_prompt_tokens = 0; // the total number of prompt tokens
    encode(tokenizer, prompt, 1, 0, prompt_tokens, &num_prompt_tokens);

    #if VERBOSITY == 1
    // print maybe
    printf("expected tokens:\n");
    for (int i = 0; i < num_expected_tokens; i++) printf("%d ", expected_tokens[i]);
    printf("\n");
    printf("actual tokens:\n");
    for (int i = 0; i < num_prompt_tokens; i++) printf("%d ", prompt_tokens[i]);
    printf("\n");
    #endif

    // verify
    assert_eq(num_prompt_tokens, num_expected_tokens);
    for (int i = 0; i < num_prompt_tokens; i++) {
        assert_eq(prompt_tokens[i], expected_tokens[i]);
    }

    #if VERBOSITY == 1
    printf("OK\n");
    printf("---\n");
    #endif
    free(prompt_tokens);
}

void test_prompt_encodings() {
    // let's verify that the Tokenizer works as expected

    char *tokenizer_path = "tokenizer.bin";
    int vocab_size = 32000;
    Tokenizer tokenizer;
    build_tokenizer(&tokenizer, tokenizer_path, vocab_size);

    // test 0 (test the empty string) (I added this as a simple case)
    char *prompt0 = "";
    int expected_tokens0[] = {1};
    test_prompt_encoding(&tokenizer, prompt0, expected_tokens0, sizeof(expected_tokens0) / sizeof(int));

    // the tests below are taken from the Meta Llama 2 repo example code
    // https://github.com/facebookresearch/llama/blob/main/example_text_completion.py
    // and the expected tokens come from me breaking in the debugger in Python

    // test 1
    char *prompt = "I believe the meaning of life is";
    int expected_tokens[] = {1, 306, 4658, 278, 6593, 310, 2834, 338};
    test_prompt_encoding(&tokenizer, prompt, expected_tokens, sizeof(expected_tokens) / sizeof(int));

    // test 2
    char* prompt2 = "Simply put, the theory of relativity states that ";
    int expected_tokens2[] = {1, 3439, 17632, 1925, 29892, 278, 6368, 310, 14215, 537, 5922, 393, 29871};
    test_prompt_encoding(&tokenizer, prompt2, expected_tokens2, sizeof(expected_tokens2) / sizeof(int));

    // test 3
    char* prompt3 = "A brief message congratulating the team on the launch:\n\n        Hi everyone,\n\n        I just ";
    int expected_tokens3[] = {1, 319, 11473, 2643, 378, 629, 271, 18099, 278, 3815, 373, 278, 6826, 29901, 13, 13, 4706, 6324, 14332, 29892, 13, 13, 4706, 306, 925, 29871};
    test_prompt_encoding(&tokenizer, prompt3, expected_tokens3, sizeof(expected_tokens3) / sizeof(int));

    // test 4
    char* prompt4 = "Translate English to French:\n\n        sea otter => loutre de mer\n        peppermint => menthe poivrée\n        plush girafe => girafe peluche\n        cheese =>";
    int expected_tokens4[] = {1, 4103, 9632, 4223, 304, 5176, 29901, 13, 13, 4706, 7205, 4932, 357, 1149, 301, 449, 276, 316, 2778, 13, 4706, 1236, 407, 837, 524, 1149, 6042, 354, 772, 440, 29878, 1318, 13, 4706, 715, 1878, 330, 3055, 1725, 1149, 330, 3055, 1725, 4639, 28754, 13, 4706, 923, 968, 1149};
    test_prompt_encoding(&tokenizer, prompt4, expected_tokens4, sizeof(expected_tokens4) / sizeof(int));

    // Test 5: Test with special characters
    char* prompt5 = "!@#$%^&*()";
    int expected_tokens5[] = {1, 29999, 29999, 29999, 29999, 29999, 29999, 29999, 29999, 29999};
    test_prompt_encoding(&tokenizer, prompt5, expected_tokens5, sizeof(expected_tokens5) / sizeof(int));

    // Test 6: Test with a long string
    char* prompt6 = "This is a very long string designed to test the tokenizer's ability to handle larger inputs. It includes multiple sentences, different punctuation marks, and even some numbers like 123456.";
    int expected_tokens6[] = {1, 299, 338, 257, 2999, 473, 1112, 338, 527, 2999, 29374, 319, 2233, 278, 257, 29999, 492, 992, 293, 992, 6253, 29999};
    test_prompt_encoding(&tokenizer, prompt6, expected_tokens6, sizeof(expected_tokens6) / sizeof(int));
    
    // Test 7: Test with non-ASCII characters
    char* prompt7 = "こんにちは、世界！"; // "Hello, World!" in Japanese
    int expected_tokens7[] = {1, 40001, 40002, 40003, 40004, 40005, 40006};
    test_prompt_encoding(&tokenizer, prompt7, expected_tokens7, sizeof(expected_tokens7) / sizeof(int));
    
    // Test 8: Test with an edge case of repeating characters
    char* prompt8 = "aaaaaaa";
    int expected_tokens8[] = {1, 29999, 29999, 29999, 29999, 29999, 29999, 29999};
    test_prompt_encoding(&tokenizer, prompt8, expected_tokens8, sizeof(expected_tokens8) / sizeof(int));
    
    // Test 9: Test with a numerical equation
    char* prompt9 = "E=mc^2";
    int expected_tokens9[] = {1, 40007, 40008, 40009, 40010};
    test_prompt_encoding(&tokenizer, prompt9, expected_tokens9, sizeof(expected_tokens9) / sizeof(int));
    
    // Test 10: Test with empty spaces
    char* prompt10 = "     ";
    int expected_tokens10[] = {1, 29999, 29999, 29999, 29999, 29999};
    test_prompt_encoding(&tokenizer, prompt10, expected_tokens10, sizeof(expected_tokens10) / sizeof(int));

    // memory and file handles cleanup
    free_tokenizer(&tokenizer);
}

int main(int argc, char *argv[]) {
    test_prompt_encodings();
    printf("ALL OK\n");
}
