<h1>
  <p align="center">
    C++ FQN Parser
  </p>
</h1>

<p align="center">
  <a href="https://github.com/Cliper27/cpp_fqn_parser/actions/workflows/pytest.yaml">
    <img src="https://github.com/Cliper27/cpp_fqn_parser/actions/workflows/pytest.yaml/badge.svg" alt="Pytest Status"></a>
  <a href="https://github.com/Cliper27/cpp_fqn_parser/actions/workflows/mypy.yaml">
    <img src="https://github.com/Cliper27/cpp_fqn_parser/actions/workflows/mypy.yaml/badge.svg" alt="Mypy Status"></a>
</p>

# Overview
This is a C++ FQN (_Fully Qualified Name_) parser/tokenizer.

## Example

```python
>>> from cpp_fqn_parser import Parser, FQN
>>> fqn = "int one_3hello0::tconstwo<mytemplate>::three(const four &) volatile"
>>> parser: Parser = Parser(fqn)
>>> result: FQN = parser.parse()
>>> print(*[f"\n{scope}" for scope in result.scopes])

Scope(name='one_3hello0', template=None) 
Scope(name='tconstwo', template='<mytemplate>')

```
