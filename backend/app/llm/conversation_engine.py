from collections import defaultdict

from backend.app.llm.llm_interface import LLMInterface
from backend.app.llm.memory_extractor import MemoryExtractor
from backend.app.models.memory import Memory
from backend.app.memory.behavioral_profile_builder import (
    build_behavioral_profile,
)


class ConversationEngine:
    """
    Coordinates conversation between the user,
    memory system, and LLM provider.

    Pipeline:

        User message
              ↓
        Memory extraction
              ↓
        Multiple memory processing
              ↓
        Memory retrieval
              ↓
        Behavioral profile retrieval
              ↓
        Context construction
              ↓
        LLM response
    """

    def __init__(
        self,
        llm: LLMInterface,
        memory_manager,
    ):
        self.llm = llm
        self.memory_manager = memory_manager

        self.memory_extractor = MemoryExtractor(
            llm=llm
        )

    def respond(
        self,
        user_id: str,
        message: str,
    ) -> str:

        # =====================================================
        # STEP 1 : EXTRACT POSSIBLE NEW MEMORIES
        # =====================================================

        extraction = self.memory_extractor.extract(
            message
        )

        print(
            "\nMEMORY EXTRACTION:"
        )

        print(
            extraction
        )

        # =====================================================
        # STEP 2 : PROCESS NEW MEMORIES
        # =====================================================

        if extraction["should_remember"]:

            memories = extraction.get(
                "memories",
                []
            )

            for extracted_memory in memories:

                content = extracted_memory.get(
                    "memory"
                )

                memory_type = extracted_memory.get(
                    "memory_type",
                    "fact",
                )

                if not content:
                    continue

                new_memory = Memory(
                    user_id=user_id,
                    content=content,
                    memory_type=memory_type,
                )

                print(
                    f"New memory detected: "
                    f"{new_memory.content}"
                )

                self.memory_manager.process_memory(
                    new_memory
                )

        else:

            print(
                "No durable memory detected."
            )

        # =====================================================
        # STEP 3 : RETRIEVE RELEVANT MEMORIES
        # =====================================================

        memories = (
            self.memory_manager
            .retrieve_relevant_memories(
                user_id=user_id,
                query=message,
            )
        )

        print(
            "\nRETRIEVED MEMORIES:"
        )

        for memory in memories:

            print(
                f"- {memory.content}"
            )

        # =====================================================
        # STEP 4 : BUILD MEMORY CONTEXT
        # =====================================================

        context = self._build_context(
            memories
        )

        print(
            "\nMEMORY CONTEXT:"
        )

        print(
            context
        )

        # =====================================================
        # STEP 5 : BUILD BEHAVIORAL PROFILE CONTEXT
        # =====================================================

        behavioral_context = (
            self._build_behavioral_context(
                user_id
            )
        )

        print(
            "\nBEHAVIORAL PROFILE:"
        )

        print(
            behavioral_context
        )

        # =====================================================
        # STEP 6 : GENERATE RESPONSE
        # =====================================================

        response = self.llm.generate(
            prompt=message,
            system_prompt=self._build_system_prompt(
                context,
                behavioral_context,
            ),
        )

        return response

    def _build_context(
        self,
        memories,
    ) -> str:

        if not memories:

            return (
                "No relevant memories were found."
            )

        lines = []

        for memory in memories:

            lines.append(
                f"- {memory.content}"
            )

        return "\n".join(lines)

    def _build_behavioral_context(
        self,
        user_id: str,
    ) -> str:

        evidence = [
            item
            for item in self.memory_manager
            .behavioral_accumulator
            .get_all()
            if item.get("user_id") == user_id
        ]

        if not evidence:

            return (
                "No behavioral profile is available."
            )

        grouped_evidence = defaultdict(list)

        for item in evidence:

            concept = item.get("concept")

            if concept is not None:

                grouped_evidence[concept].append(
                    item
                )

        if not grouped_evidence:

            return (
                "No behavioral profile is available."
            )

        lines = []

        for concept, concept_evidence in (
            grouped_evidence.items()
        ):

            profile = build_behavioral_profile(
                concept_evidence
            )

            lines.append(
                f"- Concept: {profile['concept']}"
            )

            lines.append(
                f"  Behavior: {profile['behavior']}"
            )

            lines.append(
                f"  Direction: {profile['direction']}"
            )

            lines.append(
                f"  Evidence count: "
                f"{profile['evidence_count']}"
            )

            lines.append(
                f"  Confidence: "
                f"{profile['confidence']:.2f}"
            )

        return "\n".join(lines)

    def _build_system_prompt(
        self,
        context: str,
        behavioral_context: str,
    ) -> str:

        return f"""
You are an AI assistant with a human-like memory system.

Use the following memories when they are relevant
to the current conversation.

MEMORIES:
{context}

BEHAVIORAL PROFILE:
{behavioral_context}

Behavioral profile rules:

- Use behavioral information only when relevant.
- Adapt responses when a behavioral preference,
  usage pattern, or learning pattern is relevant.
- Do not mention the behavioral profile itself
  unless explicitly asked.
- Do not reveal confidence scores or internal
  behavioral evidence.
- Do not treat a behavioral inference as an absolute
  fact when the evidence is weak or conflicting.
- If the behavioral profile conflicts with newer
  information, prefer the newer information.

Memory rules:

- Use memories only when relevant.
- Do not invent memories.
- Do not claim to remember something that is not
  present in the provided memory context.
- Connect related memories when appropriate.
- If multiple memories provide different parts of
  the answer, combine them naturally.
- Do not reveal internal memory scores or system
  implementation details unless explicitly asked.
"""