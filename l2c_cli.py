import argparse
import logging

import l2c
from session_logger import SESSION_ID, log_turn

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="L2C command line interface")
    parser.add_argument("--prompt", help="generate text from prompt")
    parser.add_argument("--dream", action="store_true", help="run dream loop")
    parser.add_argument("--health", action="store_true", help="print health metrics")
    parser.add_argument("--train", metavar="FILE", help="train on dataset")
    parser.add_argument("--tokens", metavar="FILE", help="tokenize file")
    args = parser.parse_args()

    print(f"L2C | New session started: {SESSION_ID}")

    if args.prompt is not None:
        response = l2c.generate(args.prompt)
        print(response)
        log_turn(args.prompt, response)
    elif args.dream:
        l2c.dream_loop()
    elif args.health:
        metrics = l2c.health()
        for k, v in metrics.items():
            print(f"{k}: {v}")
    elif args.train:
        l2c.train(args.train)
    elif args.tokens:
        tokens = l2c.tokenize_file(args.tokens)
        print(tokens)
    else:
        parser.print_help()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
