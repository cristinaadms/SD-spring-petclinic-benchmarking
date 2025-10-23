#!/bin/bash
# ============================================================
# Script de execução automática dos 3 cenários do Locust
# para o Spring PetClinic Microservices.
# ============================================================

# Configurações gerais
LOCUST_FILE="locustfile.py"
HOST="http://localhost:8081"   # Pode trocar pelo gateway (http://localhost:8080) se quiser
WAIT_AFTER_STOP=20             # Tempo antes de desligar o PC (em segundos)

# ============================================================
# Função auxiliar para rodar cenário
# ============================================================
run_scenario() {
    local USERS=$1
    local SPAWN_RATE=$2
    local DURATION=$3
    local CSV_NAME=$4
    echo "🚀 Iniciando cenário: $CSV_NAME"
    echo "Usuários: $USERS | Spawn rate: $SPAWN_RATE | Duração: $DURATION"

    locust -f $LOCUST_FILE --headless \
      -u $USERS -r $SPAWN_RATE -t $DURATION \
      --csv=$CSV_NAME --host=$HOST

    echo "✅ Cenário $CSV_NAME finalizado!"
    echo "------------------------------------------"
}

# ============================================================
# 1️⃣ Cenário Leve
# ============================================================
run_scenario 20 5 10m res1

# ============================================================
# 2️⃣ Cenário Moderado
# ============================================================
run_scenario 50 5 10m res2

# ============================================================
# 3️⃣ Cenário Pico
# ============================================================
run_scenario 200 10 5m res3

# ============================================================
# Finalização
# # ============================================================

# echo "🧹 Finalizando containers Docker..."
# docker compose -f ./spring-petclinic-microservices/docker-compose.yml down

# echo "⏳ Aguardando $WAIT_AFTER_STOP segundos antes de desligar..."
# sleep $WAIT_AFTER_STOP

# echo "💻 Desligando o computador..."
# sudo shutdown now