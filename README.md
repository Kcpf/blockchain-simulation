## Consenso

A ideia deste entregável é aprender o conceito básico do algoritmo de consenso Proof of Work, utilizado no processo de mineração de várias criptomoedas, como o Bitcoin. Assim, conforme visto na aula, você precisara descobrir um "nonce" que, somado às informações contidas no bloco, gere um hash válido para a dificuldade definida pela rede.

O bloco deste exercício contém sete informações:

- Difficulty (dificuldade da rede)
- Height (altura do bloco)
- Merkle Root (raiz merkle das transações)
- Nonce
- Previous Hash (hash do bloco anterior)
- Timestamp (data e horário)
- Transactions (lista de strings contendo as transações)

A estrutura segue o seguinte exemplo de string em Python: f"{height}{previous_hash}{merkle_root}{timestamp}{difficulty}{nonce}".

Obs:
**Tenha em mente que a dificuldade pode variar.** Uma dificuldade 3, necessita que vocês gerem um hash com três zeros no começo, por exemplo: 00024232cdd221771294dfbb310aca000a0df6ac8b66b696d90ef06fdefb64a3

Informações técnicas:

- **Você poderá usar a linguagem e biblioteca que desejar**
- Recomendamos, pela simplicidade, Python ou Javasript
- Dicas:
  - Biblioteca Crypto e Axios (Javascript)
  - Bibliotecas Python Dome, Starkbank e requests (Python)
  - O modelo desta simulação segue todos os padrões de uma rede Bitcoin, portanto o Hash deve ser criado a partir de 2 SHA-256 seguidos da string mencionada acima
  - Veja [este link](https://www.oreilly.com/library/view/mastering-bitcoin/9781491902639/ch07.html) para entender melhor o desafio
  - **Caso esteja com dificuldades** para criar a Merkle Root a partir das transações, veja [este código](https://gist.github.com/Kcpf/ec3a687c23c032b5a0c6df86dc9f12ab)
- **Requests**

  - **(GET)** https://blockchainsper.herokuapp.com/ -> Devolve todos os blocos presentes na rede
  - **(GET)** https://blockchainsper.herokuapp.com/info -> Devolve informações úteis para minerar um bloco
    
  ```
    {
        "difficulty": int,
        "height": int,
        "last_hash": string,
        "valid": bool
    }

    Obs: valid indica se a rede é válida ou não
  ```
  - **(POST)** https://blockchainsper.herokuapp.com/mine -> Faz um post de um bloco e o envia para a validação

  ```
    {
        "height": int,
        "previous_hash": string,
        "merkle_root": string,
        "timestamp": float ou int,
        "difficulty": int,
        "nonce": int,
        "tx": Lista de strings
    }

    Obs: Timestamp deve estar em UNIX!
  ```

**Opcional:**

- [Material Complementar](https://github.com/BlockchainInsper/Entregaveis/blob/master/MateriaisComplementares/Consenso.md)

---
