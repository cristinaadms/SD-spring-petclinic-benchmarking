# spring-petclinic-benchmarking
Avaliação de desempenho da aplicação Spring PetClinic (microsserviços) utilizando Locust.

## Pré-requisitos
- Docker e Docker Compose instalados
- Python 3.10+ (opcional, apenas para análise)
- Locust (se for rodar localmente): `pip install locust`

## Como rodar os microsserviços
```bash
docker compose up -d
# Para parar:
# docker compose down
```

## Como executar o Locust
```bash
locust -f locustfile.py
# UI (padrão): http://localhost:8089
```

## Script de teste
```bash
chmod +x ./script.sh
./script.sh
```

## Análise de resultados (opcional)
Gera gráficos e tabelas a partir de CSVs no diretório `results/`:
```bash
python3 analisar_resultados.py
```
Saídas (exemplos):
- PNG: grafico_sucesso_falhas.png, grafico_taxa_falhas.png, grafico_tempos_resposta.png, grafico_throughput.png, grafico_throughput2.png, grafico_percentis_latencia.png, ...
- CSV: resumo_metricas.csv, tabela_percentis.csv, tabela_estabilidade.csv, resumo_executivo.csv, ...

## Acesso ao PDF
Para acessar o PDF do relatório, recomenda-se clonar este repositório:
```bash
git clone <URL_DO_REPOSITORIO>
cd SD-spring-petclinic-benchmarking
```
Depois, abra o arquivo PDF dentro do repositório (`artigo/ArtigoFinal.pdf`).

## Vídeo explicativo
[Vídeo explicativo](COLOQUE_O_LINK_AQUI)

