from dataclasses import dataclass
from datetime import date

HORA_EM_MINUTOS = 60
INICIO_EXPEDIENTE = 8
FIM_EXPEDIENTE = 18
ULTIMO_ATENDIMENTO = 17
DURACAO_ATENDIMENTO = 15
DURACAO_BASE = 15
DURACAO_MAXIMA = 120


class AgendaError(Exception):
    """Base para os erros do sistema de agenda."""

class EntradaInvalidaError(AgendaError, ValueError):
    """Entrada de dados inválidos."""

class ConflitoDeHorarioError(AgendaError):
    """Horário indisponível."""


# 1. Definição do tipo para o atendimento, substituindo as listas por índices
@dataclass
class Atendimento:
    paciente: str
    profissional: str
    data: str
    hora: int
    duracao: int
    status: str = "LIVRE"



# Lista global temporária 
agendamentos: list[Atendimento] = []


def validar_formato_data(data):
    try:
        valida = date.fromisoformat(data).isoformat() == data
    except (ValueError, TypeError):
        valida = False
    if not valida:
        raise EntradaInvalidaError(
            f"data deve estar no formato AAAA-MM-DD e existir no "
            f"calendário, recebido: {data!r}"
        )


def validar_hora(hora):
        if hora < INICIO_EXPEDIENTE or hora > ULTIMO_ATENDIMENTO:
            raise EntradaInvalidaError(
                f"{hora} está fora do horário do expediente.")


def verificar_disponibilidade(profissional, data, hora, duracao):
    """Impede que o profissional tenha dois atendimentos no mesmo dia e horário."""
    
    inicio = hora * HORA_EM_MINUTOS
    fim = inicio + duracao

    for atendimento in agendamentos:
        if (atendimento.data == data and atendimento.profissional == profissional):
            
            agendado_inicio = atendimento.hora * HORA_EM_MINUTOS
            agendado_fim = agendado_inicio + atendimento.duracao

            if inicio < agendado_fim and agendado_inicio < fim:
                raise ValueError(f"Horario ocupado! Conflito com atendimento agendado às "
                                 f"{atendimento.hora}h com duração de {atendimento.duracao} min."
                                 )


def validar_atendimento_fim_expediente(hora, duracao):
    """Valida se o término do atendimento está dentro do expediente."""
    
    inicio_em_minutos = hora * HORA_EM_MINUTOS
    termino_em_minutos = inicio_em_minutos + duracao
    
    if termino_em_minutos > FIM_EXPEDIENTE * HORA_EM_MINUTOS :
        return False


def validar_horario_agendamento(hora, duracao):
    """Valida as regras de horario de funcionamento"""
  
    if duracao <= 0:
        raise EntradaInvalidaError(
            f"Duração inválida, valor negativo.")

    if duracao % DURACAO_BASE != 0:
        raise EntradaInvalidaError(
            f"{duracao} não é multipla de {DURACAO_BASE}.")

    if duracao < DURACAO_BASE or duracao > DURACAO_MAXIMA:
        raise ValueError(f"Duração inválida: Deve ser entre {DURACAO_BASE} "
                         f"e {DURACAO_MAXIMA} minutos, em múltiplos de {DURACAO_BASE}.")

    if validar_atendimento_fim_expediente(hora, duracao) is False:
        raise ValueError(
            f"Horário fora do expediente: Duração de {duracao} min "
            f"ultrapassa o horário de funcionamento."
        )
    
    
    return True


def adicionar_agendamento(paciente, profissional, data, hora, duracao):
    try: 
        validar_formato_data(data)
        validar_hora(hora)
        validar_horario_agendamento(hora, duracao)
        verificar_disponibilidade(profissional, data, hora, duracao)

    except ConflitoDeHorarioError as erro:
        print(f"Agendamento recusado para {paciente}: {erro}")
    except ValueError as erro:
        print(f"Dados inválidos para {paciente}: {erro}")

    else:
        novo_atendimento = Atendimento(
            paciente = paciente,
            profissional = profissional,
            data = data,
            hora = hora,
            duracao = duracao,
            status = "AGENDADO"
        )
        
        agendamentos.append(novo_atendimento)
        print("Atendimento marcado com sucesso para", paciente)


def buscar_agendamento(paciente, data, hora):
    for atendimento in agendamentos:
        if (atendimento.paciente == paciente and
            atendimento.data == data and
            atendimento.hora == hora and 
            atendimento.status == "AGENDADO"):
            return atendimento
    return None



def remarcar_agendamento(paciente, data, hora, nova_data, nova_hora):

    try: 
        validar_formato_data(data)
        validar_hora(hora)
        validar_formato_data(nova_data)
        validar_hora(nova_hora)
    except ValueError as erro:
        print(f"Dados inválidos: {erro}")
        return None

    atendimento = buscar_agendamento(paciente, data, hora)

    if atendimento is None:
        raise AgendaError(
            f"{paciente} não tem atendimento em {data} às {hora}h"
        )

    try: 
        validar_horario_agendamento(hora, atendimento.duracao)
        verificar_disponibilidade(atendimento.profissional, nova_data, nova_hora, atendimento.duracao)
    
    except ConflitoDeHorarioError as erro:
        print(f"Agendamento recusado para {paciente}: {erro}")
        return None


    else: 
        atendimento.data = nova_data
        atendimento.hora = nova_hora
        print(f"Atendimento para {paciente} remarcado com sucesso!")


def cancelar_agendamento(paciente, data, hora):

    try: 
        validar_formato_data(data)
        validar_hora(hora)

    except ValueError as erro:
        print(f"Dados inválidos: {erro}")
        return None

    atendimento = buscar_agendamento(paciente, data, hora)

    if atendimento is None:
        raise AgendaError(
            f"{paciente} não tem atendimento em {data} às {hora}h"
        )
    else:
        atendimento.status = "CANCELADO"
        print(f"Atendimento para {paciente} cancelado com sucesso!")


def listar_agendamentos_data(data) ->list[Atendimento]:
    
    agendamentos_do_dia =[]
    for atendimento in agendamentos:
        if (atendimento.data == data and
            atendimento.status == "AGENDADO"):
            agendamentos_do_dia.append(atendimento)

    return sorted(agendamentos_do_dia, key=lambda atendimento: atendimento.hora)


def relatorio_agendamentos_por_data(data):

    try: 
        validar_formato_data(data)

    except ValueError as erro:
        print(f"Dados inválidos: {erro}")
        return None

    agendamentos_hoje = listar_agendamentos_data(data)

    if not agendamentos_hoje:
        print(f"Nenhum agendamento ativo encontrado para {data}.")
    else:
        print(f"--- AGENDA DO DIA {data} ---")
        for agendamento in agendamentos_hoje:
            print(f"{agendamento.hora}h - " 
                  f"Paciente: {agendamento.paciente} - "
                  f"Profissional: {agendamento.profissional}")
        