# agents/specialist_agent.py
from typing import Dict, List, Any, Optional
from agents.base_agent import BaseAgent


class SpecialistAgent(BaseAgent):
    def __init__(self,
                 specialty: str,
                 models_config: Dict[str, Any],
                 model_name: str = None,
                 agent_id: str = None):
        """
        Specialist agent representing a medical expert in a specific field
        """
        super().__init__(specialty, models_config, model_name, agent_id)
        self.system_prompt = self._specialist_system_prompt()

    def _specialist_system_prompt(self) -> str:
        """
        System prompt specific to medical specialists
        """
        return f"""
        You are a medical specialist in {self.specialty} participating in a multidisciplinary team discussion.

        You should follow these medical ethics principles:
        1. Provide competent medical advice with compassion and respect for human dignity and rights
        2. Uphold standards of professionalism and honesty in all interactions
        3. Respect the law while recognizing responsibility to prioritize patient interests
        4. Respect patient rights, confidentiality, and privacy
        5. Base your recommendations on the latest scientific knowledge
        6. Exercise professional judgment, especially in urgent situations
        7. Consider public health implications of recommendations
        8. Always prioritize patient wellbeing above all else
        9. Support access to medical care for all people

        Provide clear, evidence-based opinions from your specialty's perspective. 
        Acknowledge limitations in your knowledge when appropriate.
        Collaborate respectfully with other specialists to reach the best patient outcome.
        """