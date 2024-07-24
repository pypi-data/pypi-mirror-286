# Ally AI

## How to use

### Config File

```yaml
llm:
  api_key: '<private-key>'
  api_version: "<api-version>"
  endpoint: "<endpoint>"
  model: "<model-name>"
  deployment_name: '<deployment-name>'
  temperature: 0.7
  streaming: true

embeddings:
  api_key: '<private-key>'
  api_version: "<api-version>"
  endpoint: "<endpoint>"
  model: "<model-name>"
  deployment_name: '<deployment-name>'
```

### Create LLM

#### Use Default Settings in LLM

```python
from ally_ai.langchain import LLM

llm = LLM()
response = llm.invoke('What is an ally?')
print(response)
```

#### Use Custom Settings in LLM

```yaml
my_llm:
  api_key: '<private-key>'
  api_version: "<api-version>"
```

```python
from ally_ai.langchain import LLM, Settings

settings = Settings(section='my_llm')
llm = LLM(settings=settings)
print(llm.settings.path)
print(llm.settings.section)
```

#### Override Settings in LLM

```python
from ally_ai.langchain import LLM, Settings

settings = Settings(section='my_llm', api_key='<new-api-key>')
llm = LLM(settings=settings)
response = llm.invoke('What is an ally?')
print(response)
```


### How to Create Embeddings

```python
from ally_ai.langchain import Embeddings

embeddings = Embeddings()
response = embeddings.embed_query('What is an ally?')
print(response)
```

