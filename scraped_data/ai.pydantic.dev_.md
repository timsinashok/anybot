[ Skip to content ](https://ai.pydantic.dev/<#introduction>)
[ ![logo](https://ai.pydantic.dev/img/logo-white.svg) ](https://ai.pydantic.dev/<.> "PydanticAI")
PydanticAI 
Introduction 
Type to start searching
[ pydantic/pydantic-ai  ](https://ai.pydantic.dev/<https:/github.com/pydantic/pydantic-ai> "Go to repository")
[ ![logo](https://ai.pydantic.dev/img/logo-white.svg) ](https://ai.pydantic.dev/<.> "PydanticAI") PydanticAI 
[ pydantic/pydantic-ai  ](https://ai.pydantic.dev/<https:/github.com/pydantic/pydantic-ai> "Go to repository")
  * Introduction  [ Introduction  ](https://ai.pydantic.dev/<.>) Table of contents 
    * [ Why use PydanticAI  ](https://ai.pydantic.dev/<#why-use-pydanticai>)
    * [ Hello World Example  ](https://ai.pydantic.dev/<#hello-world-example>)
    * [ Tools & Dependency Injection Example  ](https://ai.pydantic.dev/<#tools-dependency-injection-example>)
    * [ Instrumentation with Pydantic Logfire  ](https://ai.pydantic.dev/<#instrumentation-with-pydantic-logfire>)
    * [ Next Steps  ](https://ai.pydantic.dev/<#next-steps>)
  * [ Installation  ](https://ai.pydantic.dev/<install/>)
  * [ Getting Help  ](https://ai.pydantic.dev/<help/>)
  * [ Contributing  ](https://ai.pydantic.dev/<contributing/>)
  * [ Troubleshooting  ](https://ai.pydantic.dev/<troubleshooting/>)
  * Documentation  Documentation 
    * [ Agents  ](https://ai.pydantic.dev/<agents/>)
    * [ Models  ](https://ai.pydantic.dev/<models/>)
    * [ Dependencies  ](https://ai.pydantic.dev/<dependencies/>)
    * [ Function Tools  ](https://ai.pydantic.dev/<tools/>)
    * [ Results  ](https://ai.pydantic.dev/<results/>)
    * [ Messages and chat history  ](https://ai.pydantic.dev/<message-history/>)
    * [ Testing and Evals  ](https://ai.pydantic.dev/<testing-evals/>)
    * [ Debugging and Monitoring  ](https://ai.pydantic.dev/<logfire/>)
    * [ Multi-agent Applications  ](https://ai.pydantic.dev/<multi-agent-applications/>)
    * [ Graphs  ](https://ai.pydantic.dev/<graph/>)
  * [ Examples  ](https://ai.pydantic.dev/<examples/>)
Examples 
    * [ Pydantic Model  ](https://ai.pydantic.dev/<examples/pydantic-model/>)
    * [ Weather agent  ](https://ai.pydantic.dev/<examples/weather-agent/>)
    * [ Bank support  ](https://ai.pydantic.dev/<examples/bank-support/>)
    * [ SQL Generation  ](https://ai.pydantic.dev/<examples/sql-gen/>)
    * [ Flight booking  ](https://ai.pydantic.dev/<examples/flight-booking/>)
    * [ RAG  ](https://ai.pydantic.dev/<examples/rag/>)
    * [ Stream markdown  ](https://ai.pydantic.dev/<examples/stream-markdown/>)
    * [ Stream whales  ](https://ai.pydantic.dev/<examples/stream-whales/>)
    * [ Chat App with FastAPI  ](https://ai.pydantic.dev/<examples/chat-app/>)
    * [ Question Graph  ](https://ai.pydantic.dev/<examples/question-graph/>)
  * API Reference  API Reference 
    * [ pydantic_ai.agent  ](https://ai.pydantic.dev/<api/agent/>)
    * [ pydantic_ai.tools  ](https://ai.pydantic.dev/<api/tools/>)
    * [ pydantic_ai.result  ](https://ai.pydantic.dev/<api/result/>)
    * [ pydantic_ai.messages  ](https://ai.pydantic.dev/<api/messages/>)
    * [ pydantic_ai.exceptions  ](https://ai.pydantic.dev/<api/exceptions/>)
    * [ pydantic_ai.settings  ](https://ai.pydantic.dev/<api/settings/>)
    * [ pydantic_ai.usage  ](https://ai.pydantic.dev/<api/usage/>)
    * [ pydantic_ai.format_as_xml  ](https://ai.pydantic.dev/<api/format_as_xml/>)
    * [ pydantic_ai.models  ](https://ai.pydantic.dev/<api/models/base/>)
    * [ pydantic_ai.models.openai  ](https://ai.pydantic.dev/<api/models/openai/>)
    * [ pydantic_ai.models.anthropic  ](https://ai.pydantic.dev/<api/models/anthropic/>)
    * [ pydantic_ai.models.cohere  ](https://ai.pydantic.dev/<api/models/cohere/>)
    * [ pydantic_ai.models.gemini  ](https://ai.pydantic.dev/<api/models/gemini/>)
    * [ pydantic_ai.models.vertexai  ](https://ai.pydantic.dev/<api/models/vertexai/>)
    * [ pydantic_ai.models.groq  ](https://ai.pydantic.dev/<api/models/groq/>)
    * [ pydantic_ai.models.mistral  ](https://ai.pydantic.dev/<api/models/mistral/>)
    * [ pydantic_ai.models.test  ](https://ai.pydantic.dev/<api/models/test/>)
    * [ pydantic_ai.models.function  ](https://ai.pydantic.dev/<api/models/function/>)
    * [ pydantic_graph  ](https://ai.pydantic.dev/<api/pydantic_graph/graph/>)
    * [ pydantic_graph.nodes  ](https://ai.pydantic.dev/<api/pydantic_graph/nodes/>)
    * [ pydantic_graph.state  ](https://ai.pydantic.dev/<api/pydantic_graph/state/>)
    * [ pydantic_graph.mermaid  ](https://ai.pydantic.dev/<api/pydantic_graph/mermaid/>)
    * [ pydantic_graph.exceptions  ](https://ai.pydantic.dev/<api/pydantic_graph/exceptions/>)


Table of contents 
  * [ Why use PydanticAI  ](https://ai.pydantic.dev/<#why-use-pydanticai>)
  * [ Hello World Example  ](https://ai.pydantic.dev/<#hello-world-example>)
  * [ Tools & Dependency Injection Example  ](https://ai.pydantic.dev/<#tools-dependency-injection-example>)
  * [ Instrumentation with Pydantic Logfire  ](https://ai.pydantic.dev/<#instrumentation-with-pydantic-logfire>)
  * [ Next Steps  ](https://ai.pydantic.dev/<#next-steps>)


Version Notice
This documentation is ahead of the last release by [1 commit](https://ai.pydantic.dev/<https:/github.com/pydantic/pydantic-ai/compare/v0.0.25...main>). You may see documentation for features not yet supported in the latest release [v0.0.25 2025-02-12](https://ai.pydantic.dev/<https:/github.com/pydantic/pydantic-ai/releases/tag/v0.0.25>). 
# Introduction
![PydanticAI](https://ai.pydantic.dev/img/pydantic-ai-dark.svg#only-dark)
![PydanticAI](https://ai.pydantic.dev/img/pydantic-ai-light.svg#only-light)
_Agent Framework / shim to use Pydantic with LLMs_
[ ![CI](https://github.com/pydantic/pydantic-ai/actions/workflows/ci.yml/badge.svg?event=push) ](https://ai.pydantic.dev/<https:/github.com/pydantic/pydantic-ai/actions/workflows/ci.yml?query=branch%3Amain>) [ ![Coverage](https://coverage-badge.samuelcolvin.workers.dev/pydantic/pydantic-ai.svg) ](https://ai.pydantic.dev/<https:/coverage-badge.samuelcolvin.workers.dev/redirect/pydantic/pydantic-ai>) [ ![PyPI](https://img.shields.io/pypi/v/pydantic-ai.svg) ](https://ai.pydantic.dev/<https:/pypi.python.org/pypi/pydantic-ai>) [ ![versions](https://img.shields.io/pypi/pyversions/pydantic-ai.svg) ](https://ai.pydantic.dev/<https:/github.com/pydantic/pydantic-ai>) [ ![license](https://img.shields.io/github/license/pydantic/pydantic-ai.svg) ](https://ai.pydantic.dev/<https:/github.com/pydantic/pydantic-ai/blob/main/LICENSE>)
PydanticAI is a Python agent framework designed to make it less painful to build production grade applications with Generative AI. 
PydanticAI is a Python Agent Framework designed to make it less painful to build production grade applications with Generative AI.
FastAPI revolutionized web development by offering an innovative and ergonomic design, built on the foundation of [Pydantic](https://ai.pydantic.dev/<https:/docs.pydantic.dev>).
Similarly, virtually every agent framework and LLM library in Python uses Pydantic, yet when we began to use LLMs in [Pydantic Logfire](https://ai.pydantic.dev/<https:/pydantic.dev/logfire>), we couldn't find anything that gave us the same feeling.
We built PydanticAI with one simple aim: to bring that FastAPI feeling to GenAI app development.
## Why use PydanticAI
  * **Built by the Pydantic Team** : Built by the team behind [Pydantic](https://ai.pydantic.dev/<https:/docs.pydantic.dev/latest/>) (the validation layer of the OpenAI SDK, the Anthropic SDK, LangChain, LlamaIndex, AutoGPT, Transformers, CrewAI, Instructor and many more).
  * **Model-agnostic** : Supports OpenAI, Anthropic, Gemini, Deepseek, Ollama, Groq, Cohere, and Mistral, and there is a simple interface to implement support for [other models](https://ai.pydantic.dev/<models/>).
  * **Pydantic Logfire Integration** : Seamlessly [integrates](https://ai.pydantic.dev/<logfire/>) with [Pydantic Logfire](https://ai.pydantic.dev/<https:/pydantic.dev/logfire>) for real-time debugging, performance monitoring, and behavior tracking of your LLM-powered applications.
  * **Type-safe** : Designed to make [type checking](https://ai.pydantic.dev/<agents/#static-type-checking>) as powerful and informative as possible for you.
  * **Python-centric Design** : Leverages Python's familiar control flow and agent composition to build your AI-driven projects, making it easy to apply standard Python best practices you'd use in any other (non-AI) project.
  * **Structured Responses** : Harnesses the power of [Pydantic](https://ai.pydantic.dev/<https:/docs.pydantic.dev/latest/>) to [validate and structure](https://ai.pydantic.dev/<results/#structured-result-validation>) model outputs, ensuring responses are consistent across runs.
  * **Dependency Injection System** : Offers an optional [dependency injection](https://ai.pydantic.dev/<dependencies/>) system to provide data and services to your agent's [system prompts](https://ai.pydantic.dev/<agents/#system-prompts>), [tools](https://ai.pydantic.dev/<tools/>) and [result validators](https://ai.pydantic.dev/<results/#result-validators-functions>). This is useful for testing and eval-driven iterative development.
  * **Streamed Responses** : Provides the ability to [stream](https://ai.pydantic.dev/<results/#streamed-results>) LLM outputs continuously, with immediate validation, ensuring rapid and accurate results.
  * **Graph Support** : [Pydantic Graph](https://ai.pydantic.dev/<graph/>) provides a powerful way to define graphs using typing hints, this is useful in complex applications where standard control flow can degrade to spaghetti code.


In Beta
PydanticAI is in early beta, the API is still subject to change and there's a lot more to do. [Feedback](https://ai.pydantic.dev/<https:/github.com/pydantic/pydantic-ai/issues>) is very welcome!
## Hello World Example
Here's a minimal example of PydanticAI:
hello_world.py```
frompydantic_aiimport Agent
agent = Agent( 
We configure the agent to use Gemini 1.5's Flash[](https://ai.pydantic.dev/<api/models/gemini/>) model, but you can also set the model when running the agent.
[](https://ai.pydantic.dev/<#__code_0_annotation_1>)
  'google-gla:gemini-1.5-flash',
  system_prompt='Be concise, reply with one sentence.', 
Register a static system prompt[](https://ai.pydantic.dev/<agents/#system-prompts>) using a keyword argument to the agent.
[](https://ai.pydantic.dev/<#__code_0_annotation_2>)
)
result = agent.run_sync('Where does "hello world" come from?') 
Run the agent[](https://ai.pydantic.dev/<agents/#running-agents>) synchronously, conducting a conversation with the LLM.
[](https://ai.pydantic.dev/<#__code_0_annotation_3>)
print(result.data)
"""
The first known use of "hello, world" was in a 1974 textbook about the C programming language.
"""

```

_(This example is complete, it can be run "as is")_
The exchange should be very short: PydanticAI will send the system prompt and the user query to the LLM, the model will return a text response.
Not very interesting yet, but we can easily add "tools", dynamic system prompts, and structured responses to build more powerful agents.
## Tools & Dependency Injection Example
Here is a concise example using PydanticAI to build a support agent for a bank:
bank_support.py```
fromdataclassesimport dataclass
frompydanticimport BaseModel, Field
frompydantic_aiimport Agent, RunContext
frombank_databaseimport DatabaseConn

@dataclass
classSupportDependencies: 
The SupportDependencies dataclass is used to pass data, connections, and logic into the model that will be needed when running system prompt[](https://ai.pydantic.dev/<agents/#system-prompts>) and tool[](https://ai.pydantic.dev/<tools/>) functions. PydanticAI's system of dependency injection provides a type-safe[](https://ai.pydantic.dev/<agents/#static-type-checking>) way to customise the behavior of your agents, and can be especially useful when running unit tests[](https://ai.pydantic.dev/<testing-evals/>) and evals.
[](https://ai.pydantic.dev/<#__code_1_annotation_3>)
  customer_id: int
  db: DatabaseConn 
This is a simple sketch of a database connection, used to keep the example short and readable. In reality, you'd be connecting to an external database (e.g. PostgreSQL) to get information about customers.
[](https://ai.pydantic.dev/<#__code_1_annotation_12>)

classSupportResult(BaseModel): 
This Pydantic[](https://ai.pydantic.dev/<https:/docs.pydantic.dev>) model is used to constrain the structured data returned by the agent. From this simple definition, Pydantic builds the JSON Schema that tells the LLM how to return the data, and performs validation to guarantee the data is correct at the end of the run.
[](https://ai.pydantic.dev/<#__code_1_annotation_13>)
  support_advice: str = Field(description='Advice returned to the customer')
  block_card: bool = Field(description="Whether to block the customer's card")
  risk: int = Field(description='Risk level of query', ge=0, le=10)

support_agent = Agent( 
This agent[](https://ai.pydantic.dev/<agents/>) will act as first-tier support in a bank. Agents are generic in the type of dependencies they accept and the type of result they return. In this case, the support agent has type Agent[SupportDependencies, SupportResult].
[](https://ai.pydantic.dev/<#__code_1_annotation_1>)
  'openai:gpt-4o', 
Here we configure the agent to use OpenAI's GPT-4o model[](https://ai.pydantic.dev/<api/models/openai/>), you can also set the model when running the agent.
[](https://ai.pydantic.dev/<#__code_1_annotation_2>)
  deps_type=SupportDependencies,
  result_type=SupportResult, 
The response from the agent will, be guaranteed to be a SupportResult, if validation fails reflection[](https://ai.pydantic.dev/<agents/#reflection-and-self-correction>) will mean the agent is prompted to try again.
[](https://ai.pydantic.dev/<#__code_1_annotation_9>)
  system_prompt=( 
Static system prompts[](https://ai.pydantic.dev/<agents/#system-prompts>) can be registered with the system_prompt keyword argument[](https://ai.pydantic.dev/<api/agent/#pydantic_ai.agent.Agent.__init__>) to the agent.
[](https://ai.pydantic.dev/<#__code_1_annotation_4>)
    'You are a support agent in our bank, give the '
    'customer support and judge the risk level of their query.'
  ),
)

@support_agent.system_prompt 
Dynamic system prompts[](https://ai.pydantic.dev/<agents/#system-prompts>) can be registered with the @agent.system_prompt[](https://ai.pydantic.dev/<api/agent/#pydantic_ai.agent.Agent.system_prompt>) decorator, and can make use of dependency injection. Dependencies are carried via the RunContext[](https://ai.pydantic.dev/<api/tools/#pydantic_ai.tools.RunContext>) argument, which is parameterized with the deps_type from above. If the type annotation here is wrong, static type checkers will catch it.
[](https://ai.pydantic.dev/<#__code_1_annotation_5>)
async defadd_customer_name(ctx: RunContext[SupportDependencies]) -> str:
  customer_name = await ctx.deps.db.customer_name(id=ctx.deps.customer_id)
  return f"The customer's name is {customer_name!r}"

@support_agent.tool 
tool[](https://ai.pydantic.dev/<tools/>) let you register functions which the LLM may call while responding to a user. Again, dependencies are carried via RunContext[](https://ai.pydantic.dev/<api/tools/#pydantic_ai.tools.RunContext>), any other arguments become the tool schema passed to the LLM. Pydantic is used to validate these arguments, and errors are passed back to the LLM so it can retry.
[](https://ai.pydantic.dev/<#__code_1_annotation_6>)
async defcustomer_balance(
  ctx: RunContext[SupportDependencies], include_pending: bool
) -> float:
"""Returns the customer's current account balance.""" 
The docstring of a tool is also passed to the LLM as the description of the tool. Parameter descriptions are extracted[](https://ai.pydantic.dev/<tools/#function-tools-and-schema>) from the docstring and added to the parameter schema sent to the LLM.
[](https://ai.pydantic.dev/<#__code_1_annotation_7>)
  return await ctx.deps.db.customer_balance(
    id=ctx.deps.customer_id,
    include_pending=include_pending,
  )

... 
In a real use case, you'd add more tools and a longer system prompt to the agent to extend the context it's equipped with and support it can provide.
[](https://ai.pydantic.dev/<#__code_1_annotation_11>)

async defmain():
  deps = SupportDependencies(customer_id=123, db=DatabaseConn())
  result = await support_agent.run('What is my balance?', deps=deps) 
Run the agent[](https://ai.pydantic.dev/<agents/#running-agents>) asynchronously, conducting a conversation with the LLM until a final response is reached. Even in this fairly simple case, the agent will exchange multiple messages with the LLM as tools are called to retrieve a result.
[](https://ai.pydantic.dev/<#__code_1_annotation_8>)
  print(result.data) 
The result will be validated with Pydantic to guarantee it is a SupportResult, since the agent is generic, it'll also be typed as a SupportResult to aid with static type checking.
[](https://ai.pydantic.dev/<#__code_1_annotation_10>)
"""
  support_advice='Hello John, your current account balance, including pending transactions, is $123.45.' block_card=False risk=1
  """
  result = await support_agent.run('I just lost my card!', deps=deps)
  print(result.data)
"""
  support_advice="I'm sorry to hear that, John. We are temporarily blocking your card to prevent unauthorized transactions." block_card=True risk=8
  """

```

Complete `bank_support.py` example
The code included here is incomplete for the sake of brevity (the definition of `DatabaseConn` is missing); you can find the complete `bank_support.py` example [here](https://ai.pydantic.dev/<examples/bank-support/>).
## Instrumentation with Pydantic Logfire
To understand the flow of the above runs, we can watch the agent in action using Pydantic Logfire.
To do this, we need to set up logfire, and add the following to our code:
bank_support_with_logfire.py```
...
frombank_databaseimport DatabaseConn
importlogfire
logfire.configure() 
Configure logfire, this will fail if project is not set up.
[](https://ai.pydantic.dev/<#__code_2_annotation_1>)
logfire.instrument_asyncpg() 
In our demo, DatabaseConn uses asyncpg[](https://ai.pydantic.dev/<>) to connect to a PostgreSQL database, so logfire.instrument_asyncpg()[](https://ai.pydantic.dev/<https:/magicstack.github.io/asyncpg/current/>) is used to log the database queries.
[](https://ai.pydantic.dev/<#__code_2_annotation_2>)
...

```

That's enough to get the following view of your agent in action:
See [Monitoring and Performance](https://ai.pydantic.dev/<logfire/>) to learn more.
## Next Steps
To try PydanticAI yourself, follow the instructions [in the examples](https://ai.pydantic.dev/<examples/>).
Read the [docs](https://ai.pydantic.dev/<agents/>) to learn more about building applications with PydanticAI.
Read the [API Reference](https://ai.pydantic.dev/<api/agent/>) to understand PydanticAI's interface.
© Pydantic Services Inc. 2024 to present 
