#!/usr/bin/env python3
"""
Script para adicionar dados adicionais ao banco de dados
Inclui: tipos de ausência, turnos, feriados e eventos de exemplo
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database.models import init_db
from api.database.crud import (
    criar_tipo_ausencia, listar_tipos_ausencia,
    criar_turno, listar_turnos,
    criar_feriado_nacional, criar_feriado_estadual,
    criar_evento, listar_usuarios,
)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def seed_tipos_ausencia():
    """Cria tipos de ausência padrão"""
    logging.info("📋 Criando tipos de ausência...")
    
    tipos_ausencia = [
        {"descricao": "Férias", "usa_turno": False},
        {"descricao": "Licença Médica", "usa_turno": False},
        {"descricao": "Licença Maternidade", "usa_turno": False},
        {"descricao": "Licença Paternidade", "usa_turno": False},
        {"descricao": "Falta Justificada", "usa_turno": True},
        {"descricao": "Falta Injustificada", "usa_turno": True},
        {"descricao": "Abono", "usa_turno": True},
        {"descricao": "Compensação", "usa_turno": True},
        {"descricao": "Home Office", "usa_turno": False},
        {"descricao": "Treinamento", "usa_turno": False}
    ]
    
    tipos_existentes = listar_tipos_ausencia()
    descricoes_existentes = {tipo.descricao_ausencia for tipo in tipos_existentes}
    
    criados = 0
    for tipo_data in tipos_ausencia:
        try:
            if tipo_data["descricao"] not in descricoes_existentes:
                tipo = criar_tipo_ausencia(
                    descricao_ausencia=tipo_data["descricao"],
                    usa_turno=tipo_data["usa_turno"]
                )
                logging.info(f"✅ Tipo de ausência criado: {tipo.descricao_ausencia}")
                criados += 1
            else:
                logging.info(f"ℹ️ Tipo de ausência já existe: {tipo_data['descricao']}")
        except Exception as e:
            logging.error(f"❌ Erro ao criar tipo de ausência {tipo_data['descricao']}: {e}")
    
    logging.info(f"✅ Tipos de ausência processados: {len(tipos_ausencia)} (criados: {criados})")

def seed_turnos():
    """Cria turnos padrão"""
    logging.info("⏰ Criando turnos...")
    
    turnos = [
        "Manhã",
        "Tarde", 
        "Noite",
        "Integral",
        "Meio Período"
    ]
    
    turnos_existentes = listar_turnos()
    descricoes_existentes = {turno.descricao_ausencia for turno in turnos_existentes}
    
    criados = 0
    for turno_desc in turnos:
        try:
            if turno_desc not in descricoes_existentes:
                turno = criar_turno(descricao_ausencia=turno_desc)
                logging.info(f"✅ Turno criado: {turno.descricao_ausencia}")
                criados += 1
            else:
                logging.info(f"ℹ️ Turno já existe: {turno_desc}")
        except Exception as e:
            logging.error(f"❌ Erro ao criar turno {turno_desc}: {e}")
    
    logging.info(f"✅ Turnos processados: {len(turnos)} (criados: {criados})")

def seed_feriados_2025():
    """Cria feriados nacionais e estaduais para 2025"""
    logging.info("🎉 Criando feriados de 2025...")
    
    # Feriados nacionais 2025
    feriados_nacionais = [
        {"data": "2025-01-01", "descricao": "Confraternização Universal"},
        {"data": "2025-04-18", "descricao": "Sexta-feira Santa"},
        {"data": "2025-04-21", "descricao": "Tiradentes"},
        {"data": "2025-05-01", "descricao": "Dia do Trabalhador"},
        {"data": "2025-09-07", "descricao": "Independência do Brasil"},
        {"data": "2025-10-12", "descricao": "Nossa Senhora Aparecida"},
        {"data": "2025-11-02", "descricao": "Finados"},
        {"data": "2025-11-15", "descricao": "Proclamação da República"},
        {"data": "2025-12-25", "descricao": "Natal"}
    ]
    
    # Feriados estaduais de SP
    feriados_sp = [
        {"data": "2025-02-17", "descricao": "Carnaval - Segunda-feira"},
        {"data": "2025-02-18", "descricao": "Carnaval - Terça-feira"},
        {"data": "2025-06-19", "descricao": "Corpus Christi"},
        {"data": "2025-07-09", "descricao": "Revolução Constitucionalista"}
    ]
    
    criados_nacionais = 0
    criados_estaduais = 0
    
    # Criar feriados nacionais para SP
    for feriado in feriados_nacionais:
        try:
            criar_feriado_nacional(
                data_feriado=feriado["data"],
                uf="SP",
                descricao_feriado=feriado["descricao"]
            )
            logging.info(f"✅ Feriado nacional criado: {feriado['descricao']} ({feriado['data']})")
            criados_nacionais += 1
        except Exception as e:
            if "Duplicate entry" in str(e):
                logging.info(f"ℹ️ Feriado nacional já existe: {feriado['descricao']}")
            else:
                logging.error(f"❌ Erro ao criar feriado nacional {feriado['descricao']}: {e}")
    
    # Criar feriados estaduais de SP
    for feriado in feriados_sp:
        try:
            criar_feriado_estadual(
                data_feriado=feriado["data"],
                uf="SP",
                descricao_feriado=feriado["descricao"]
            )
            logging.info(f"✅ Feriado estadual criado: {feriado['descricao']} ({feriado['data']})")
            criados_estaduais += 1
        except Exception as e:
            if "Duplicate entry" in str(e):
                logging.info(f"ℹ️ Feriado estadual já existe: {feriado['descricao']}")
            else:
                logging.error(f"❌ Erro ao criar feriado estadual {feriado['descricao']}: {e}")
    
    logging.info(f"✅ Feriados processados: {len(feriados_nacionais)} nacionais (criados: {criados_nacionais}), {len(feriados_sp)} estaduais (criados: {criados_estaduais})")

def seed_eventos_exemplo():
    """Cria eventos de exemplo"""
    logging.info("📅 Criando eventos de exemplo...")
    
    # Busca usuários existentes
    usuarios = listar_usuarios()
    if len(usuarios) < 2:
        logging.warning("⚠️ Poucos usuários encontrados. Pulando criação de eventos.")
        return
    
    # Busca tipos de ausência
    tipos_ausencia = listar_tipos_ausencia()
    if not tipos_ausencia:
        logging.warning("⚠️ Nenhum tipo de ausência encontrado. Pulando criação de eventos.")
        return
    
    # Pega o primeiro usuário como solicitante e o segundo como aprovador
    usuario_solicitante = usuarios[0]
    usuario_aprovador = usuarios[1] if len(usuarios) > 1 else usuarios[0]
    tipo_ferias = next((t for t in tipos_ausencia if "Férias" in t.descricao_ausencia), tipos_ausencia[0])
    
    # Eventos de exemplo
    eventos_exemplo = [
        {
            "cpf_usuario": usuario_solicitante.cpf,
            "data_inicio": "2025-07-01",
            "data_fim": "2025-07-15",
            "id_tipo_ausencia": tipo_ferias.id_tipo_ausencia,
            "uf": usuario_solicitante.UF,
            "aprovado_por": usuario_aprovador.cpf
        },
        {
            "cpf_usuario": usuario_solicitante.cpf,
            "data_inicio": "2025-12-23",
            "data_fim": "2025-12-30",
            "id_tipo_ausencia": tipo_ferias.id_tipo_ausencia,
            "uf": usuario_solicitante.UF,
            "aprovado_por": usuario_aprovador.cpf
        }
    ]
    
    criados = 0
    for evento_data in eventos_exemplo:
        try:
            evento = criar_evento(**evento_data)
            logging.info(f"✅ Evento criado: {evento_data['data_inicio']} a {evento_data['data_fim']}")
            criados += 1
        except Exception as e:
            logging.error(f"❌ Erro ao criar evento: {e}")
    
    logging.info(f"✅ Eventos processados: {len(eventos_exemplo)} (criados: {criados})")

def main():
    """Função principal"""
    print("\n" + "="*50)
    print("🌱 SEED DE DADOS ADICIONAIS")
    print("="*50)
    
    # Carrega variáveis de ambiente
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logging.info(f"✅ Arquivo .env carregado: {env_path}")
    else:
        logging.warning("⚠️ Arquivo .env não encontrado")
    
    # Conecta ao banco
    try:
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            logging.info("🚀 Conectando ao MySQL...")
            host = database_url.split('@')[1].split(':')[0] if '@' in database_url else 'localhost'
            database = database_url.split('/')[-1] if '/' in database_url else 'tooff_app'
            logging.info(f"📊 Host: {host}")
            logging.info(f"🗄️ Database: {database}")
        
        init_db(database_url)
        logging.info("✅ Conexão com o banco de dados estabelecida com sucesso!")
        
    except Exception as e:
        logging.error(f"❌ Erro ao conectar com o banco: {e}")
        return
    
    # Executa seeds
    try:
        logging.info("🌱 Iniciando seed de dados adicionais...")
        
        seed_tipos_ausencia()
        seed_turnos()
        seed_feriados_2025()
        seed_eventos_exemplo()
        
        logging.info("\n" + "="*50)
        logging.info("📊 RESUMO DO SEED ADICIONAL:")
        logging.info("📋 Tipos de Ausência: Férias, Licenças, Faltas, etc.")
        logging.info("⏰ Turnos: Manhã, Tarde, Noite, Integral")
        logging.info("🎉 Feriados: Nacionais e Estaduais de 2025")
        logging.info("📅 Eventos: Exemplos de férias")
        logging.info("="*50)
        logging.info("✅ Seed adicional concluído com sucesso!")
        
    except Exception as e:
        logging.error(f"❌ Erro durante o seed: {e}")
        return
    
    print("\n" + "="*50)
    print("✅ SEED ADICIONAL CONCLUÍDO COM SUCESSO!")
    print("="*50)
    print("\n=== DADOS ADICIONAIS CRIADOS ===")
    print("📋 Tipos de Ausência: 10 tipos padrão")
    print("⏰ Turnos: 5 turnos padrão")
    print("🎉 Feriados: Calendário 2025 completo")
    print("📅 Eventos: Exemplos de solicitações")
    print("="*50)

if __name__ == "__main__":
    main()
