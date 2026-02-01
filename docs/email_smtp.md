# Configuration email (envoi réel SMTP)

Par défaut, le backend utilise `console.EmailBackend` (les emails s'affichent dans la console).

Pour activer un envoi réel, définissez les variables d'environnement suivantes avant de lancer le backend
ou créez un fichier `pfsi/backend/.env` (non versionné) :

```bat
set EMAIL_HOST=smtp.gmail.com
set EMAIL_PORT=587
set EMAIL_USE_TLS=true
set EMAIL_HOST_USER=votre.email@gmail.com
set EMAIL_HOST_PASSWORD=VOTRE_MOT_DE_PASSE_APPLICATION
set DEFAULT_FROM_EMAIL=Logistique Pro <votre.email@gmail.com>
```

Notes :
- Pour Gmail, utilisez un **mot de passe d’application** (pas votre mot de passe normal).
- `EMAIL_USE_SSL` est optionnel (défaut: `false`). Si vous utilisez SSL, mettez `EMAIL_PORT=465` et `EMAIL_USE_SSL=true`, et `EMAIL_USE_TLS=false`.
- Vous pouvez partir de `pfsi/backend/.env.example` pour créer votre `.env` local.
