# MRV SCRAPPER

Este _script_ tem a finalidade de **raspar**, **baixar** e **salvar** localmente todas as novas fotos do **andamento de obra** disponíveis no [**Portal Meu Apê da MRV**](https://meuape.mrv.com.br/).

![login-page](https://user-images.githubusercontent.com/47225177/188993864-186ca967-dd06-44b7-91dd-722d1a05db61.png)

Caso você também tenha um apartamento sendo construído pela MRV e acompanha as fotos do andamento da obra, pode usar esse projeto para acessar o seu perfil.

## Como usar?

- Clone ou faça o [download](https://github.com/ramongss/mrv_scrapper/archive/refs/heads/main.zip) deste projeto na sua máquina:

```bash
git clone git@github.com:ramongss/mrv_scrapper.git
```

- Acesse a pasta criada, crie um ambiente de desenvolvimento, e instale as dependências no seu projeto:

```bash
cd mrv_scrapper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Crie um arquivo `.secrets` com o seguinte formato:

```yml
username SeuUsuario
password SuaSenha
```

- Execute o _script_:

```bash
python3 scrapper.py
```

## Como funciona?

Com isso, o _script_ irá acessar o seu perfil do **Portal Meu Apê**, realizar o login e acessar a _homepage_:

![homepage](https://user-images.githubusercontent.com/47225177/188995648-59c99421-0ce7-424d-9418-90d9c0702c8a.png)

Logo em seguida, ele acessa a aba **Acompanhe sua obra** na aba lateral e percorre por cada uma das fases da obra:

![acompanhe](https://user-images.githubusercontent.com/47225177/188995936-b0772e17-1f6e-4f3d-ae94-866c57304a7a.png)

![fases](https://user-images.githubusercontent.com/47225177/188996107-11be07b4-9a70-4552-a88a-874963ad1479.png)

O _script_ vai então raspando todas as abas, colhendo as urls das fotos disponibilizadas e realizando o _download_ localmente conforme a estrutura de pastas presente no projeto.

Ao final, todas as fotos disponíveis no momento da execução do _script_ estarão salvas no seu computador. Caso queira executar novamente, a função vai verificar a existência das fotos no seu computador e realizar o download apenas de novas fotos.

## O que melhorar?

- [ ] Criar uma imagem `docker` para execução da tarefa via _cronjob_.