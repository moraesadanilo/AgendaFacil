import agenda



print("--- Cenário principal ---")
agenda.adicionar_agendamento("Ana", "Dr. Silva",  "2026-10-05", 9, 30)   # ok
agenda.adicionar_agendamento("Bruno", "Dr. Silva",  "2026-10-05", 9, 30)   # conflito (mesmo horário)
agenda.adicionar_agendamento("Carla", "Dra. Souza", "2026-10-05", 14, 60)  # ok
agenda.remarcar_agendamento("Ana", "2026-out-15", 9, "2026-10-06", 10)      #erro data fica o antigo
agenda.adicionar_agendamento("Bruno", "Dr. Silva",  "2026-10-05", 10, 15)  #ok
agenda.adicionar_agendamento("Paulo", "Dr. Silva",  "2026-10-05", 11, 15)  #ok 
agenda.cancelar_agendamento("Paulo", "2026-10-05", 11)                     #desmarca sai da lista



agenda.relatorio_agendamentos_por_data("2026-10-05")