# utils/shared_memory.py
from typing import Dict, List, Any
import datetime


class SharedMemory:
    def __init__(self):
        """
        Shared memory for agents to exchange information
        """
        self.memory = []

    def add_entry(self, agent_id: str, specialty: str, content: str) -> None:
        """
        Add an entry to the shared memory
        """
        self.memory.append({
            "agent_id": agent_id,
            "specialty": specialty,
            "content": content,
            "timestamp": self._get_timestamp()
        })

    def get_all_entries(self) -> List[Dict[str, Any]]:
        """
        Get all entries in the shared memory
        """
        return self.memory

    def get_latest_entries(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the latest n entries
        """
        return self.memory[-n:] if len(self.memory) >= n else self.memory

    def get_entries_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get all entries by a specific agent
        """
        return [entry for entry in self.memory if entry["agent_id"] == agent_id]

    def clear(self) -> None:
        """
        Clear the memory
        """
        self.memory = []

    def _get_timestamp(self) -> str:
        """
        Get the current timestamp
        """
        return datetime.datetime.now().isoformat()

    def get_formatted_discussion(self) -> str:
        """
        Get the discussion in a formatted string
        """
        formatted = ""
        for entry in self.memory:
            formatted += f"{entry['specialty']} ({entry['agent_id']}): {entry['content']}\n\n"
        return formatted