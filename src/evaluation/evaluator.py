


def evaluate(student_answer_path, dataset_path, k, max_context_length):
    


# fonction evaluate(student_answer_path, dataset_path, k, max_context_length):

#     1. charger les résultats du student (ton output)
#     2. charger le dataset annoté (les bonnes réponses)

#     3. pour chaque question :
#            récupérer les sources correctes (ground truth)
#            récupérer tes sources retrieved
           
#            pour chaque source correcte :
#                est-ce qu'une de tes sources a au moins 5% d'overlap ?
#                → oui : found + 1
           
#            score_question = found / total_sources_correctes

#     4. recall@k = moyenne des scores sur toutes les questions
#     5. afficher les résultats