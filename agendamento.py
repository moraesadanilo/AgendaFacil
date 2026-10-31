from dataclasses import dataclass
from datetime import date
from enum import Enum

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
    """Dado de entrada com tipo, formato ou valor inválido."""

class ConflitoDeHorarioError(AgendaError):
    """Horário indisponível."""

class AtendimentoNaoEncontradoError(AgendaError):
    """Não existe atendimento para os dados informados."""

class StatusAtendimento(Enum):
    LIVRE = "LIVRE"
    AGENDADO = "AGENDADO"
    CANCELADO = "CANCELADO"

@dataclass
class Atendimento:
    """Estrutura de dados de um atendimento.

    Attributes:
        paciente (str): Nome do paciente.
        profissional (str): Nome do profissional que realizará o atendimento.
        data (str): Data no formato AAAA-MM-DD.
        hora (int): Hora de início no formato inteiro.
        duracao (int): Duração em minutos.
        status (str): Estado atual do agendamento. O valor padrão é "LIVRE".
    """
    paciente: str
    profissional: str
    data: str
    hora: int
    duracao: int
    status: StatusAtendimento = StatusAtendimento.LIVRE


agendamentos: list[Atendimento] = []

def _validar_string(campo, valor) -> None:
    """Garante que o campo é uma string não vazia."""

    if type(valor) is not str or not valor.strip():
        raise EntradaInvalidaError(
            f"{campo} deve ser um texto não vazio, recebido: {valor!r}"
        )
 
 
def _validar_inteiro(campo, valor) -> None:
    """Garante que o campo informado é um número inteiro."""
 
    if type(valor) is not int:
        raise EntradaInvalidaError(
            f"{campo} deve ser um número inteiro, recebido: {valor!r}"
        )


def _validar_formato_data(data) -> None:
    """Valida se a data está no formato AAAA-MM-DD e existe no calendário."""
    
    try:
        valida = date.fromisoformat(data).isoformat() == data
    except (ValueError, TypeError):
        valida = False
    if not valida:
        raise EntradaInvalidaError(
            f"data deve estar no formato AAAA-MM-DD e existir no "
            f"calendário, recebido: {data!r}"
        )


def _validar_hora(hora) -> None:
    """Valida se a hora está dentro do horário de expediente."""

    _validar_inteiro("Hora", hora)

    if hora < INICIO_EXPEDIENTE or hora > ULTIMO_ATENDIMENTO:
        raise EntradaInvalidaError(
            f"{hora} está fora do horário do expediente! "
            f"Deve estar entre {INICIO_EXPEDIENTE} e {ULTIMO_ATENDIMENTO}"
        )


def _validar_atendimento_fim_expediente(hora, duracao) -> None:
    """Valida se o término do atendimento está dentro do horário de expediente."""
    # A conversão dos horários de início e fim para minutos
    # simplifica a checagem de sobreposição de intervalos.

    _validar_inteiro("Hora", hora)
    _validar_inteiro("Duração", duracao)
    
    inicio_em_minutos = hora * HORA_EM_MINUTOS
    termino_em_minutos = inicio_em_minutos + duracao
    
    if termino_em_minutos > FIM_EXPEDIENTE * HORA_EM_MINUTOS :
        raise ConflitoDeHorarioError(
            f"Atendimento às {hora}h com {duracao}min termina depois "
            f"das {FIM_EXPEDIENTE}h"
        )

    
def _validar_duracao(duracao) -> None:
    """Garante duração entre 15 e 120 minutos, em múltiplos de 15."""

    _validar_inteiro("Duração", duracao)

    if duracao <= 0:
        raise EntradaInvalidaError(
            f"Duração inválida, valor negativo.")

    if duracao % DURACAO_BASE != 0:
        raise EntradaInvalidaError(
            f"{duracao} não é multipla de {DURACAO_BASE}.")

    if duracao < DURACAO_BASE or duracao > DURACAO_MAXIMA:
        raise EntradaInvalidaError(
            f"Duração inválida: Deve ser entre {DURACAO_BASE} "
            f"e {DURACAO_MAXIMA} minutos, em múltiplos de {DURACAO_BASE}.")


