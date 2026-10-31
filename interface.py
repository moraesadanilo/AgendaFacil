"""Camada de apresentação da demonstração.

Traduz o resultado das operações de `agenda` em mensagens para o console.
Só aqui existem prints e captura de exceções de AgendaError

"""
import agendamento
from agendamento import AgendaError


def _executar(mensagem_sucesso, operacao, *argumentos) -> None:
    """Executa a operação e exibe mensagem de sucesso ou o motivo da falha."""

    try:
        operacao(*argumentos)
    except AgendaError as erro:
        print(f"Agendamento recusada: {erro}")
    else:
        print(mensagem_sucesso)


def agendar(paciente, profissional, data, hora, duracao) -> None:
    _executar(f"Atendimento marcado com sucesso para {paciente}",
              agendamento.adicionar_agendamento,
              paciente, profissional, data, hora, duracao)


def remarcar(paciente, data, hora, nova_data, nova_hora) -> None:
    _executar(f"Atendimento para {paciente} remarcado com sucesso",
              agendamento.remarcar_agendamento,
              paciente, data, hora, nova_data, nova_hora)


def cancelar(paciente, data, hora) -> None:
    _executar(f"Atendimento para {paciente} cancelado com sucesso",
              agendamento.cancelar_agendamento,
              paciente, data, hora)


def exibir_agenda_por_data(data) -> None:
    try:
        print(agendamento.relatorio_agendamentos_por_data(data))
    except AgendaError as erro:
        print(f"Operação recusada: {erro}")