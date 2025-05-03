# Clicker Game - Flask + Tailwind

## 🎮 Description

Un petit jeu de type *Clicker Game* où le joueur clique pour augmenter son score. Le score est enregistré dans la session Flask (cookies côté client).

## 🚀 Fonctionnement

- La page principale affiche le score et un bouton "Click Me!".
- À chaque clic, un POST est envoyé à `/click`, le score est incrémenté, puis redirection vers `/`.
- Un lien "Reset" permet de remettre le score à zéro via `/reset`.
---