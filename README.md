# Gerenciamento de Escopo e Verificação de Tipos

Este projeto implementa um gerenciador de escopos e verificador de tipos para uma linguagem de programação fictícia. O objetivo é processar arquivos de código, verificar a declaração e atribuição de variáveis, e gerenciar escopos, imprimindo mensagens de erro quando necessário.

## Descrição do Projeto

O código principal está contido na classe `ScopeManager`, que utiliza expressões regulares para identificar padrões na linguagem fictícia, como declarações de variáveis, atribuições e comandos de impressão. O projeto também inclui um script para processar arquivos de entrada via linha de comando e gerar arquivos de saída com os resultados.

## Funcionalidades

- **Gerenciamento de Escopos**: Suporte para abertura e fechamento de escopos com comandos `BLOCO` e `FIM`.
- **Verificação de Tipos**: Garantia de que variáveis sejam utilizadas de acordo com seus tipos declarados.
- **Identificação de Erros**: Impressão de mensagens de erro para variáveis não declaradas e atribuições inválidas.
- **Saída para Arquivo**: Geração de arquivos de saída com os resultados do processamento.

## Uso

### Requisitos

- Python 3.6 ou superior

### Execução

```bash
python3 scope_manager.py inputs/sample_01.txt
```

O arquivo de saída será gerado na pasta `outputs/` com o mesmo nome do arquivo de entrada, mas com a extensão `.out`.

## Pseudocódigo

### Classe ScopeManager

#### Atributos
- `regex_whitespace`
- `regex_number`
- `regex_variable_number`
- `regex_string`
- `regex_variable_string`
- `regex_variable`
- `regex_print`
- `regex_declared_number`
- `regex_undeclared_number`
- `regex_declared_string`
- `regex_undeclared_string`
- `scopes`
- `output_lines`
- `block_identifiers`

#### Métodos

##### `__init__()`
- Inicializar expressões regulares para corresponder a diferentes padrões.
- Inicializar `scopes`, `output_lines` e `block_identifiers`.

##### `get_token_by_identifier(identifier)`
- Para cada escopo em ordem reversa:
  - Para cada token no escopo:
    - Se o identificador do token corresponder, retornar o token.
- Se não encontrar correspondência, retornar `None`.

##### `variable_exists(identifier, scope)`
- Verificar se algum token no escopo possui o identificador fornecido.
- Retornar `True` se encontrado, caso contrário, `False`.

##### `assign_value_to_token(identifier, value)`
- Para cada escopo em ordem reversa:
  - Para cada token no escopo:
    - Se o identificador do token corresponder, atualizar seu valor.

##### `process_line(line, line_number)`
- Limpar e formatar a linha.
- Se a linha iniciar um bloco:
  - Adicionar o identificador do bloco a `block_identifiers`.
  - Adicionar um novo escopo a `scopes`.
  - Adicionar um marcador de início de bloco a `output_lines`.
- Se a linha finalizar um bloco:
  - Remover o último escopo de `scopes`.
  - Adicionar um marcador de fim de bloco a `output_lines`.
  - Remover o identificador do bloco de `block_identifiers`.
- Outras operações específicas de linhas de acordo com as variáveis e atribuições.

##### `process_scope(file_path)`
- Abrir o arquivo e ler as linhas.
- Para cada linha no arquivo:
  - Chamar `process_line` para a linha.
- Garantir que o diretório de saída exista.
- Escrever `output_lines` em um arquivo de saída.

#### Execução Principal
- Analisar argumentos da linha de comando para obter o caminho do arquivo.
- Criar uma instância de `ScopeManager`.
- Chamar `process_scope` com o caminho do arquivo fornecido.