def _validar_horario_agendamento(hora, duracao):
    """Valida se o agendamento está dentro das regras de horario de funcionamento"""

    _validar_hora(hora)
    _validar_duracao(duracao)
    _validar_atendimento_fim_expediente(hora, duracao)


def _verificar_disponibilidade(profissional, data, hora, duracao, ignorar=None):
    """ Impede que o profissional tenha dois atendimentos no mesmo dia e horário.

    Args:
        ignorar: atendimento a desconsiderar na checagem (usado ao editar agendamentos).
    
    Pré-condição: argumentos já validados pela camada de entrada.
    
    Nota: horários são convertidos em minutos facilitar comparação de intervalos.
    """
    
    inicio = hora * HORA_EM_MINUTOS
    fim = inicio + duracao

    for atendimento in agendamentos:
        
        if atendimento == ignorar:
            continue

        if (atendimento.data == data and atendimento.profissional == profissional):
            
            agendado_inicio = atendimento.hora * HORA_EM_MINUTOS
            agendado_fim = agendado_inicio + atendimento.duracao

            if inicio < agendado_fim and agendado_inicio < fim:
                raise ConflitoDeHorarioError(
                    f"Horario ocupado! Conflito com atendimento agendado às "
                    f"{atendimento.hora}h com duração de {atendimento.duracao} min."
                )


def adicionar_agendamento(paciente, profissional, data, hora, duracao) -> None:
    """Cria e registra um atendimento na agenda.

    Valida o formato da data, horário do expediente e conflitos
    de agenda antes de realizar a inserção.

    Args:
        paciente (str): Nome do paciente.
        profissional (str): Nome do profissional.
        data (str): Data do agendamento no formato AAAA-MM-DD.
        hora (int): Hora de início, entre 8 e 17.
        duracao (int): Duração em minutos, de 15 a 120, em múltiplos de 15.

    Returns:
        None

    Raises:
        EntradaInvalidaError: Se a data, hora ou duração forem inválidas.
        ConflitoDeHorarioError: Se o profissional já possuir atendimento no horário.
    """
    _validar_string("Paciente", paciente)
    _validar_string("Profissional", profissional)
    _validar_formato_data(data)
    _validar_horario_agendamento(hora, duracao)
    _verificar_disponibilidade(profissional, data, hora, duracao)


    novo_atendimento = Atendimento(
        paciente = paciente,
        profissional = profissional,
        data = data,
        hora = hora,
        duracao = duracao,
        status = StatusAtendimento.AGENDADO 
    )
        
    agendamentos.append(novo_atendimento)        


def buscar_agendamento(paciente, data, hora) -> Atendimento | None:
    """Busca um atendimento, caso exista retorna-o.

    Args:
        paciente (str): Nome do paciente.
        data (str): Data do agendamento no formato AAAA-MM-DD.
        hora (int): Hora de início, entre 8 e 17.

    Returns:
        Atendimento com status 'AGENDADO',
        None caso não seja encontrado.
    """
    
    for atendimento in agendamentos:
        if (atendimento.paciente == paciente and
            atendimento.data == data and
            atendimento.hora == hora and 
            atendimento.status == StatusAtendimento.AGENDADO):
            return atendimento
    return None


