from interface import agendar, remarcar, cancelar, exibir_agenda_por_data


# --- Caso base do código-base ---
agendar("Ana", "Dr. Silva", "2026-10-05", 9, 30)       # ok
agendar("Bruno", "Dr. Silva", "2026-10-05", 9, 30)     # conflito (mesmo horário)
agendar("Carla", "Dra. Souza", "2026-10-05", 14, 60)   # ok
remarcar("Ana", "2026-10-05", 9, "2026-10-06", 10)     # ok

print("\n")
exibir_agenda_por_data("2026-10-05")


# --- Testes extras: cada chamada exercita uma regra da Etapa 4 ---
print("\n--- TESTES EXTRAS (PROGRAMAÇÃO DEFENSIVA) ---")

print("\n[Expediente]")
agendar("Fábio", "Dr. Silva", "2026-10-08", 20, 30)    # recusa: início após as 17h
agendar("Fábio", "Dr. Silva", "2026-10-08", 7, 30)     # recusa: início antes das 8h
agendar("Fábio", "Dr. Silva", "2026-10-08", 17, 120)   # recusa: terminaria às 19h

print("\n[Duração]")
agendar("Gabi", "Dr. Silva", "2026-10-08", 9, 0)       # recusa: abaixo de 15 min
agendar("Gabi", "Dr. Silva", "2026-10-08", 9, 20)      # recusa: não é múltiplo de 15
agendar("Gabi", "Dr. Silva", "2026-10-08", 9, 150)     # recusa: acima de 120 min

print("\n[Data]")
agendar("Hugo", "Dr. Silva", "2026-02-30", 9, 30)      # recusa: data inexistente
agendar("Hugo", "Dr. Silva", "05/10/2026", 9, 30)      # recusa: formato errado

print("\n[Tipos e textos vazios]")
agendar("Hugo", "Dr. Silva", "2026-10-08", "9", 30)    # recusa: hora é texto
agendar("Hugo", "Dr. Silva", "2026-10-08", 9.5, 30)    # recusa: hora não é inteira
agendar("", "Dr. Silva", "2026-10-08", 9, 30)          # recusa: paciente vazio
agendar("Hugo", None, "2026-10-08", 9, 30)             # recusa: profissional nulo

print("\n[Conflito por sobreposição]")
agendar("Iara", "Dr. Lima", "2026-10-09", 9, 120)      # ok: 9h às 11h
agendar("Joel", "Dr. Lima", "2026-10-09", 10, 30)      # recusa: sobrepõe 9h às 11h
agendar("Joel", "Dra. Souza", "2026-10-09", 10, 30)    # ok: outro profissional

print("\n[Remarcação e cancelamento]")
remarcar("Iara", "2026-10-09", 9, "2026-10-09", 20)    # recusa: nova hora inválida
remarcar("Zeca", "2026-10-09", 9, "2026-10-10", 9)     # recusa: atendimento inexistente
cancelar("Zeca", "2026-10-09", 9)                      # recusa: atendimento inexistente
cancelar("Iara", "2026-10-09", 9)                      # ok
agendar("Joel", "Dr. Lima", "2026-10-09", 10, 30)      # ok: horário cancelado foi liberado

print("\n[Relatório]")
exibir_agenda_por_data("2026/10/09")                   # recusa: data fora do formato
exibir_agenda_por_data("2026-10-09")                   # ok
exibir_agenda_por_data("2026-10-30")                   # ok: dia sem atendimentos
