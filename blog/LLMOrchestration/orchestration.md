---
layout: default
---

# LLM Orchestration: Task Decomposition, Coordination, and Architecture Styles


## Introduction

LLM orchestration refers to the mechanisms by which large language models decompose complex tasks into manageable subtasks, coordinate their execution, and synthesize results into coherent outputs. This blog surveys the foundational papers and architectural paradigms that have shaped this rapidly evolving field. The research is organized into five thematic buckets—single-agent reasoning, tool-augmented systems, task decomposition frameworks, multi-agent orchestration, and framework implementations—each representing a distinct architectural philosophy for how LLMs organize and coordinate work.

***

## Single-Agent (Foundational) Reasoning Architectures

The earliest orchestration mechanisms emerged from advances in LLM reasoning itself. These approaches enable a single LLM to break problems into steps internally, forming the cognitive backbone upon which more complex orchestration systems are built.

### Chain-of-Thought (CoT) Prompting

Chain-of-Thought[^1] prompting demonstrated that providing a few examples of intermediate reasoning steps dramatically improves LLM performance on complex reasoning tasks. The key insight is that CoT allows models to "decompose multi-step problems into intermediate steps," allocating additional computation to harder problems. CoT is the simplest form of task decomposition—linear, sequential step generation within a single inference pass—and serves as the foundation for all subsequent orchestration methods.


### ReAct: Reasoning + Acting

Yao et al. [^2] introduced ReAct, which interleaves reasoning traces with task-specific actions in a loop. Unlike CoT, which operates purely internally, ReAct enables the LLM to interact with external tools (e.g., search APIs, calculators) during its reasoning process. The framework follows a Thought → Action → Observation cycle that repeats until the final answer is reached. ReAct [^3] represents the first true orchestration pattern: the LLM acts as both planner and coordinator, deciding when to reason internally versus when to delegate to external tools.

### Self Consistency 
Wang et al. [^7] introduced Self Consistency, which generates multiple CoT reasoning paths and selects the most consistent answer through majority voting. This approach leverages the diversity of reasoning paths to mitigate errors from any single path, significantly improving accuracy on multi-step tasks.   It introduces multi-path reasoning but without the structured search and backtracking that ToT adds.


### Tree of Thoughts (ToT)

Yao et al. [^4] generalized CoT into a tree-structured search over reasoning paths. ToT treats intermediate "thoughts" as nodes in a search tree, using breadth-first or depth-first search combined with LLM self-evaluation to explore multiple reasoning paths simultaneously. The framework enables backtracking when a reasoning path fails, a capability absent from linear CoT. Experiments showed significant improvements on tasks requiring non-trivial planning, such as the Game of 24 and creative writing.

### Graph of Thoughts (GoT)

Besta et al. [^5] further extended the ToT paradigm by modeling LLM reasoning as an arbitrary directed graph. GoT enables combining thoughts from different branches (aggregation), refining existing thoughts (feedback loops), and distilling networks of thoughts into compact summaries. This increased the quality of planning while reducing costs. GoT represents the most general single-agent reasoning topology, subsuming both CoT (a chain/path) and ToT (a tree) as special cases.

### Verbal Reinforcement Learning (Reflexion)
Shinn et al. [^6] introduced Reflexion, which endows agents with verbal self-reflection to learn from failures across trials. After each attempt, the agent generates a textual self-critique that is stored in memory and used as additional context in subsequent trials. This "semantic gradient" signal provides concrete direction for improvement and represents orchestration of the agent's own learning process across time.

***

## Tool-Augmented LLM Systems

### MRKL Systems (routing concept)
Karpas et al. [^8] introduced Modular Reasoning, Knowledge and Language (MRKL) systems, a novel architecture that combines LLMs with external knowledge sources and discrete reasoning modules. In a MRKL system, a router analyzes incoming queries and directs them to the most appropriate module—either the core LLM, a symbolic module (e.g., tools), or an external database. This architecture introduced the fundamental pattern of LLM-as-router, where the language model's role shifts from executor to orchestrator that delegates work to specialized components.

