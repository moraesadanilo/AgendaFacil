from interface import agendar, remarcar, cancelar, exibir_agenda_por_data


agendar("Ana", "Dr. Silva", "2026-10-05", 9, 30)
agendar("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
agendar("Carla", "Dra. Souza", "2026-10-05", 14, 60)
remarcar("Ana", "2026-10-05", 9, "2026-10-06", 10)
 
print("\n")
exibir_agenda_por_data("2026-10-05")