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