### Toolformer (internalized tool use)
Schick et al. [^9] took a different approach with Toolformer, training an LLM to autonomously decide which APIs to call, when to call them, and what arguments to pass. The model learns tool usage in a self-supervised way, annotating training data with API calls where tools would improve token prediction. Toolformer's significance lies in making tool orchestration an intrinsic capability of the model itself, rather than an external framework.

### Gorilla (reliable API calling)
Patil et al. [^10] addressed a critical reliability problem in tool-augmented systems: LLMs frequently hallucinate API calls, generating plausible but incorrect function names, parameters, or signatures. Gorilla tackled this by fine-tuning an LLM specifically on large-scale API documentation, enabling it to generate accurate and up-to-date API calls. Combined with a retrieval system that grounds generation in current documentation, Gorilla outperformed even GPT-4 on correct API invocation, demonstrating that reliable tool use at scale requires dedicated training rather than prompting alone.


### ToolLLM (scaled multi-tool reasoning)
Qin et al. [^11] scaled tool-augmented reasoning further with ToolLLM, constructing a benchmark of over 16,000 real-world REST APIs and training models to handle complex multi-tool scenarios. The framework introduced a depth-first search-based decision tree (DFSDT) that enables LLMs to reason about and recover from errors during multi-step API calling. ToolLLM demonstrated that with sufficient training data and structured search over tool-use plans, open-source models could approach the multi-tool reasoning capabilities of closed-source models.


### HuggingGPT (full model orchestration)
Shen et al. [^12] presented HuggingGPT, which uses ChatGPT as an orchestrator to coordinate hundreds of specialized AI models from Hugging Face. The workflow consists of four stages: (1) task planning—the LLM decomposes user requests into structured tasks with dependencies; (2) model selection—matching tasks to the best available models; (3) task execution—running selected models with dependency management and parallelization; and (4) response generation—integrating all results into a final answer. HuggingGPT demonstrated that an LLM could serve as a universal task planner and coordinator for an entire ecosystem of AI models.

***


## Task Decomposition Frameworks

Task decomposition—how complex goals are broken into subtasks—is the core mechanism of LLM orchestration. While single-agent reasoning  architectures discussed above perform decomposition implicitly within their inference pass, the frameworks in this section make decomposition an explicit, structured process. The literature broadly distinguishes two paradigms: iterative decomposition, where subtasks are revealed and solved one at a time with each step informed by previous results, and upfront 
plan-then-execute decomposition, where all subtasks are generated first and then executed in sequence.

### Least-to-Most Prompting (simple decomposition)

Zhou et al. [^13] introduced Least-to-Most (LtM) prompting, a two-stage 
method that first decomposes a complex problem into a series of simpler 
subproblems, then solves them sequentially from easiest to hardest. 
Critically, each subproblem's solution is fed into the prompt for the next, 
allowing the model to build on intermediate results. LtM established 
the upfront plan-then-execute paradigm that subsequent frameworks refined.

### Decomposed Prompting (modular decomposition)

Khot et al. [^14] extended decomposition further with Decomposed Prompting, 
which delegates each sub-task to a specialized handler—either a differently-
prompted LLM, a symbolic function (e.g., a calculator), or a trained model. 
Unlike LtM, which uses a single LLM for both decomposition and solving, 
DecomP allows diverse decomposition structures including recursion and 
non-linear branching. This modular architecture introduced the principle 
that decomposition and sub-task execution can be handled by entirely different 
systems, foreshadowing multi-agent orchestration patterns.

### Plan-and-Solve Prompting (zero-shot decomposition)

Wang et al. [^18] formalized the plan-then-execute paradigm with Plan-and-
Solve (PS) Prompting. The approach replaces CoT's "Let's think step by step" 
with an explicit two-phase instruction: first devise a plan, then execute it 
step by step. PS+ extended this with detailed instructions such as "extract 
relevant variables" and "calculate intermediate results" to reduce 
calculation errors and missing reasoning steps. Plan-and-Solve demonstrated 
that even zero-shot prompting could achieve structured decomposition, 
bridging the gap between prompting techniques and agent planning 
architectures.

