## Scraper feito em bash para o sistema congonhas da novavidatec


### Problema 
A plataforma não viabiliza um mecanismo para que se extraia os funcionários de um *CNPJ* em __massa__.



### Explicação de cada arquivo/tool

*by_one* 
  
  Completa a extração um por um (sem threads)
 
*extd* 
   
   Extraí links de várias páginas html e mescla os links encontrados em um único arquivo
   útil quando se quer extrair mais de um CNPJ.
   
*html_para_csv*
  
   Usado pelo *extrair*, depois de efetuar a consulta, extraindo as informações e tirando o hipertexto.
   
*link_extrator*
  
   Cada CPF tem um link de consulta correspondente, o trabalho do *link_extrator* é extrair esses links.
   
*extrair*

   Executa uma requisição GET para o link de consulta de um CPF, faz isto em várias threads.
   
 pasta *receber_csv*
 
   O poder computacional do meu notebook é fraco suficientemente para travar em 50 threads, então adaptei este script para o seguinte modelo:
   
    meu_pc (esperando resultado) <---> ngrok <---> servidor remoto (executando o extrair)
    
   Dessa forma o "trabalho pesado" é feito pelo servidor remoto e eu só recebo o resultado.
   
### Como usar

Siga os passos abaixo para extrair funcionários em massa de um CNPJ no sistema congonhas:

  - 1º Consulte os __funcionários__ do CNPJ alvo.
  - 2º Clique em *ver mais* na página de resultado e salve a página como __html__
  - 3º Use o *link_extrator* para retirar os links de consulta para os CPF's de cada __funcionário__
  - 4º Execute o extrair: __./extrair__ sadia.links 0 "cookie" 0 

Onde: 
- sadia.links é o arquivo de saída do *link_extrator*
- 0 ~ Ignorar -> URL do ngrok para postar os resultados
- "cookie" -> Somente o __valor__ do cookie __ASP.NET_SessionId__
- 0 ~ Iniciar em, caso deseje pular (INTERRUPÇÕES)

O arquivo CSV resultado das consultas será concatenado em $HOME/INFOS_EXTRAIDAS/collect_\[RANDOM\].csv

