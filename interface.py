"""Camada de apresentação da demonstração.

Traduz o resultado das operações de `agendamento` em mensagens para a console.
Só aqui existem prints e captura de exceções de AgendaError

"""
import agendamento
from agendamento import AgendaError


def _executar(mensagem_sucesso, operacao, *argumentos) -> None:
    """Executa a operação e exibe mensagem de sucesso ou o motivo da falha."""

    try:
        operacao(*argumentos)
    except AgendaError as erro:
        print(f"Operação recusada: {erro}")
    else:
        print(mensagem_sucesso)


def agendar(paciente, profissional, data, hora, duracao) -> None:
    """Agenda um atendimento e exibe o resultado no console.
 
    Args:
        paciente (str): Nome do paciente.
        profissional (str): Nome do profissional.
        data (str): Data no formato AAAA-MM-DD.
        hora (int): Hora de início, entre 8 e 17 horas.
        duracao (int): Duração em minutos, entre 15 e 120 minutos, em múltiplos de 15.
 
    Returns:
        None. O resultado do agendamento ou mensagens de erro são exibidos diretamente no console.
    """
    _executar(f"Atendimento marcado com sucesso para {paciente}",
              agendamento.adicionar_agendamento,
              paciente, profissional, data, hora, duracao)


def remarcar(paciente, data, hora, nova_data, nova_hora) -> None:
    """Remarca um atendimento e exibe o resultado no console.
 
    Args:
        paciente (str): Nome do paciente.
        data (str): Data atual do atendimento, AAAA-MM-DD.
        hora (int): Hora atual do atendimento.
        nova_data (str): Nova data, AAAA-MM-DD.
        nova_hora (int): Nova hora de início.
 
    Returns:
        None. O resultado do reagendamento ou mensagens de erro são exibidos diretamente no console.
    """

    _executar(f"Atendimento para {paciente} remarcado com sucesso",
              agendamento.remarcar_agendamento,
              paciente, data, hora, nova_data, nova_hora)


def cancelar(paciente, data, hora) -> None:
    """Cancela um atendimento e exibe o resultado no console.
 
    Args:
        paciente (str): Nome do paciente.
        data (str): Data do atendimento, AAAA-MM-DD.
        hora (int): Hora de início do atendimento.
 
    Returns:
        None. O resultado do cancelamento ou mensagens de erro são exibidos diretamente no console.
    """

    _executar(f"Atendimento para {paciente} cancelado com sucesso",
              agendamento.cancelar_agendamento,
              paciente, data, hora)


def exibir_agenda_por_data(data) -> None:
    """Exibe no console a agenda de um dia.
 
    Args:
        data (str): Dia consultado, AAAA-MM-DD.
 
    Returns:
        None. Relatótio ou mensagens de erro são exibidos diretamente no console.
    """

    try:
        print(agendamento.relatorio_agendamentos_por_data(data))
    except AgendaError as erro:
        print(f"Operação recusada: {erro}")