### Decomposition Topologies (decomposition theory)

The PlanGenLLMs survey [^15] provides a useful taxonomy: 
sequential decomposition, where each subtask depends on its predecessor in 
a linear chain; parallel decomposition, where independent subtasks share 
the same preconditions and can execute concurrently; and recursive 
decomposition, where any decomposition mode is applied repeatedly, breaking 
subtasks into further sub-subtasks until each is atomically executable. These 
topologies are not mutually exclusive—complex tasks often combine sequential 
dependencies with parallelizable branches, forming DAG (directed acyclic 
graph) structures.

### Hierarchical Task Decomposition

Hierarchical planning extends these topologies by organizing subtasks across 
multiple levels of abstraction. High-level steps are progressively refined 
into executable actions, either top-down (generating all high-level steps 
first, then refining) or incrementally (refining each step as it is reached). 
The Agent-Oriented Planning framework [^16] formalized 
three design principles for effective decomposition: solvability (each 
subtask must be independently solvable by an available agent), completeness 
(subtasks must collectively cover all aspects of the original query), and 
non-redundancy (no duplicate or irrelevant tasks). These principles provide 
a quality framework applicable to any decomposition method.

### Closed-Loop Replanning (adaptive replanning)

Static plans inevitably encounter failures during execution, making closed-
loop replanning a critical coordination mechanism.The PlanGenLLMs survey [^15] 
distinguishes between implicit closed-loop systems, which fix only the 
failed action, and explicit closed-loop systems, which regenerate the entire 
plan from the point of failure. ADaPT [^17] introduced 
recursive decomposition triggered by execution failure: when a subtask 
cannot be executed, it is further decomposed until all components are 
within the executor's capabilities. This adaptive approach prevents error 
compounding and enables LLMs to handle dynamic, long-horizon tasks.

***


## Multi-Agent Orchestration Architectures

When tasks exceed the capacity of a single LLM, multi-agent systems 
distribute intelligence across specialized agents by an orchestration layer. The literature 
describes these systems along two dimensions: the communication 
topology (how agents are connected) and the interaction paradigm 
(how agents collaborate).


### Role-Playing and Conversational Collaboration

CAMEL [^19] introduced the role-playing paradigm, 
where two LLM agents—an "AI user" and an "AI assistant"—are assigned 
complementary roles and collaborate through structured conversation 
toward task completion. Using inception prompting to maintain role 
consistency, CAMEL demonstrated that autonomous agent cooperation 
could proceed with minimal human intervention. This decentralized, 
peer-to-peer pattern established role assignment as a fundamental 
mechanism for multi-agent coordination.

### Multi-Agent Debate

Du et al. [^20] proposed multi-agent debate, where multiple LLM instances independently 
generate answers and then critique each other's reasoning over 
multiple rounds to converge on a consensus. Multi-agent debate 
introduced a competitive-cooperative dynamic—agents simultaneously 
collaborate toward correctness while challenging each other's 
reasoning—that became a widely adopted pattern for improving LLM 
reliability.

### Structured Workflow Orchestration (MetaGPT and ChatDev)

MetaGPT [^21] operationalized the 
principle "Code = SOP(Team)" by encoding standardized operating 
procedures into multi-agent collaboration. Agents are assigned 
professional roles—Product Manager, Architect, Engineer, QA 
Engineer—and interact through structured communication interfaces 
with publish-subscribe message filtering. ChatDev [^22] applied a similar philosophy, organizing agents into a 
virtual software company that follows a waterfall-style development 
process across design, coding, testing, and documentation phases. 
Both systems demonstrated that imposing human organizational 
structures on agent teams reduces the cascading 
hallucination errors that plague unstructured multi-agent 
interactions.

### Orchestration Topologies

