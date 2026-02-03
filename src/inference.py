"""
ClinExplain AI - MedGemma Inference Module

This module handles inference via OpenRouter API.
Replaces previous local transformer implementation.
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass

from .config import get_inference_config
from .prompts import build_extraction_prompt, build_simplification_prompt

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Data Structures
# ------------------------------------------------------------------

@dataclass
class InferenceResult:
    """Result of model inference"""
    success: bool
    output: Optional[str]
    error: Optional[str]
    metadata: Dict[str, Any]

# ------------------------------------------------------------------
# Main Engine
# ------------------------------------------------------------------

class MedGemmaInference:
    """
    Wrapper for OpenRouter API inference.
    
    Handles API calls, errors, and mock fallback.
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        device: str = "auto",
        use_mock: bool = False
    ):
        """
        Initialize inference engine.
        """
        self.use_mock = use_mock
        self.model_name = "openai/gpt-4.1-mini"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.inference_config = get_inference_config()

        logger.info(f"Initializing Inference Engine | Requested Mock: {self.use_mock}")

        if not self.use_mock:
            if not self.api_key:
                logger.warning("CRITICAL: OPENROUTER_API_KEY missing -> Falling back to MOCK mode")
                self.use_mock = True
            else:
                logger.info("OpenRouter API Key found. Ready for real inference.")

    # ------------------------------------------------------------------

    def extract_findings(
        self,
        report_text: str,
        include_examples: bool = False
    ) -> InferenceResult:

        logger.info("Extracting findings from report")

        prompt = build_extraction_prompt(report_text, include_examples)
        return self._run_inference(prompt, task="extraction")

    # ------------------------------------------------------------------

    def simplify_findings(
        self,
        structured_findings: Dict[str, Any]
    ) -> InferenceResult:

        logger.info("Generating patient-friendly summary")

        prompt = build_simplification_prompt(structured_findings)
        return self._run_inference(prompt, task="simplification")

    # ------------------------------------------------------------------

    def _run_inference(
        self,
        prompt: str,
        task: str = "extraction",
        max_retries: int = 2
    ) -> InferenceResult:

        if self.use_mock:
            logger.info(f"MODE: MOCK | Task: {task}")
            return self._mock_inference(prompt, task)

        logger.info(f"MODE: REAL | Model: {self.model_name}")

        try:
            output_text = self.call_openrouter(prompt)
            
            return InferenceResult(
                success=True,
                output=output_text,
                error=None,
                metadata={
                    "task": task,
                    "model": self.model_name
                }
            )

        except Exception as e:
            logger.error(f"OpenRouter inference failed: {str(e)}")
            logger.warning("Falling back to mock inference due to error")
            return self._mock_inference(prompt, task)

    # ------------------------------------------------------------------

    def call_openrouter(self, prompt: str) -> str:
        """
        Call OpenRouter Chat Completions API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a medical report analysis assistant that outputs strict JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 600
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    # ------------------------------------------------------------------

    def _mock_inference(self, prompt: str, task: str) -> InferenceResult:

        logger.info(f"Using mock inference for task: {task}")

        if task == "extraction":
            mock_output = json.dumps({
                "findings": [
                    {
                        "text": "Heart appears mildly enlarged",
                        "source_quote": "mild cardiomegaly",
                        "confidence": "high",
                        "category": "observation"
                    },
                    {
                        "text": "Lungs appear clear with no signs of infection",
                        "source_quote": "Lungs are clear bilaterally",
                        "confidence": "high",
                        "category": "normal"
                    }
                ],
                "attention_flags": [
                    {
                        "flag": "Mild heart enlargement noted",
                        "severity": "info",
                        "context": "May require clinical correlation",
                        "source_quote": "mild cardiomegaly"
                    }
                ],
                "terminology": [
                    {
                        "medical_term": "cardiomegaly",
                        "simple_explanation": "Enlargement of the heart",
                        "confidence": "high"
                    }
                ],
                "uncertainties": []
            }, indent=2)

        elif task == "simplification":
            mock_output = json.dumps({
                "summary":
                    "The report shows your heart looks slightly larger than normal. "
                    "Your lungs appear clear. Your doctor can explain what this means for you.",
                "key_points": [
                    "Heart mildly enlarged",
                    "Lungs normal",
                    "Doctor will guide next steps"
                ],
                "next_steps_note":
                    "Discuss these findings with your healthcare provider."
            }, indent=2)

        else:
            mock_output = json.dumps({"error": "Unknown task"})

        return InferenceResult(
            success=True,
            output=mock_output,
            error=None,
            metadata={
                "task": task,
                "mock": True,
                "prompt_length": len(prompt),
                "output_length": len(mock_output)
            }
        )

# ------------------------------------------------------------------
# Factory
# ------------------------------------------------------------------

def create_inference_engine(
    model_path: Optional[str] = None,
    use_mock: bool = False
) -> MedGemmaInference:

    return MedGemmaInference(
        model_path=model_path,
        use_mock=use_mock
    )
