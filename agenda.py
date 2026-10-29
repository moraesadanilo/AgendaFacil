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

    if hora < INICIO_EXPEDIENTE or hora > ULTIMO_ATENDIMENTO:
        raise EntradaInvalidaError(
            f"{hora} está fora do horário do expediente.")

    if validar_atendimento_fim_expediente(hora, duracao) is False:
        raise ValueError(
            f"Horário fora do expediente: Duração de {duracao} min "
            f"ultrapassa o horário de funcionamento."
        )
    
    
    return True


def adicionar_agenda(paciente, profissional, data, hora, duracao):
    try: 
        validar_formato_data(data)
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
            status = "MARCADO"
        )
        
        agendamentos.append(novo_atendimento)
        print("Atendimento marcado com sucesso para", paciente)

def buscar_agendamento(paciente, data, hora):
    for atendimento in agendamentos:
        if (atendimento.paciente == paciente,
            atendimento.data == data,
            atendimento.hora == hora):
            return atendimento
    return None
    
def remarcar_agenda(paciente, data, hora, nova_data, nova_hora):

    try: 
        validar_formato_data(data)
        #TODO validar_hora(hora)
        validar_formato_data(nova_data)
        #TODO validar_hora(nova_hora)
    except ValueError as erro:
        print(f"Dados inválidos: {erro}")

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


    else: 
        atendimento.data = nova_data
        atendimento.hora = nova_hora
        print(f"Atendimento para {paciente} remarcado com sucesso!")



"""
# def desmarcar(p, d, h):
#     ag.remove(...)




def lst(d):
    # lista os atendimentos do mes
    for a in ag:
        if a[2] == d:
            print(a[3], a[0], a[1], a[5])


add("Ana", "Dr. Silva", "2026-10-05", 9, 30)
add("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
add("Carla", "Dra. Souza", "2026-10-05", 14, 60)

lst("2026-10-05")
"""

if __name__ == "__main__":
    print("--- Cenário principal ---")
    adicionar_agenda("Ana",   "Dr. Silva",  "2026-10-05", 9, 30)   # ok
    #adicionar_agenda("Bruno", "Dr. Silva",  "2026-10-05", 9, 30)   # ❌ conflito (mesmo horário)
    #adicionar_agenda("Carla", "Dra. Souza", "2026-10-05", 14, 60)  # ok
    remarcar_agenda("Ana", "2026-10-15", 9, "2026-10-06", 10)