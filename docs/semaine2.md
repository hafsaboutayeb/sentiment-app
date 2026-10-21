# Analyse des erreurs du modèle de sentiment (TP2)

Le modèle commet 7 erreurs sur 58 avis, et toutes portent sur des avis mitigés (contenant des retournements comme "sauf que ensuite").
Cela s'explique par le fait que le modèle "sac de mots" (TF-IDF) compte les mots positifs et négatifs sans tenir compte de leur ordre, il ne voit donc pas le retournement de situation.
Pour corriger cela, il faudrait utiliser des embeddings de mots (comme Word2Vec ou les transformers de la semaine 9) qui capturent le contexte et l'ordre des mots.

