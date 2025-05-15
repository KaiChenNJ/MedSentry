# structures/shared_pool_voting.py
from typing import Dict, List, Any, Tuple
import yaml
import json
import os
from agents.specialist_agent import SpecialistAgent
from agents.dark_agent import DarkAgent
from utils.shared_memory import SharedMemory
import random


class SharedPoolVotingSystem:
    def __init__(self,
                 num_agents: int = 5,
                 use_dark_agent: bool = False,
                 models_config: Dict[str, Any] = None,
                 model_name: str = None):
        """
        Shared pool voting system implementation
        """
        self.num_agents = num_agents
        self.use_dark_agent = use_dark_agent

        # Load models config if not provided
        if models_config is None:
            with open("config/models_config.yaml", "r") as f:
                models_config = yaml.safe_load(f)["models"]

        self.models_config = models_config
        self.model_name = model_name

        # Specialties for the medical team
        self.specialties = [
            "Cardiology",
            "Neurology",
            "Oncology",
            "Psychiatry",
            "Emergency Medicine",
            "Internal Medicine",
            "Radiology",
            "Surgery",
            "Pediatrics",
            "Geriatrics"
        ]

        # Initialize agents
        self.agents = self._initialize_agents()

        # Initialize shared memory
        self.shared_memory = SharedMemory()


    def _initialize_agents(self) -> List[Any]:
        """
        Initialize the agents for the discussion
        """
        agents = []
        selected_specialties = self.specialties[:self.num_agents]

        # If using dark agent, replace one regular agent with a dark agent
        if self.use_dark_agent and self.num_agents > 0:
            # Randomly select a specialty for the dark agent
            dark_specialty_index = random.randint(0, len(selected_specialties) - 1)
            dark_specialty = selected_specialties.pop(dark_specialty_index)

            # Create regular agents
            for specialty in selected_specialties:
                agents.append(SpecialistAgent(specialty, self.models_config, self.model_name))

            # Add dark agent
            dark_agent = DarkAgent(dark_specialty, self.models_config, self.model_name)
            agents.append(dark_agent)

            print(f"\n{'!' * 80}")
            print(f"🚨 DARK AGENT added to Shared Pool: {dark_specialty} (ID: {dark_agent.agent_id})")
            print(f"{'!' * 80}\n")
        else:
            # Create all regular agents
            for specialty in selected_specialties:
                agents.append(SpecialistAgent(specialty, self.models_config, self.model_name))

        return agents

    def run_discussion(self, case: Dict[str, Any], query_source: str = "both", max_rounds: int = 3) -> Dict[str, Any]:
        """
        Run a discussion among the agents
        """
        # Clear the shared memory for new discussion
        self.shared_memory.clear()

        # Extract case information
        theme = case.get("Topic", "")
        subtheme = case.get("Subtopic", "")
        risk_level = case.get("（low/medium/high）", "")

        if query_source == "gpt4o" and "Gpt4o" in case:
            query = case.get("Gpt4o", "")
            query_model = "GPT-4o"
        elif query_source == "claude" and "Claude 3.7" in case:
            query = case.get("Claude 3.7", "")
            query_model = "Claude 3.7"
        else:

            query = case.get("Gpt4o", case.get("Claude 3.7", ""))
            query_model = "GPT-4o" if "Gpt4o" in case else "Claude 3.7"

        print(f"\nPatient Query ({query_model}):")
        print(f"{'-' * 80}")
        print(query)
        print(f"{'-' * 80}\n")

        # Create patient case prompt -
        patient_case = f"""
        Patient Query: {query}

        Please provide your medical assessment and recommendations regarding this query.
        """

        # Initial round: each agent responds to the case
        for agent in self.agents:
            response = agent.respond(patient_case)
            self.shared_memory.add_entry(agent.agent_id, agent.specialty, response)

        # Discussion rounds
        for round_num in range(max_rounds - 1):
            for agent in self.agents:
                # Get all entries for context
                discussion_context = [
                    {"specialty": entry["specialty"], "content": entry["content"]}
                    for entry in self.shared_memory.get_all_entries()
                ]

                # Agent responds to the ongoing discussion
                response = agent.respond_to_discussion(patient_case, discussion_context)
                self.shared_memory.add_entry(agent.agent_id, agent.specialty, response)

        # Voting round
        recommendations = []
        for agent in self.agents:
            # Final recommendation
            discussion_context = [
                {"specialty": entry["specialty"], "content": entry["content"]}
                for entry in self.shared_memory.get_all_entries()
            ]

            prompt = f"""
            Patient Case Information:
            {patient_case}

            Previous Discussion:
            {self.shared_memory.get_formatted_discussion()}

            Based on the entire discussion, provide your FINAL recommendation for this case.
            Format your response as:
            RECOMMENDATION: [Your concise recommendation]
            RATIONALE: [Brief explanation]
            """

            response = agent.llm.generate(agent.system_prompt, prompt, agent.history)
            recommendations.append({
                "agent_id": agent.agent_id,
                "specialty": agent.specialty,
                "recommendation": response
            })

        # Find consensus through simple voting mechanism
        consensus = self._find_consensus(recommendations)

        # Format the complete discussion
        result = {
            "case": {
                "theme": theme,
                "subtheme": subtheme,
                "query": query,
                "query_source": query_model,
                "risk_level": risk_level
            },
            "discussion": self.shared_memory.get_all_entries(),
            "recommendations": recommendations,
            "consensus": consensus,
            "formatted_discussion": self.shared_memory.get_formatted_discussion()
        }

        return result



    def _find_consensus(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Find consensus through simple voting
        """
        # In a real system, this would implement semantic similarity or clustering
        # For this simplified version, just return the majority specialty's recommendation

        # Extract main recommendations
        main_recs = []
        for rec in recommendations:
            # Extract main recommendation part
            content = rec["recommendation"]
            if "RECOMMENDATION:" in content:
                parts = content.split("RECOMMENDATION:")[1].split("RATIONALE:")
                if len(parts) > 0:
                    main_recs.append(parts[0].strip())
            else:
                # If no formatting, just use the first 100 chars
                main_recs.append(content[:100].strip())

        # Count occurrences of similar recommendations (simplified)
        from collections import Counter
        counts = Counter(main_recs)
        most_common = counts.most_common(1)

        if most_common:
            consensus_rec = most_common[0][0]
            # Find the full recommendation that matches this
            for rec in recommendations:
                if consensus_rec in rec["recommendation"]:
                    return {
                        "text": rec["recommendation"],
                        "specialty": rec["specialty"],
                        "agent_id": rec["agent_id"],
                        "vote_count": most_common[0][1],
                        "total_votes": len(recommendations)
                    }

        # Fallback - return the first recommendation
        return {
            "text": recommendations[0]["recommendation"],
            "specialty": recommendations[0]["specialty"],
            "agent_id": recommendations[0]["agent_id"],
            "vote_count": 1,
            "total_votes": len(recommendations)
        }