def remarcar_agendamento(paciente, data, hora, nova_data, nova_hora) -> None:
    """Altera nova data e/ou hora de um atendimento existente na agenda.

    Valida o formato da data, horário do expediente e conflitos
    de agenda antes de localizar o agendamento e realizar a alteração.

    Args:
        paciente (str): Nome do paciente.
        data (str): Data do agendamento atual no formato AAAA-MM-DD.
        hora (int): Hora do agendamento atual, entre 8 e 17.
        nova_data (str): Nova data do agendamento no formato AAAA-MM-DD.
        nova_hora (int): Nova hora do agendamento, entre 8 e 17.        

    Returns:
        None

    Raises:
        EntradaInvalidaError: Se a data, hora ou duração forem inválidas.
        ConflitoDeHorarioError: Se o profissional já possuir atendimento no horário.
        AtendimentoNaoEncontradoError: Se não existeir atendimento para os dados informados.
    """
    _validar_string("Paciente", paciente)
    _validar_formato_data(data)
    _validar_hora(hora)
    _validar_formato_data(nova_data)
    _validar_hora(nova_hora)

    atendimento = buscar_agendamento(paciente, data, hora)

    if atendimento is None:
        raise AtendimentoNaoEncontradoError(
            f"{paciente} não tem atendimento em {data} às {hora}h"
        )

    _validar_horario_agendamento(nova_hora, atendimento.duracao)
    _verificar_disponibilidade(atendimento.profissional,
                                nova_data, nova_hora, 
                                atendimento.duracao, ignorar=atendimento
    )

    atendimento.data = nova_data
    atendimento.hora = nova_hora  


def cancelar_agendamento(paciente, data, hora) -> None:
    """Altera o status de um atendimento na agenda para cancelado.

    Valida o formato da data, horário do expediente, antes de localizar 
    e modificar o status do agendamento em questão.
    
    Realiza a exclusão lógica do registro, alterando seu status para "CANCELADO"
    sem removê-lo dos registros, preservando o histórico de solicitações.


    Args:
        paciente (str): Nome do paciente.
        profissional (str): Nome do profissional.
        data (str): Data do agendamento no formato AAAA-MM-DD.
        hora (int): Hora de início, entre 8 e 17.
        duracao (int): Duração em minutos, de 15 a 120, em múltiplos de 15.

    Returns:
        None

    Raises:
        EntradaInvalidaError: Se a data, hora ou duração forem inválidas.
        ConflitoDeHorarioError: Se o profissional já possuir atendimento no horário.
        AtendimentoNaoEncontradoError: Se não existeir atendimento para os dados informados.    
    """
    _validar_string("Paciente", paciente)
    _validar_formato_data(data)
    _validar_hora(hora)

    atendimento = buscar_agendamento(paciente, data, hora)

    if atendimento is None:
        raise AtendimentoNaoEncontradoError(
            f"{paciente} não tem atendimento em {data} às {hora}h"
        )
    else:
        # Optou-se pela alteração de status em vez da remoção para manter a 
        # rastreabilidade e preservar o histórico de atendimentos cancelados.
        atendimento.status = StatusAtendimento.CANCELADO


def listar_agendamentos_data(data) ->list[Atendimento]:
    """Lista os atendimentos marcados em um dia, na ordem de horário.

    Esta função assume que a data fornecida já foi validada previamente
    (formato AAAA-MM-DD e existência no calendário).
 
    Args:
        data (str): Dia consultado, no formato AAAA-MM-DD.
 
    Returns:
        Lista de Atendimento do dia.
        Lista vazia se não houver nenhum atendimento no dia pesquisado.
    """
    _validar_formato_data(data)
    
    agendamentos_do_dia =[]
    for atendimento in agendamentos:
        if (atendimento.data == data and
            atendimento.status == StatusAtendimento.AGENDADO):
            agendamentos_do_dia.append(atendimento)

    return sorted(agendamentos_do_dia, key=lambda atendimento: atendimento.hora)


def relatorio_agendamentos_por_data(data) -> None:
    """Gera e exibe em tela o texto formatado com atendimentos do dia.

    Args:
        data (str): Dia consultado, no formato AAAA-MM-DD.

    Returns:
        None

    Raises:
        EntradaInvalidaError: Se a data, hora ou duração forem inválidas.
    """
 
    _validar_formato_data(data)

    agendamentos_hoje = listar_agendamentos_data(data)

    if not agendamentos_hoje:
        return f"Nenhum agendamento ativo encontrado para {data}."


    linhas = [f"--- AGENDA DO DIA {data} ---"]
    for agendamento in agendamentos_hoje:
        linhas.append(f"{agendamento.hora}h - "
                      f"Paciente: {agendamento.paciente} - "
                       f"Profissional: {agendamento.profissional}")
    
    return "\n".join(linhas)