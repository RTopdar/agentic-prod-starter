import asyncio
import openai
from langfuse import Langfuse
from langfuse.api import TraceWithDetails
from tqdm import tqdm

from app.core.config import settings
from app.core.logging import logger
from evals.metrics import metrics
from evals.schemas import ScoreSchema
from evals.helpers import get_input_output


class Evaluator:
    """
    Automated Judge that grades AI interactions.
    Fetches real-world traces and applies LLM-based metrics.
    """

    def __init__(self):
        self.client = openai.AsyncOpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
        )
        self.langfuse = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
        )

    async def run(self):
        """
        Main execution loop.
        """
        # 1. Fetch recent production traces
        traces = self.__fetch_traces()
        logger.info(f"Found {len(traces)} traces to evaluate")
        for trace in tqdm(traces, desc="Evaluating traces"):
            # Extract the user input and agent output from the trace
            input_text, output_text = get_input_output(trace)

            # 2. Run every defined metric against this trace
            for metric in metrics:
                score = await self._run_metric_evaluation(
                    metric, input_text, output_text
                )
                if score:
                    # 3. Upload the grade back to Langfuse
                    self._push_to_langfuse(trace, score, metric)

    async def _run_metric_evaluation(
        self, metric: dict, input_str: str, output_str: str
    ) -> ScoreSchema | None:
        """
        Uses an LLM as a Judge to grade the conversation.
        """
        try:
            response = await self.client.beta.chat.completions.parse(
                model=settings.openrouter_model,
                messages=[
                    {"role": "system", "content": metric["prompt"]},
                    {
                        "role": "user",
                        "content": f"Input: {input_str}\nGeneration: {output_str}",
                    },
                ],
                response_format=ScoreSchema,
            )
            return response.choices[0].message.parsed
        except Exception as e:
            logger.error(f"Metric {metric['name']} failed", error=str(e))
            return None

    def _push_to_langfuse(
        self, trace: TraceWithDetails, score: ScoreSchema, metric: dict
    ):
        """
        Persist the score. This allows us to build charts like:
        "Hallucination rate over the last 30 days".
        """
        self.langfuse.create_score(
            trace_id=trace.id,
            name=metric["name"],
            value=score.score,
            comment=score.reasoning,
        )

    def __fetch_traces(self) -> list[TraceWithDetails]:
        """Fetch traces from the last 24h that haven't been scored yet."""
        return []