**Centralized orchestration** employs a single controller agent 
that decomposes tasks, assigns them to specialized agents, monitors 
execution, and synthesizes outputs. This includes the 
controller-agent pattern (as in HuggingGPT), pipeline processing 
where agents are arranged linearly with each agent's output becoming 
the next agent's input, and hierarchical task decomposition where 
parent agents divide work for child agents at each level. These patterns introduce single points of failure.
**Decentralized orchestration** allows agents to operate 
autonomously based on local information. This includes swarm 
intelligence patterns where agents collaborate without hierarchy, 
and committee voting systems where agents aggregate evaluations 
through voting (as in multi-agent debate).
**Hierarchical orchestration** combines centralized oversight with 
decentralized execution, where higher-level agents manage groups of 
lower-level specialists.
**Blackboard systems** coordinate agents through a shared knowledge 
space, where agents read from and write to a common data structure. 
The orchestration layer manages contributions and ensures agents 
build on each other's work,

***

## Framework Implementations and Protocols

The theoretical architectures above are realized through Agentic AI frameworks and communication standards.

### Implementation Frameworks

| Framework | Architecture Style | Key Abstraction | Best For |
|---|---|---|---|
| LangGraph | Graph-based workflows | Agents as nodes in directed graph | Complex branching + conditional logic[^23] |
| AutoGen | Conversational multi-agent | Natural language agent dialogue | Prototyping, human-in-the-loop[^24] |
| CrewAI | Role-based collaboration | Agents with roles, tasks, crews | Business process automation[^25] |

LangGraph treats agent interactions as nodes in a directed graph, providing exceptional flexibility for workflows with conditional logic, parallel processing, and dynamic adaptation. AutoGen emphasizes conversational interactions where agents adapt roles based on context, using patterns like RoundRobinGroupChat and SelectorGroupChat for coordination. CrewAI focuses on structured role-based teams, with each agent having a clearly defined responsibility.

### Communication Protocols

Two emerging standards are formalizing inter-agent communication:

- **Model Context Protocol (MCP)**: Standardizes how agents access external tools and contextual data through a client-server design. Agents request capabilities (tools, resources, prompts) while connected systems expose these as standardized callable services.[^26]
- **Agent-to-Agent (A2A) Protocol**: Governs peer coordination, negotiation, and delegation between agents. Supports structured metadata, cryptographic signing, and role-based routing for enterprise-grade deployments.[^27]

Together, MCP handles agent-to-tool communication while A2A handles agent-to-agent communication, forming the dual foundation of orchestrated multi-agent systems.

***


## Synthesis: A Unified View of Orchestration

Evolutionary trajectory in LLM orchestration:

1. **Internal reasoning** (CoT, ToT, GoT) enables a single LLM to decompose problems cognitively, progressing from linear chains to arbitrary graph structures.
2. **Tool augmentation** (MRKL, Toolformer, HuggingGPT) extends the LLM's capabilities by connecting it to external systems, with the LLM serving as router and planner.
3. **Task decomposition frameworks** formalize how goals are broken into subtasks—sequentially, in parallel, asynchronously, or recursively—with closed-loop replanning for robustness.
4. **Multi-agent systems** distribute both reasoning and execution across specialized agents, coordinated through centralized, decentralized, hierarchical, or hybrid patterns.
5. **Standardized protocols** (MCP, A2A) and frameworks (LangGraph, AutoGen, CrewAI) bring these patterns to production, enabling interoperable, enterprise-scale deployments.

---

## References



