import asyncio
import sys
from app.core.logging import logger
from evals.evaluator import Evaluator


async def run_evaluation():
    """
    CLI Command to kick off the evaluation process.
    Usage: python -m evals.main
    """

    print("Starting AI Evaluation...")

    try:
        evaluator = Evaluator()
        await evaluator.run()
        print("✅ Evaluation completed successfully.")
    except Exception as e:
        logger.error("Evaluation failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_evaluation())
