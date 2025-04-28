# agents/base_agent.py
from typing import Dict, List, Any, Optional
import uuid
from utils.llm_interface import LLMInterface


# class BaseAgent:
#     def __init__(self,
#                  specialty: str,
#                  models_config: Dict[str, Any],
#                  model_name: str = None,
#                  agent_id: str = None,
#                  system_prompt: str = None):
#         """
#         Base agent class for medical specialists
#         """
#         self.specialty = specialty
#         self.agent_id = agent_id or str(uuid.uuid4())[:8]
#         self.history = []
#         self.llm = LLMInterface(models_config, model_name)
#
#         # Default system prompt if none provided
#         self.system_prompt = system_prompt or self._default_system_prompt()
#
#     def _default_system_prompt(self) -> str:
#         """
#         Default system prompt for medical specialist agents
#         """
#         return f"""
#         You are a medical specialist in {self.specialty}.
#         You are participating in a multidisciplinary team discussion about a patient case.
#         Provide your professional medical opinion based on your expertise.
#         Follow medical ethics principles and prioritize patient safety and wellbeing.
#         Your responses should be evidence-based and considerate of patient dignity.
#         """
#
#     def respond(self, patient_info: str, context: Optional[List[Dict[str, str]]] = None) -> str:
#         """
#         Generate a response based on patient information and context
#         """
#         prompt = f"""
#         Patient Case Information:
#         {patient_info}
#
#         Based on your expertise in {self.specialty}, please provide your assessment and recommendations.
#         """
#
#         response = self.llm.generate(self.system_prompt, prompt, self.history)
#
#         # Update history
#         self.history.append({"role": "user", "content": prompt})
#         self.history.append({"role": "assistant", "content": response})
#
#         return response
#
#     def respond_to_discussion(self, patient_info: str, discussion_context: List[Dict[str, str]]) -> str:
#         """
#         Respond in a discussion context
#         """
#         prompt = f"""
#         Patient Case Information:
#         {patient_info}
#
#         Previous Discussion:
#         {self._format_discussion(discussion_context)}
#
#         Based on your expertise in {self.specialty} and considering the discussion so far,
#         please provide your assessment and recommendations.
#         """
#
#         response = self.llm.generate(self.system_prompt, prompt, self.history)
#
#         # Update history
#         self.history.append({"role": "user", "content": prompt})
#         self.history.append({"role": "assistant", "content": response})
#
#         return response
#
#     def _format_discussion(self, discussion_context: List[Dict[str, str]]) -> str:
#         """
#         Format the discussion context for the prompt
#         """
#         formatted = ""
#         for item in discussion_context:
#             specialist = item.get("specialty", "Unknown Specialist")
#             content = item.get("content", "")
#             formatted += f"{specialist}: {content}\n\n"
#
#         return formatted

from typing import Dict, List, Any, Optional
import uuid
from utils.llm_interface import LLMInterface


class BaseAgent:
    def __init__(self,
                 specialty: str,
                 models_config: Dict[str, Any],
                 model_name: str = None,
                 agent_id: str = None,
                 system_prompt: str = None):
        """
        Base agent class for medical specialists
        """
        self.specialty = specialty
        self.agent_id = agent_id or str(uuid.uuid4())[:8]
        self.history = []
        self.llm = LLMInterface(models_config, model_name)

        # Default system prompt if none provided
        self.system_prompt = system_prompt or self._default_system_prompt()

    def _default_system_prompt(self) -> str:
        """
        Default system prompt for medical specialist agents
        """
        return f"""
        You are a medical specialist in {self.specialty}. 
        You are participating in a multidisciplinary team discussion about a patient case.
        Provide your professional medical opinion based on your expertise.
        Follow medical ethics principles and prioritize patient safety and wellbeing.
        Your responses should be evidence-based and considerate of patient dignity.
        """

    # def respond(self, patient_info: str, context: Optional[List[Dict[str, str]]] = None) -> str:
    #     """
    #     Generate a response based on patient information and context
    #     """
    #     prompt = f"""
    #     Patient Case Information:
    #     {patient_info}
    #
    #     Based on your expertise in {self.specialty}, please provide your assessment and recommendations.
    #     """
    #
    #     print(f"\n{'=' * 80}")
    #     print(f"Agent: {self.specialty} (ID: {self.agent_id}) is thinking...")
    #     print(f"Prompt: {prompt[:150]}...")
    #
    #     response = self.llm.generate(self.system_prompt, prompt, self.history)
    #
    #     print(f"\nResponse from {self.specialty} (ID: {self.agent_id}):")
    #     print(f"{'-' * 80}")
    #     print(response)
    #     print(f"{'-' * 80}")
    #
    #     # Update history
    #     self.history.append({"role": "user", "content": prompt})
    #     self.history.append({"role": "assistant", "content": response})
    #
    #     return response
    def respond(self, patient_info: str, context: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate a response based on patient information and context
        """
        prompt = f"""
        Patient Case Information:
        {patient_info}

        Based on your expertise in {self.specialty}, please provide your assessment and recommendations.
        """

        print(f"\n{'=' * 80}")
        print(f"Agent: {self.specialty} (ID: {self.agent_id}) is thinking...")
        # 不截断提示词，只打印一个简化版本
        print(f"Responding to patient query...")

        response = self.llm.generate(self.system_prompt, prompt, self.history)

        print(f"\nResponse from {self.specialty} (ID: {self.agent_id}):")
        print(f"{'-' * 80}")
        print(response)
        print(f"{'-' * 80}")

        # Update history
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": response})

        return response

    def respond_to_discussion(self, patient_info: str, discussion_context: List[Dict[str, str]]) -> str:
        """
        Respond in a discussion context
        """
        prompt = f"""
        Patient Case Information:
        {patient_info}

        Previous Discussion:
        {self._format_discussion(discussion_context)}

        Based on your expertise in {self.specialty} and considering the discussion so far, 
        please provide your assessment and recommendations.
        """

        print(f"\n{'=' * 80}")
        print(f"Agent: {self.specialty} (ID: {self.agent_id}) is responding to discussion...")
        print(f"Prompt: {prompt[:150]}...")

        response = self.llm.generate(self.system_prompt, prompt, self.history)

        print(f"\nResponse from {self.specialty} (ID: {self.agent_id}):")
        print(f"{'-' * 80}")
        print(response)
        print(f"{'-' * 80}")

        # Update history
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": response})

        return response

    def _format_discussion(self, discussion_context: List[Dict[str, str]]) -> str:
        """
        Format the discussion context for the prompt
        """
        formatted = ""
        for item in discussion_context:
            specialist = item.get("specialty", "Unknown Specialist")
            content = item.get("content", "")
            formatted += f"{specialist}: {content}\n\n"

        return formatted

    def get_token_usage(self) -> Dict[str, int]:
        """
        Get token usage statistics from the LLM interface
        """
        return self.llm.get_token_usage()