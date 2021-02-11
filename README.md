[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/berrondo/ledge)

# The Ledger

foundation ledger to django applications which deals with financial data.

some insights:

https://medium.com/memobank/choosing-an-architecture-85750e1e5a03

https://www.ibase.ru/files/articles/programming/dbmstrees/sqltrees.html

http://mikehillyer.com/articles/managing-hierarchical-data-in-mysql/

the MVP:

https://medium.com/@hnordt/como-pagar-6-de-impostos-dentro-da-lei-a91c23868ec6


    Venda(
        Imposto(),
    )
    
    class Transacao
    class Venda(Transacao)
    class Imposto(Transacao)
    
    Venda
      +- Imposto
