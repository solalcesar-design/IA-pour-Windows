🤖 WinAssistant - IA Locale & Contrôle Windows
WinAssistant est un assistant vocal intelligent conçu pour fonctionner à 100% en local. Il permet de piloter Windows à la voix ou par texte tout en discutant avec une IA puissante (Llama 3.2), sans jamais envoyer vos données sur le cloud.

✨ Fonctionnalités principales :
🧠 IA 100% Locale : Utilise Ollama (modèle Llama 3.2:1b) pour répondre à vos questions.

🛡️ Respect de la vie privée : Aucune clé API requise, pas de dépendance aux serveurs Google.

🎮 Optimisé pour le Gaming : S'active uniquement sur demande pour ne pas consommer de ressources en jeu.

💻 Contrôle Système : Éteindre, redémarrer, déconnecter ou verrouiller le PC à la voix.

🌐 Recherche Web : Capable de trouver des liens vidéos (ex: Fuze III) ou des infos sur le web si besoin.

💾 Mémoire : Se souvient de vos préférences et de l'historique de la conversation.

🚀 Installation :
Installer Python : Téléchargez la dernière version sur python.org.

Installer Ollama : Téléchargez-le sur ollama.com et lancez la commande :

Bash
ollama run llama3.2:1b
Cloner le projet et installer les dépendances :

Bash
pip install -r requirements.txt
Lancer l'assistant :

Bash
python assistant.py

PS : si vous voulez mettre un logo metait un logo au format ico qui se nome logo.ico

🗣️ Exemples de commandes :
"Assistant, verrouille l'ordinateur"


"Assistant, quel est le meilleur build sur Elden Ring ?" (Réponse par l'IA locale)

"Assistant, éteins le PC"