[^1]: [Wei, Jason, et al. "Chain-of-thought prompting elicits reasoning in large language models." NeurIPS 2022.](https://webdocs.cs.ualberta.ca/~dale/papers/neurips22a.pdf)

[^2]: [Yao, Shunyu, et al. "React: Synergizing reasoning and acting in language models." ICLR 2022.](https://arxiv.org/pdf/2210.03629)

[^3]: [ReAct (Reason+Act) prompting in LLMs - tsmatz - WordPress.com](https://tsmatz.wordpress.com/2023/03/07/react-with-openai-gpt-and-langchain/)

[^4]: [Yao, Shunyu, et al. "Tree of thoughts: Deliberate problem solving with large language models." NeurIPS 2023.](https://papers.nips.cc/paper_files/paper/2023/file/271db9922b8d1f4dd7aaef84ed5ac703-Paper-Conference.pdf) 

[^5]: [Besta, Maciej, et al. "Graph of thoughts: Solving elaborate problems with large language models." AAAI 2024](https://arxiv.org/pdf/2308.09687)

[^6]: [Shinn, Noah, et al. "Reflexion: Language agents with verbal reinforcement learning." NeurIPS 2023.](https://arxiv.org/pdf/2303.11366) 

[^7]: [Wang, Xuezhi, et al. "Self-consistency improves chain of thought reasoning in language models." ICLR 2023](https://arxiv.org/pdf/2203.11171) 

[^8]: [Karpas, Ehud, et al. "MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning.](https://arxiv.org/pdf/2205.00445)

[^9]: [Schick, Timo, et al. "Toolformer: Language models can teach themselves to use tools." NeuRIPS 2023](https://arxiv.org/pdf/2302.04761)

[^10]: [Patil, Shishir G., et al. "Gorilla: Large language model connected with massive apis." NeuRIPS 2024](https://arxiv.org/pdf/2305.15334)

[^11]: [Qin, Yujia, et al. "Toolllm: Facilitating large language models to master 16000+ real-world apis." ICLR 2024](https://arxiv.org/pdf/2307.16789)

[^12]: [Shen, Yongliang, et al. "Hugginggpt: Solving ai tasks with chatgpt and its friends in hugging face." NeurIPS 2023] (https://arxiv.org/pdf/2303.17580)

[^13]: [Zhou, Denny, et al. "Least-to-most prompting enables complex reasoning in large language models." ICLR 2023](https://arxiv.org/pdf/2205.10625)

[^14]: [Khot, Tushar, et al. "Decomposed prompting: A modular approach for solving complex tasks." ICLR 2023](https://arxiv.org/pdf/2210.02406)

[^15]:  [Wei, Hui, et al. "Plangenllms: A modern survey of llm planning capabilities." ACL 2025.](https://aclanthology.org/2025.acl-long.958.pdf)

[^16]: [Li, Ao, et al. "Agent-oriented planning in multi-agent systems." ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/31610e68fe41a62e460e044216a10766-Paper-Conference.pdf)

[^17]: [Prasad, Archiki, et al. "Adapt: As-needed decomposition and planning with language models."NAACL 2024] (https://aclanthology.org/2024.findings-naacl.264.pdf)

[^18]: [Wang, Lei, et al. "Plan-and-solve prompting: Improving zero-shot chain-of-thought reasoning by large language models" ACL 2023] (https://arxiv.org/abs/2305.04091)

[^19]: [Li, Guohao, et al. "Camel: Communicative agents for" mind" exploration of large language model society." NeuRIPS 2023] (https://openreview.net/pdf?id=3IyL2XWDkG)

[^20]: [Du, Yilun, et al. "Improving factuality and reasoning in language models through multiagent debate." ICML 2024.] (https://arxiv.org/pdf/2305.14325)

[^21]: [Hong, Sirui, et al. "MetaGPT: Meta programming for a multi-agent collaborative framework." ICLR 2023.] (https://arxiv.org/pdf/2308.00352)

[^22]: [Qian, Chen, et al. "Chatdev: Communicative agents for software development." ACL 2024] (https://aclanthology.org/2024.acl-long.810.pdf)

[^23]: [LangGraph] (https://www.langchain.com/langgraph)

[^24]: [AutoGen] (https://github.com/microsoft/autogen)

[^25]: [CrewAI] (https://github.com/crewAIInc/crewAI)

[^26]: [MCP] (https://modelcontextprotocol.io/docs/getting-started/intro)

[^27]: [A2A] (https://github.com/a2aproject/A2A)
