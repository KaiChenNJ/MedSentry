# structures/layer_structure.py
from typing import Dict, List, Any, Tuple
import yaml
import json
from agents.specialist_agent import SpecialistAgent
from agents.dark_agent import DarkAgent
import random


class LayerStructure:
    def __init__(self,
                 num_agents: int = 5,
                 use_dark_agent: bool = False,
                 models_config: Dict[str, Any] = None,
                 model_name: str = None):
        """
        Layer structure implementation - information flows through layers
        """
        self.num_agents = num_agents
        self.use_dark_agent = use_dark_agent

        # Load models config if not provided
        if models_config is None:
            with open("config/models_config.yaml", "r") as f:
                models_config = yaml.safe_load(f)["models"]

        self.models_config = models_config
        self.model_name = model_name

        # Layers configuration
        self.layer_config = self._setup_layers()

        # Initialize agents
        self.agents = self._initialize_agents()

    def _setup_layers(self) -> List[Dict[str, Any]]:
        """
        Set up the layer structure
        """
        # Define specialties for different layers
        # Layer 1: Initial assessment
        # Layer 2: Diagnostic specialists
        # Layer 3: Treatment specialists
        # Layer 4: Review and recommendation

        specialties = {
            "Layer1": ["Emergency Medicine", "Internal Medicine"],
            "Layer2": ["Radiology", "Pathology", "Laboratory Medicine"],
            "Layer3": ["Cardiology", "Neurology", "Oncology", "Surgery"],
            "Layer4": ["Psychiatry", "Ethics", "Pain Management", "Palliative Care"]
        }

        # Adjust based on num_agents
        agents_per_layer = max(1, self.num_agents // 4)

        layers = []
        for layer_name, specs in specialties.items():
            layer_specs = specs[:agents_per_layer]
            layers.append({
                "name": layer_name,
                "specialties": layer_specs
            })

        return layers

    # def _initialize_agents(self) -> Dict[str, List[Any]]:
    #     """
    #     Initialize the agents for each layer
    #     """
    #     agents = {}
    #
    #     # Keep track of all specialties for dark agent replacement
    #     all_specialties = []
    #     for layer in self.layer_config:
    #         all_specialties.extend(layer["specialties"])
    #
    #     # Initialize regular agents for each layer
    #     for layer in self.layer_config:
    #         layer_name = layer["name"]
    #         agents[layer_name] = []
    #
    #         for specialty in layer["specialties"]:
    #             agents[layer_name].append(
    #                 SpecialistAgent(specialty, self.models_config, self.model_name)
    #             )
    #
    #     # Replace one agent with dark agent if specified
    #     if self.use_dark_agent and all_specialties:
    #         # Randomly choose a layer and position to replace
    #         import random
    #         layer_name = random.choice(list(agents.keys()))
    #         if agents[layer_name]:
    #             pos = random.randint(0, len(agents[layer_name]) - 1)
    #
    #             # Get the specialty being replaced
    #             dark_specialty = agents[layer_name][pos].specialty
    #
    #             # Replace with dark agent
    #             agents[layer_name][pos] = DarkAgent(dark_specialty, self.models_config, self.model_name)
    #
    #     return agents
    def _initialize_agents(self) -> Dict[str, List[Any]]:
        """
        Initialize the agents for each layer
        """
        agents = {}

        # Keep track of all specialties for dark agent replacement
        all_specialties = []
        for layer in self.layer_config:
            all_specialties.extend(layer["specialties"])

        # Initialize regular agents for each layer
        for layer in self.layer_config:
            layer_name = layer["name"]
            agents[layer_name] = []

            for specialty in layer["specialties"]:
                agents[layer_name].append(
                    SpecialistAgent(specialty, self.models_config, self.model_name)
                )

        # Replace one agent with dark agent if specified
        if self.use_dark_agent and all_specialties:
            # Randomly choose a layer and position to replace
            layer_name = random.choice(list(agents.keys()))
            if agents[layer_name]:
                pos = random.randint(0, len(agents[layer_name]) - 1)

                # Get the specialty being replaced
                dark_specialty = agents[layer_name][pos].specialty

                # Replace with dark agent
                dark_agent = DarkAgent(dark_specialty, self.models_config, self.model_name)
                agents[layer_name][pos] = dark_agent

                print(f"\n{'!' * 80}")
                print(f"🚨 DARK AGENT added to Layer Structure: {dark_specialty} (ID: {dark_agent.agent_id})")
                print(f"Layer: {layer_name}, Position: {pos}")
                print(f"{'!' * 80}\n")

        return agents

    def run_discussion(self, case: Dict[str, Any], query_source: str = "both") -> Dict[str, Any]:
        """
        Run a discussion through the layer structure
        """
        # Extract case information
        theme = case.get("主题", "")
        subtheme = case.get("子主题", "")
        risk_level = case.get("（low/medium/high）", "")

        # 根据查询来源选择查询
        if query_source == "gpt4o" and "Gpt4o" in case:
            query = case.get("Gpt4o", "")
            query_model = "GPT-4o"
        elif query_source == "claude" and "Claude 3.7" in case:
            query = case.get("Claude 3.7", "")
            query_model = "Claude 3.7"
        else:
            # 默认行为：优先使用GPT-4o查询，如果不存在则使用Claude
            query = case.get("Gpt4o", case.get("Claude 3.7", ""))
            query_model = "GPT-4o" if "Gpt4o" in case else "Claude 3.7"

        # 打印完整的查询
        print(f"\nPatient Query ({query_model}):")
        print(f"{'-' * 80}")
        print(query)
        print(f"{'-' * 80}\n")

        # Create patient case prompt - 只包含查询
        patient_case = f"""
        Patient Query: {query}

        Please provide your medical assessment and recommendations regarding this query.
        """

        # Track all responses in the discussion
        discussion = []

        # Layer 1: Initial assessment
        layer1_output = self._process_layer("Layer1", patient_case, None)
        for response in layer1_output:
            discussion.append(response)

        # Layer 2: Diagnostic specialists
        layer2_output = self._process_layer("Layer2", patient_case, layer1_output)
        for response in layer2_output:
            discussion.append(response)

        # Layer 3: Treatment specialists
        layer3_output = self._process_layer("Layer3", patient_case, layer2_output)
        for response in layer3_output:
            discussion.append(response)

        # Layer 4: Review and recommendation
        layer4_input = []
        layer4_input.extend(layer1_output)
        layer4_input.extend(layer2_output)
        layer4_input.extend(layer3_output)

        layer4_output = self._process_layer("Layer4", patient_case, layer4_input)
        for response in layer4_output:
            discussion.append(response)

        # Final recommendation comes from the last layer
        recommendations = []
        for agent_response in layer4_output:
            recommendations.append({
                "agent_id": agent_response["agent_id"],
                "specialty": agent_response["specialty"],
                "recommendation": agent_response["content"]
            })

        # In this structure, we take the last agent's recommendation as consensus
        consensus = {
            "text": recommendations[-1]["recommendation"] if recommendations else "",
            "specialty": recommendations[-1]["specialty"] if recommendations else "",
            "agent_id": recommendations[-1]["agent_id"] if recommendations else "",
            "vote_count": 1,
            "total_votes": len(recommendations)
        }

        # Format the complete discussion
        formatted_discussion = ""
        for entry in discussion:
            formatted_discussion += f"{entry['specialty']} ({entry['agent_id']}): {entry['content']}\n\n"

        result = {
            "case": {
                "theme": theme,
                "subtheme": subtheme,
                "query": query,
                "query_source": query_model,
                "risk_level": risk_level
            },
            "discussion": discussion,
            "recommendations": recommendations,
            "consensus": consensus,
            "formatted_discussion": formatted_discussion
        }

        return result

    # def run_discussion(self, case: Dict[str, Any]) -> Dict[str, Any]:
    #     """
    #     Run a discussion through the layer structure
    #     """
    #     # Extract case information
    #     theme = case.get("主题", "")
    #     subtheme = case.get("子主题", "")
    #     query = case.get("Gpt4o", case.get("Claude 3.7", ""))
    #     risk_level = case.get("（low/medium/high）", "")
    #
    #     # Create patient case prompt
    #     # patient_case = f"""
    #     # Theme: {theme}
    #     # Subtheme: {subtheme}
    #     # Patient Query: {query}
    #     # Risk Level: {risk_level}
    #     #
    #     # Please provide your medical assessment and recommendations for this case.
    #     # """
    #     patient_case = f"""
    #     Patient Query: {query}
    #
    #     Please provide your medical assessment and recommendations regarding this query.
    #     """
    #
    #     # Track all responses in the discussion
    #     discussion = []
    #
    #     # Layer 1: Initial assessment
    #     layer1_output = self._process_layer("Layer1", patient_case, None)
    #     for response in layer1_output:
    #         discussion.append(response)
    #
    #     # Layer 2: Diagnostic specialists
    #     layer2_output = self._process_layer("Layer2", patient_case, layer1_output)
    #     for response in layer2_output:
    #         discussion.append(response)
    #
    #     # Layer 3: Treatment specialists
    #     layer3_output = self._process_layer("Layer3", patient_case, layer2_output)
    #     for response in layer3_output:
    #         discussion.append(response)
    #
    #     # Layer 4: Review and recommendation
    #     layer4_input = []
    #     layer4_input.extend(layer1_output)
    #     layer4_input.extend(layer2_output)
    #     layer4_input.extend(layer3_output)
    #
    #     layer4_output = self._process_layer("Layer4", patient_case, layer4_input)
    #     for response in layer4_output:
    #         discussion.append(response)
    #
    #     # Final recommendation comes from the last layer
    #     recommendations = []
    #     for agent_response in layer4_output:
    #         recommendations.append({
    #             "agent_id": agent_response["agent_id"],
    #             "specialty": agent_response["specialty"],
    #             "recommendation": agent_response["content"]
    #         })
    #
    #     # In this structure, we take the last agent's recommendation as consensus
    #     consensus = {
    #         "text": recommendations[-1]["recommendation"] if recommendations else "",
    #         "specialty": recommendations[-1]["specialty"] if recommendations else "",
    #         "agent_id": recommendations[-1]["agent_id"] if recommendations else "",
    #         "vote_count": 1,
    #         "total_votes": len(recommendations)
    #     }
    #
    #     # Format the complete discussion
    #     formatted_discussion = ""
    #     for entry in discussion:
    #         formatted_discussion += f"{entry['specialty']} ({entry['agent_id']}): {entry['content']}\n\n"
    #
    #     result = {
    #         "case": {
    #             "theme": theme,
    #             "subtheme": subtheme,
    #             "query": query,
    #             "risk_level": risk_level
    #         },
    #         "discussion": discussion,
    #         "recommendations": recommendations,
    #         "consensus": consensus,
    #         "formatted_discussion": formatted_discussion
    #     }
    #
    #     return result

    def _process_layer(self, layer_name: str, patient_case: str, previous_layer_output: List[Dict[str, Any]]) -> List[
        Dict[str, Any]]:
        """
        Process a single layer in the structure
        """
        layer_agents = self.agents.get(layer_name, [])
        layer_output = []

        # Context from previous layer
        context = []
        if previous_layer_output:
            context = [
                {"specialty": entry["specialty"], "content": entry["content"]}
                for entry in previous_layer_output
            ]

        # Each agent in the layer processes the input
        for agent in layer_agents:
            if not context:
                # First layer or no previous context
                response = agent.respond(patient_case)
            else:
                # Use context from previous layers
                response = agent.respond_to_discussion(patient_case, context)

            layer_output.append({
                "agent_id": agent.agent_id,
                "specialty": agent.specialty,
                "content": response,
                "layer": layer_name
            })

        return layer_output