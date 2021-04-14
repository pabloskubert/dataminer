# dataminer
Conjunto de scripts que desenvolvi para coletar dados em massa.

### enriquecer_target.py

  É necessário modificar o script e colocar suas credenciais do __targetdatasmart.com__
  
  Script para enriquecer uma lista de CPF's que estão em um arquivo CSV, ex:
  
```csv
  "nome","cpf","nasc"
  "robson",85712301024, "xx-xx-xxxx"
  "rowalsd",07681883002,"xx-xx-xxxx"
  
``` 

  É somente obrigatório o campo "cpf" em minúsculo.
  
#### Uso

Sintaxe:
```
 ./enriquecer_target.py [ARQ_CSV] [SALVAR_NOME] [PAROU EM]
```
Exemplo:
```
 ./enriquecer_target.py sadia_funcs.csv sadia_funcs_enriquecido 0
```

### Congonhas
Leia o readme dentro da pasta.
