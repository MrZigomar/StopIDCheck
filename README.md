# StopIDCheck
# Cahier des charges – Outil de référencement des sites à vérification d’identité (et alternatives sans vérification)
# Contexte et problématique

Depuis l’apparition de nouvelles législations dans plusieurs pays, certains utilisateurs se voient obligés de prouver leur majorité pour accéder à du contenu en ligne dit « mature » (pornographie, contenus violents, jeux d’argent, etc.). Ces lois – adoptées par exemple en France, au Royaume-Uni ou dans certains États américains – exigent que les sites web vérifient l’âge de leurs visiteurs majeurs sous peine de sanctions. Les méthodes de vérification imposées sont souvent intrusives, allant du téléversement d’une pièce d’identité au scan facial via une IA
politico.eu
. Par exemple, une loi française entrée en vigueur en 2025 oblige les sites pornographiques à mettre en place un contrôle d’âge « sécurisé », via un selfie vidéo analysé par IA ou via la vérification d’une carte d’identité, sous peine de blocage par le régulateur
politico.eu
. De même, au Royaume-Uni, l’Online Safety Act pousse des plateformes populaires (réseaux sociaux, forums, etc.) à déployer des systèmes de vérification d’âge utilisant des prestataires tiers (scan de pièce d’identité, estimation d’âge par reconnaissance faciale, vérification par carte bancaire, etc.)
tomsguide.com
tomsguide.com
.

Cette évolution, bien qu’ayant pour but la protection des mineurs, suscite de vives inquiétudes en matière de vie privée et de libertés numériques. De nombreux internautes majeurs sont réticents à fournir des documents d’identité ou des données biométriques pour naviguer sur Internet
tomsguide.com
tomsguide.com
. Des experts en cybersécurité et des associations de défense des droits numériques soulignent les risques potentiels : fuite de données sensibles, surveillance accrue, atteinte à l’anonymat en ligne, etc. Les grandes plateformes elles-mêmes sont divisées – certaines se conforment aux exigences légales, tandis que d’autres préfèrent refuser ces contrôles quitte à perdre des utilisateurs dans certaines régions. Par exemple, en France le groupe Aylo (Pornhub, YouPorn, Redtube) a bloqué l’accès à ses sites pour les internautes français afin de protester contre l’obligation de vérification d’âge instaurée par la loi de 2024
tf1info.fr
tf1info.fr
. De même, Pornhub a adopté une démarche similaire dans l’État américain de l’Utah, en désactivant son site localement plutôt que d’imposer une identification à ses visiteurs
apnews.com
. Ces réactions montrent qu’une partie de l’industrie préfère perdre une partie de son audience plutôt que d’imposer des mesures jugées intrusives.

Toutefois, de nombreux sites ont choisi de se conformer aux nouvelles règles. On observe l’apparition de vérifications d’âge dans tous les secteurs :

    Sites pour adultes (pornographiques) – Plusieurs grands sites pornographiques gratuits résistent encore (préférant le blocage géographique), mais certains acteurs « bons élèves » se sont mis en conformité. Par exemple, le site français Dorcel (contenu pour adultes payant) a intégré dès 2025 la solution de vérification d’âge de Yoti (estimation d’âge par IA ou vérification d’identité)
    politico.eu
    . D’autres sites X ont testé diverses solutions de contrôle d’âge en prévision des lois
    politico.eu
    .

    Réseaux sociaux et forums en ligne – Des plateformes comme Reddit ont introduit en 2023-2024 une vérification d’âge via un prestataire (upload d’ID ou selfie) pour accéder aux communautés marquées NSFW
    tomsguide.com
    tomsguide.com
    . Le réseau social X (Twitter) a également affiché des demandes de vérification d’identité pour certains contenus sensibles chez les utilisateurs britanniques, tout comme son alternative Bluesky qui propose aux utilisateurs au Royaume-Uni de vérifier leur âge via carte bancaire, pièce d’identité ou scan facial
    tomsguide.com
    tomsguide.com
    . Même des communautés comme Discord ou des applications de rencontre comme Grindr ont commencé à implémenter des contrôles d’âge sur certains contenus ou fonctionnalités
    tomsguide.com
    .

    Plateformes de streaming et médias – Des services inattendus ont suivi le mouvement : Spotify, par exemple, exige désormais une preuve d’âge pour visionner certains clips musicaux classés 18+ et utilise la technologie Yoti (vérification d’âge par reconnaissance faciale ou pièce d’identité) pour ce faire
    tomsguide.com
    . De même, la plateforme de mods de jeux vidéo Nexus Mods a introduit une restriction d’âge pour les contenus adultes
    tomsguide.com
    , et l’encyclopédie Wikipédia a fait part de son inquiétude face à la possibilité de devoir vérifier l’âge de ses contributeurs sur certains articles sensibles (la fondation Wikimedia s’opposant aux réglementations en ce sens)
    tomsguide.com
    .

    Jeux en ligne et services gaming – Le secteur du jeu vidéo n’est pas épargné. Microsoft prévoit d’intégrer un système de vérification d’âge pour les utilisateurs Xbox au Royaume-Uni, avec plusieurs méthodes (estimation faciale, ID, vérification opérateur mobile ou carte bancaire) afin de se conformer à l’Online Safety Act
    tomsguide.com
    . Sans vérification, certaines fonctionnalités sociales (chat vocal, partages) pourraient être limitées pour les joueurs non vérifiés
    tomsguide.com
    .

En résumé, la tendance mondiale est à l’extension des contrôles d’âge sur Internet. Chaque site « compliant » (conforme) qui se plie à ces exigences introduit une barrière d’accès pour l’utilisateur, au risque de frustrer les adultes légitimes et de voir ceux-ci migrer vers des alternatives plus permissives. D’ailleurs, Pornhub a publiquement fait valoir que ces lois poussent simplement les internautes vers des sites moins connus qui n’appliquent pas ces restrictions
apnews.com
. On assiste ainsi à un déplacement du trafic vers des plateformes non conformes (souvent plus petites ou hébergées dans des juridictions sans telles lois).

Problème : Pour un internaute soucieux de préserver sa vie privée, il devient difficile de savoir quels sites exigent désormais une vérification d’identité et où trouver une alternative équivalente sans contrainte. Il n’existe pas aujourd’hui de ressource centralisée listant ces sites « compliants » et les solutions de rechange disponibles. D’où l’idée de créer un outil dédié : un site web référentiel permettant d’identifier facilement les sites ayant adopté ces vérifications d’âge/identité, afin de les boycotter si on le souhaite, et de découvrir des alternatives sans vérification offrant des contenus ou services similaires.
Objectifs du projet

L’objectif principal est de développer un outil web qui informe les utilisateurs sur les sites web imposant un contrôle d’identité ou un scan facial pour accéder à du contenu mature, et qui propose des alternatives n’exigeant pas de telles vérifications. Cet outil vise à :

    Recenser de manière exhaustive, et à jour, les sites “compliants” ayant mis en place une vérification d’âge intrusive dans tous les secteurs concernés. Qu’il s’agisse de sites pornographiques, de réseaux sociaux, de plateformes médias, de services de jeux en ligne, de sites de rencontre, ou tout autre domaine imposant une restriction par âge, le répertoire doit couvrir un maximum de secteurs et de pays. L’approche se veut globale : par exemple, l’outil listera aussi bien un grand site adulte international se conformant à la loi française qu’un réseau social populaire appliquant les règles britanniques, ou un site de pari en ligne respectant la législation d’un État américain. Le périmètre est mondial et multi-domaine afin de refléter l’ampleur du phénomène.

    Fournir aux utilisateurs les informations clés sur chaque site répertorié, notamment : la nature du contrôle mis en place (upload de pièce d’identité, vérification via un prestataire tiers, analyse d’un selfie vidéo, etc.), le contexte (dans quel pays ou selon quelle loi cette vérification a été instaurée), depuis quand elle est en vigueur, et tout autre détail pertinent (par exemple si la mesure s’applique seulement dans certaines régions ou pour certaines sections du site). L’outil doit donc être pédagogique et transparent, expliquant clairement à l’internaute quel type de vérification d’âge l’attend sur tel ou tel site
    politico.eu
    . L’utilisateur doit comprendre pourquoi le site est listé (ex : « Site conforme à la loi Online Safety Act 2024 – vérification de l’âge via fournisseur externe Persona (selfie/ID requis) »).

    Orienter l’utilisateur vers des alternatives sans vérification pour chaque site « à boycotter ». C’est le second pan essentiel de l’outil : non seulement dénoncer les pratiques de vérification d’identité, mais offrir une porte de sortie aux internautes en listant des sites ou services équivalents qui n’imposent pas de contrôle d’identité. Par exemple, si un site de vidéos adulte A est devenu inaccessible sans ID, le répertoire proposera un ou plusieurs sites B, C, etc. dans la même catégorie de contenu qui, eux, se contentent d’une confirmation d’âge classique (bouton « J’ai 18+ »), ou qui n’ont pas (encore) mis en place de solution intrusive. De même, pour un réseau social majeur qui exigerait une vérification pour voir du contenu NSFW, l’outil pourrait suggérer d’autres forums ou réseaux alternatifs (par ex. des plateformes décentralisées, fédérées, ou des concurrents plus petits) où ce type de contenu reste accessible sans procédure d’identification. L’objectif est de faciliter le boycott : l’utilisateur, apprenant qu’un site qu’il fréquente devient intrusif, peut immédiatement voir vers quelle alternative se tourner.

    Encourager une prise de conscience et un mouvement utilisateur vis-à-vis de ces mesures. En rendant l’information visible et centralisée, l’outil vise à informer correctement l’utilisateur sur ses choix. Le but n’est pas d’encourager l’accès des mineurs aux contenus inadéquats, mais de défendre les droits des adultes à la confidentialité. Le site pourra donc comporter une dimension éditoriale ou communautaire : actualités sur les lois de vérification d’âge, conséquences observées, pétitions en cours, conseils (ex : utilisation de VPN, etc.), tout en restant dans le cadre légal. Cette dimension informative renforcera l’objectif de transparence et d’empowerment de l’utilisateur, afin qu’il connaisse les enjeux et solutions.

En synthèse, l’outil doit devenir un référentiel de confiance, régulièrement mis à jour, couvrant le maximum de détails possible sur la situation des vérifications d’âge en ligne, et offrant des choix alternatifs pour naviguer sans montrer patte blanche. Il s’agit d’un projet à visée éthique et pratique, pour un Internet plus respectueux de la vie privée des utilisateurs majeurs.
Description générale de la solution
Format et plateforme

Le choix initial se porte sur la création d’un site web (application web) accessible depuis n’importe quel navigateur. Ce site web sera la vitrine du service et la plateforme centrale où les informations seront consultables.

    Site web pour commencer : Le projet débutera sous forme d’un site Internet responsive (adapté aux ordinateurs et mobiles) plutôt que d’une application mobile native ou d’une extension navigateur. Cela permettra une accessibilité maximale sans installation, et une itération plus rapide lors du lancement. L’URL devra être simple et explicite (par exemple : StopVerifAge.org, BypassIDCheck.net, etc. – le nom est à définir).

    Le site web servira de base de données consultable : les utilisateurs pourront rechercher un site particulier ou parcourir des catégories pour voir quels sites imposent un contrôle d’identité. Chaque site listé disposera d’une page ou d’une fiche descriptive détaillée, et les alternatives sans vérification seront proposées en regard.

    Le design sera axé sur la lisibilité et la clarté de l’information (UX simple, sans fioritures inutiles). On évitera tout contenu superflu ou publicitaire pour se concentrer sur la mission informative. La navigation devra être intuitive, avec des filtres par secteur et pays, et une barre de recherche en haut de page. Un soin particulier sera apporté à la hiérarchisation visuelle (titres, icônes, codes couleur) pour que l’utilisateur identifie d’un coup d’œil les sites à éviter et les alternatives recommandées.

# Portée fonctionnelle (périmètre)

Secteurs couverts : L’outil ambitionne de couvrir tous les secteurs où un contrôle d’âge strict peut s’appliquer. On inclura notamment :

    Contenu adulte : sites pornographiques, plateformes d’hébergement de vidéos pour adultes, sites d’escort ou de rencontres 18+, etc. (C’est historiquement le secteur le plus visé par ces lois : en France, seules les plateformes pornographiques étaient initialement ciblées
    politico.eu
    , avant extension à d’autres acteurs).

    Réseaux sociaux et communautés en ligne : tout site ou application sociale modérant l’accès à certains contenus pour des raisons d’âge – forums type Reddit, messageries type Telegram (qui floute désormais le contenu sensible si l’âge n’est pas vérifié), plateformes de partage (Twitter/X, TikTok si applicable, etc.), serveurs de discussion (Discord, etc.). Toute communauté en ligne imposant une vérification d’identité pour contenu NSFW sera éligible à figurer.

    Plateformes de streaming multimédia : services vidéo ou audio verrouillant du contenu mature. Par exemple, des sites de streaming vidéo pouvant contenir des films/émissions 18+, ou de musique qui bloquent certains clips explicites (e.g. Spotify pour les clips 18+
    tomsguide.com
    ). YouTube et consorts pourraient être concernés si jamais ils renforcent leurs contrôles au-delà de la simple connexion compte.

    Jeux vidéo et mondes virtuels : services de jeux en ligne ou univers virtuels qui mettent en place des restrictions d’âge. Cela inclut les consoles (ex: fonctionnalités en ligne Xbox nécessitant une vérif en UK
    tomsguide.com
    ), les MMORPG/jeux en ligne avec zones adultes, ou des plateformes de mods comme Nexus Mods (qui a introduit un filtrage d’âge
    tomsguide.com
    ). Aussi, les casinos en ligne et sites de paris (qui depuis longtemps demandent pièce d’identité pour vérifier la majorité, mais qui pourraient être référencés si leur procédure est renforcée par IA par ex.).

    Autres secteurs divers : on restera attentif à d’autres domaines émergents. Par exemple, les sites de vente d’alcool, de cigarettes électroniques ou cannabis (selon légalités) pourraient recourir à des vérifications d’identité en ligne. De même, certains sites de streaming d’anime/manga ou d’art comportant du contenu érotique violent pourraient être soumis à régulation. Le cahier des charges prévoit donc une structure flexible pour ajouter de nouvelles catégories sectorielles en cas de besoin.

Couverture géographique : Le site aura une vocation internationale. Il ne se limitera pas à un pays. Chaque fiche de site précisera éventuellement la portée géographique de la mesure (exemple : « Vérification d’âge requise pour les usagers en France uniquement », ou « appliqué mondialement »). Au lancement, une priorité sera donnée aux régions où la réglementation est déjà en place ou imminente (Europe et Amérique du Nord notamment), car ce sont là que la demande utilisateur sera forte. Mais l’architecture devra permettre d’intégrer des informations pour d’autres pays si de telles lois apparaissent ailleurs. L’interface sera d’abord en français (public sensibilisé en France notamment), avec une version anglaise envisagée pour toucher un public plus large étant donné la dimension mondiale du phénomène.

Hors du périmètre : Le site ne proposera pas de contenu adulte ou autre en lui-même (ce n’est pas une plateforme de diffusion, juste un annuaire informatif). Il ne fournira pas non plus d’outils illégaux de contournement (pas de liens directs vers des VPN ou proxies illégaux, bien qu’il puisse informer sur ces pratiques dans le discours général). Il ne recueillera pas de données personnelles sensibles des utilisateurs (pas d’inscription obligatoire côté internaute pour consulter les informations – l’accès sera libre, anonyme et gratuit).

En résumé, le périmètre fonctionnel couvre la collecte, la centralisation et la présentation de données sur les pratiques de vérification d’âge de sites tiers, et la mise en relation avec des alternatives. Le cœur du service est informationnel et comparatif.
Fonctions et caractéristiques détaillées de l’outil

1. Base de données des sites “compliants”

Le système reposera sur une base de données constamment mise à jour qui recense les sites ayant mis en place un contrôle d’identité/âge. Chaque entrée (enregistrement) dans cette base contiendra les champs et attributs suivants :

    Nom du site : nom de la plateforme (ex : Pornhub, Reddit, Spotify, Xbox Live, etc.).

    URL principale : adresse web ou domaine (ex : pornhub.com).

    Secteur / Catégorie : catégorie prédéfinie (Adulte, Réseau social, Streaming, Jeu en ligne, etc. – voir liste des secteurs couverts). Un site peut appartenir à plusieurs catégories le cas échéant.

    Description du service : courte description du type de contenu ou service proposé par ce site, pour informer l’utilisateur (ex : « Réseau social de forums communautaires », « Site de vidéos pour adultes », « Plateforme de streaming musical », etc.).

    Type de vérification d’âge déployée : informations spécifiques sur la méthode de vérification mise en place, par exemple :

        Contrôle par document d’identité (avec éventuellement précision du prestataire si connu, ex : “via service Veriff ou Persona” si le site communique là-dessus).

        Vérification par analyse faciale IA (préciser si possible l’outil, ex : “estimation de l’âge via l’IA Yoti”
        tomsguide.com
        ).

        Validation par carte bancaire (même si cette méthode tend à disparaître pour non-conformité aux nouvelles normes
        politico.eu
        , certains sites l’ont utilisée).

        Vérification via identifiant gouvernemental (par ex. en France un futur système d’identification via FranceConnect pourrait voir le jour).

        Autre méthode (ex : en UK, certains sites offrent plusieurs choix – Persona, Yoti, carte bancaire, etc. – il faudra l’indiquer
        tomsguide.com
        ).

        Si un site a choisi une alternative inhabituelle (ex: contrôle d’âge au niveau de l’appareil comme le préconisent certains opérateurs
        tf1info.fr
        ), cela sera mentionné.

    Portée et obligations légales associées : ce champ explique pourquoi le site a mis en place ce contrôle. On précisera la loi ou réglementation correspondante et la zone géographique d’application :

        Exemples : « Conformité à la loi française n°XXXX (2024) – contrôle d’âge obligatoire pour les sites pornographiques en France
        tf1info.fr
         » ;

        « Mise en conformité avec l’Online Safety Act 2023 (R.-Uni) – restriction du contenu adulte pour les utilisateurs britanniques
        tomsguide.com
         » ;

        « Exigence de l’État de Louisiane (USA) – loi locale de 2023 sur la pornographie en ligne » ;

        « Politique interne du site – décision volontaire de la plateforme d’instaurer un âge minimum vérifié » (certains services peuvent prendre les devants sans loi directe).

    Date d’entrée en vigueur : la date (même approximative) depuis laquelle le contrôle d’âge est effectif sur le site. Ceci permet aux utilisateurs de savoir si c’est récent (et potentiellement contournable) ou en place depuis longtemps. Si la date exacte n’est pas connue, on indiquera « Depuis mi-2025 », « À partir de juillet 2024 » etc., idéalement avec une référence (communiqué, actualité).

    Statut d’accessibilité : dans certains cas, au lieu d’implémenter une vérification, un site a pu choisir de se rendre inaccessible sur une zone (ex: blocage géographique). On le signalera dans ce champ. Par exemple : « Site non accessible aux utilisateurs localisés en Utah – redirection vers un message explicatif à la place du contenu
    apnews.com
     » ; « Blocage volontaire pour les IP françaises en protestation à la loi ». Ce statut est important car du point de vue de l’utilisateur, un site bloqué ou un site demandant une pièce d’identité aboutissent tous deux à ne pas pouvoir naviguer librement.

    Sources / référence : pour la transparence, chaque fiche contiendra en interne une référence à la source d’information ayant permis de confirmer la présence de la vérification. Par exemple, un lien vers un article de presse, un communiqué officiel du site, ou l’expérience utilisateur rapportée. Ces sources pourront être citées (via une petite icône cliquable « i » menant à plus d’info) pour donner du contexte à l’utilisateur méfiant. (Dans la version publique, ces références seront présentées de manière non intrusive, peut-être en bas de page ou dans un volet d’information supplémentaire.)

Exemple illustratif (fictif) d’une fiche :

Nom : Reddit  
Catégorie : Réseaux sociaux / Forum  
Vérification d’âge : **Obligation de vérification via service tiers (Persona)** – scan d’une pièce d’identité **ou** selfie vidéo requis:contentReference[oaicite:34]{index=34}.  
Contexte légal : Conformité à l’Online Safety Act 2023 (UK) – depuis juillet 2024, les subreddits NSFW et certains contenus (alcool, gambling) sont restreints aux comptes vérifiés au Royaume-Uni:contentReference[oaicite:35]{index=35}.  
En vigueur depuis : 14 juillet 2024.  
Accessibilité : **Pas de restriction hors UK** – les utilisateurs d’autres pays ne sont pas concernés par cette vérification pour le moment.  

(Des icônes pourraient signaler visuellement “ID” pour pièce d’identité, “Selfie” pour reconnaissance faciale, “CC” pour carte bancaire, etc., afin que dans la liste on voie rapidement quel type de vérif.)

Cette base de données sera le noyau central du projet. Elle devra être conçue de manière évolutive pour intégrer facilement de nouvelles entrées et mettre à jour les existantes. On prévoit d’ailleurs une montée en charge automatique : initialement, le nombre de sites listés peut être modeste (quelques dizaines de très connus), mais l’architecture doit permettre d’atteindre potentiellement des centaines de sites référencés à terme (en incluant de plus en plus de pays et de plateformes).

2. Listing des alternatives sans vérification

Pour chaque site “compliant” recensé, le cœur du service est de proposer une ou plusieurs alternatives équivalentes n’imposant pas de contrôle d’identité strict. Cette fonctionnalité se matérialise ainsi :

    La fiche d’un site comportera une section « Alternatives sans vérification » listant d’autres sites ou services similaires. Par exemple, pour un site pornographique donné qui demande une vérification, on pourra suggérer d’autres sites pornographiques comparables (même type de contenu, même genre de vidéos) qui n’exigent qu’un simple clic de confirmation d’âge ou aucune vérif du tout. Pour un réseau social grand public imposant des vérifications sur du contenu sensible, on pourra lister des réseaux alternatifs (par ex. Mastodon, Lemmy, Peertube, etc., selon le cas d’usage) où les communautés équivalentes existent sans ces restrictions. Un autre exemple : si un service de streaming de vidéos officielles (type YouTube/Spotify) se met à restreindre certains contenus par âge vérifié, on peut pointer l’utilisateur vers des plateformes alternatives ou vers des astuces (par ex. regarder un clip musical sur une autre plateforme libre).

    Nombre d’alternatives : idéalement, au moins une alternative par site listé. S’il en existe plusieurs pertinentes, on peut en proposer 2 ou 3, classées par popularité ou par pertinence. Le but est de donner le choix à l’utilisateur boycottant : il ne s’agit pas de faire de la publicité pour une alternative unique, mais de montrer qu’il y a un écosystème sans vérification qu’il peut explorer.

    Description des alternatives : chaque alternative listée aura un mini-descriptif expliquant en quoi ce service est similaire et confirmant qu’aucune vérification d’identité n’y est requise (du moins à la connaissance actuelle). Ex : « SiteB.com – plateforme vidéo adulte généraliste basée à l’étranger, accessible sans compte ni vérification (simple disclaimer 18+). Contenu semblable à SiteA.com, avec catégories XXX variées. » Ou « Lemmy – alternative open-source à Reddit, composée de communautés auto-hébergées. Aucune vérification d’âge centralisée : chaque instance peut définir ses règles, mais pas de demande d’ID globale. »

    Fiabilité et légalité des alternatives : on s’engage à ne proposer que des alternatives légales et relativement sûres. Cela veut dire que les sites de contenus illégaux ou dangereux seront exclus (par ex, ne pas renvoyer vers un site qui serait connu pour du malware ou des pratiques douteuses). De même, on ne recommandera pas de solutions qui permettent à des mineurs de contourner la loi de façon illicite. Les alternatives proposées doivent être destinées aux adultes, comme l’outil entier. Un message d’avertissement général peut rappeler que « Les alternatives suggérées sont réservées aux publics majeurs ». Le but est de protéger la vie privée des adultes, pas d’encourager les mineurs à consommer du contenu inapproprié.

    Actualisation des alternatives : il faudra tenir à jour ces suggestions. Si une alternative vient à implémenter elle aussi un contrôle d’âge (par exemple un site jusqu’ici ouvert décide de se conformer plus tard), alors ce site devrait basculer de la liste « alternative » à la liste des sites “compliants” (et on lui trouvera d’autres alternatives…). Un mécanisme de suivi sera donc prévu pour réévaluer régulièrement les alternatives.

    Notation ou feedback utilisateur (optionnel) : on pourrait permettre aux utilisateurs de donner un retour sur les alternatives proposées (par ex. un système de vote ou de commentaire sur l’utilité de l’alternative, ou un signalement si l’alternative demande désormais une vérif). Cela aiderait à ajuster la liste et assure une forme de curation communautaire. Cependant, ceci pourrait être implémenté dans une seconde phase pour ne pas complexifier la v1.

Cette partie « Alternatives » est cruciale pour la philosophie de boycott : il ne suffit pas de dire « n’allez plus sur tel site », il faut offrir une solution de rechange pour que l’utilisateur ne perde pas l’accès au type de contenu recherché. Ainsi, le cahier des charges insiste sur la recherche approfondie d’alternatives pertinentes pour chaque site ajouté. Dans certains cas, la meilleure alternative pourra être d’indiquer des outils de contournement technique (ex : « utilisez un VPN pour continuer d’accéder à la version non restreinte » ou « passez par le réseau Tor sur tel site miroir »), mais ces conseils seront formulés prudemment, en dernier recours, et accompagnés de disclaimers sur la légalité selon le pays. L’accent principal restera sur les autres sites ou services disponibles légalement.

3. Recherche, filtres et navigation

Pour que l’outil informe efficacement, il doit être facile à parcourir. Les fonctions de recherche et de filtrage permettront aux usagers de trouver rapidement l’information voulue :

    Barre de recherche libre en haut de chaque page : l’utilisateur peut y taper le nom d’un site web ou d’un service pour voir s’il est référencé. La recherche sera en auto-complétion si possible, et tolérante (ex : si on tape “pornhub” ou “Porn hub” ou “pronhub”, le résultat doit apparaître). Si le site cherché n’est pas encore listé, le site pourrait proposer un message « Pas encore dans la base… » avec éventuellement une option de suggestion (voir point sur contributions).

    Filtres par catégorie : une page dédiée ou un menu permettra de filtrer par grands thèmes. Par exemple, un menu « Catégories » offrant la liste : Sites Adultes, Réseaux Sociaux, Streaming, Jeux en ligne, Divers. En cliquant sur l’une, on voit tous les sites de cette catégorie qui ont une vérification d’âge, avec un résumé de la méthode de contrôle pour chacun. Ce listing filtré permet de parcourir, par curiosité ou par veille, l’état du secteur. Par exemple, un journaliste ou un curieux pourrait lister tous les réseaux sociaux impactés pour avoir une vue d’ensemble des politiques selon les plateformes.

    Filtre par pays/région : il pourrait être utile de filtrer par zone géographique d’application des mesures. Par exemple « En France » vs « International » vs « États-Unis », etc., afin que l’utilisateur puisse voir quels sites posent problème dans son pays. Un français voudra surtout connaître les sites bloqués ou à vérification en France, un britannique ceux liés à la loi UK, etc. Ce filtrage peut être fait via un petit sélecteur de pays ou via des tags sur les fiches (ex : [FR], [UK], [US], [UE]…). Remarque : Un site peut apparaître dans plusieurs filtres géographiques s’il a des contrôles dans plusieurs régions (ex: s’il applique la loi UK pour UK et la loi d’un État US pour les visiteurs de cet État).

    Tri et classement : par défaut, on peut classer les sites par popularité (les plus connus en premier) ou par date d’ajout récente. Des options de tri (alphabétique, popularité, récents…) seront offertes pour que l’utilisateur organise la liste à sa convenance.

    Navigation interne : le site comportera quelques pages statiques en plus du listing dynamique, par exemple « À propos » (explication de la mission, contexte légal global), « Actualités » (voir plus loin), et éventuellement « FAQ » (réponses aux questions usuelles sur la légalité, le fonctionnement, etc.). Une navigation simple (menu en header ou sidebar) donnera accès à ces sections.

4. Mise à jour automatique et contribution

Étant donné la rapidité avec laquelle la situation évolue (nouvelles lois, nouveaux sites se conformant ou inversément renonçant à se conformer), l’outil doit intégrer dès la conception une stratégie pour mettre à jour les données de façon efficace, idéalement automatisée. Plusieurs mécanismes sont envisagés :

    Veille automatisée des sources officielles et de l’actualité : Un module logiciel pourra effectuer une veille périodique sur des sources clés (par ex. sites des régulateurs comme l’ARCOM en France, communiqués d’OFCOM au Royaume-Uni, actualités tech, forums spécialisés comme Reddit, etc.). En identifiant des mots-clés (noms de sites + “age verification”, “ID check”, etc.), on peut repérer rapidement qu’un nouveau site a instauré un contrôle ou qu’un site a été bloqué. Par exemple, si l’ARCOM publie une liste de sites mis en demeure ou bloqués, l’outil pourrait automatiquement la récupérer et la comparer à la base existante pour ajouter/mettre à jour des entrées
    politico.eu
    politico.eu
    . Cette partie requiert de l’ingénierie (scraping de pages web, utilisation d’API s’il y en a, flux RSS de sites d’actus juridiques…). On cherchera à automatiser au maximum pour ne pas dépendre uniquement d’une intervention humaine quotidienne.

    Analyse automatique de site web (crawling) : Ce serait un complément innovant mais complexe – l’idée serait de détecter automatiquement si un site impose un âge vérifié en testant son comportement. Par exemple, un robot pourrait essayer d’accéder à la page d’accueil ou à du contenu de test sur un site cible depuis différentes adresses IP régionales, et détecter la présence de certaines caractéristiques : texte du type “veuillez vérifier votre âge” ou éléments HTML spécifiques des modules de vérification (script d’un prestataire connu tel que Yoti, pop-up Persona, redirection vers un service d’identité). Si le robot détecte qu’un site redirige vers un domaine de vérification ou affiche un formulaire d’ID, cela pourrait générer une alerte. Limite : ce mécanisme peut être fragile (il y a mille manières d’implémenter un contrôle d’âge) et il risque de consommer des ressources. Il pourrait être exploité pour quelques grands sites en surveillance, mais pas forcément pour tout le web. On le considère en bonus pour fiabiliser les données sur les sites majeurs.

    Mise à jour manuelle / éditoriale : Au lancement, il faudra de toute façon alimenter la base manuellement en récoltant les infos disponibles. Une équipe éditoriale ou la personne en charge du projet devra effectuer une recherche initiale (via actualités et tests concrets) pour remplir les fiches. Ensuite, cette même équipe assurera une vérification régulière des données. L’automatisation aide, mais ne garantit pas 100% de couverture. Il y aura donc un travail de veille humaine : suivre les news, les retours utilisateurs, tester périodiquement certains sites listés pour voir s’ils changent leur politique. Le cahier des charges prévoit la rédaction de procédures internes pour cette veille (ex : chaque mois, vérifier un échantillon aléatoire de sites listés ; chaque fois qu’une loi passe dans un pays, vérifier les principaux sites du secteur concerné dans ce pays, etc.).

    Contributions des utilisateurs (crowdsourcing) : Puisque l’outil s’adresse à une communauté vigilante, il est judicieux de permettre aux utilisateurs de signaler des informations. Concrètement, on implémentera un formulaire de suggestion sur le site web, du type « Proposer un site / Signaler un changement ». Un utilisateur pourra indiquer : « Le site X demande maintenant une pièce d’identité depuis tel jour », ou « Le site Y est une bonne alternative sans vérif ». Ces remontées seront modérées (pour éviter le spam ou les erreurs) par l’équipe, puis vérifiées et intégrées si elles s’avèrent correctes. Avec le temps, cette approche participative peut enrichir beaucoup la base de données de cas locaux ou spécifiques que l’équipe de base n’aurait pas repérés.

    Fréquence de mise à jour : Grâce aux méthodes ci-dessus, l’outil devrait être mis à jour en continu. En pratique, on peut viser une mise à jour notable (ajout ou modification) au moins chaque semaine, voire quotidienne en période de forte actualité législative. Le site affichera quelque part une mention « Dernière mise à jour le … » pour rassurer les visiteurs sur la fraîcheur des informations.

En combinant l’automatisation (veille web), la contribution utilisateur, et l’effort éditorial, on vise une exhaustivité maximale et une réactivité élevée. L’ambition est d’être la référence sur ce sujet, donc de ne pas laisser de côté un site important qui aurait implémenté un contrôle d’âge sans le mentionner.

5. Interface utilisateur et design UX

Le design de l’outil doit servir son objectif informatif : il sera donc sobre, clair et orienté vers la consultation efficace. Quelques points de conception UX/UI :

    Accueil du site (Home page) : La page d’accueil présentera brièvement le contexte et la mission du projet (quelques phrases d’introduction sur le problème des vérifications d’âge et l’utilité de l’outil). Elle mettra en avant un champ de recherche bien visible (« Recherchez un site… ») et éventuellement un bouton d’accès aux catégories. On pourra aussi afficher sur la page d’accueil quelques exemples marquants, par exemple une section « Sites récemment ajoutés » ou « Top sites à éviter en ce moment » pour attirer l’attention (ex : Pornhub, Reddit, Twitter, etc., s’ils sont dans la liste).

    Page liste/catégorie : Lorsqu’on affiche la liste des sites (par catégorie ou par recherche), l’information sera présentée sous forme d’entrées condensées avec possibilité de déplier pour le détail :

        Par exemple, une liste à puces ou un tableau où chaque ligne = Nom du site – icônes de méthode (ID, selfie…) – courte note sur le type de contenu – [bouton ou lien « Détails »].

        Si l’utilisateur clique sur « Détails » ou sur le nom, il arrive sur la page de fiche complète du site. Alternativement, on peut déployer un accordéon pour montrer un aperçu des alternatives sans quitter la page liste.

        Les sites pourraient être mis en forme avec un code couleur : par exemple, rouge/orange pour signaler « attention, vérification d’âge requise », et vert à côté des alternatives « recommandé sans vérif ». Ainsi, visuellement, l’utilisateur voit la liste des “mauvais élèves” et tout de suite les “échappatoires” associées.

    Page fiche d’un site : La page dédiée à un site “compliant” reprendra toutes les informations de la base le concernant, bien structurées avec des sous-titres (Méthode de vérification, Contexte légal, etc.). Les alternatives seront présentées sous forme d’une liste avec nom + description + lien direct. On insérera éventuellement un lien « guide : comment accéder à [site] sans vérification » si pertinent (par ex. renvoyant vers l’usage d’un VPN ou d’un proxy – mais cela sera traité prudemment, possiblement dans une section blog/actualités séparée pour les astuces générales).

    Performances et simplicité : Le site doit être léger et rapide pour être utilisable même par des internautes qui pourraient, par souci de confidentialité, naviguer via Tor ou VPN avec bande passante limitée. Pas de vidéos auto-play, pas de design lourd. Du texte, des liens, éventuellement quelques icônes vectorielles, et c’est tout. Ainsi la page pourra se charger rapidement même sur un réseau lent ou sur mobile.

    Responsive design : Un grand nombre d’utilisateurs potentiels pourront consulter ce site depuis leur smartphone. Il faudra donc s’assurer que l’interface est bien utilisable sur petit écran : menu hamburger pour les catégories, liste déroulante facilement scrollable, pas de tableaux larges difficiles à lire sur mobile, etc. Le cahier des charges impose des tests UI sur différents formats (desktop, tablette, mobile).

    Accessibilité : Autant que possible, respecter les standards d’accessibilité (contraste de couleurs, texte alternatif sur les icônes, navigation clavier possible, etc.) pour que l’outil soit utilisable par tous.

Visuellement, on peut imaginer un style évoquant la vigilance et la fiabilité (par ex. un logo avec un bouclier ou un œil barré, signifiant la protection de la vie privée, ou un symbole 18+ barré, etc.). Mais ce sont des détails cosmétiques à affiner. L’essentiel est que l’utilisateur se sente en confiance en lisant les informations (d’où l’importance de citer des sources ou d’afficher les références pour montrer le sérieux).

6. Section d’actualités et ressources

Pour informer correctement l’utilisateur, il peut être judicieux d’intégrer au site une section Actualités/Articles liées à la thématique :

    Cette section pourrait contenir des brèves ou des articles de blog rédigés par l’équipe, qui expliquent les évolutions récentes : nouvelles lois adoptées, réactions de l’industrie, analyses des solutions techniques (par ex. expliquer ce qu’est la technologie de “double anonymat” en France, ou un comparatif des solutions d’age verification du marché), tutoriels pour utiliser un VPN en toute légalité, etc.

    On peut y relayer des statistiques marquantes (ex: “5 millions de contrôles d’âge sont effectués chaque jour suite à la loi UK”
    tomsguide.com
    ) ou des informations sur l’opposition en cours (ex: pétitions, associations, positions d’ONG comme l’Electronic Frontier Foundation qui critique ces lois
    apnews.com
    ).

    L’objectif est que l’utilisateur comprenne le contexte plus large au-delà de la simple fiche. S’il le souhaite, il peut approfondir ses connaissances depuis notre plateforme. Cela renforce la crédibilité de l’outil en le positionnant aussi comme centre de ressources sur le sujet.

    Bien entendu, cette section resterait secondaire par rapport à la fonction première (annuaire de sites). Elle doit être à jour mais ne pas noyer l’interface principale (peut-être juste un lien "Actualités" dans le menu).

7. Considérations techniques et sécurité

Quelques éléments techniques à prendre en compte dans le cahier des charges :

    Stack technologique : Le site web pourra être développé avec des technologies web classiques (HTML/CSS/JavaScript pour le front-end, et un back-end pour la base de données + logique). Un framework web (comme React/Vue pour le front si nécessaire pour interactivité, et Node.js/Python/PHP etc. pour le back) peut être utilisé. L’important est la fiabilité et la facilité de maintenance. Étant donné l’accent sur les données, un SGBD (base de données) type PostgreSQL ou MySQL suffira pour stocker les fiches et leurs attributs.

    Scalabilité : Le volume d’utilisateurs n’est pas facilement prévisible, mais si le site devient la référence, il pourrait y avoir beaucoup de trafic. Il faudra héberger sur une infrastructure robuste et sécurisée, supporter des pics de connexions (par ex. lors d’une news majeure, tous les internautes cherchent “quel site est bloqué ?” et tombent sur nous). On dimensionnera l’hébergement en conséquence.

    Sécurité : Le site lui-même doit être exemplaire en matière de confidentialité, puisqu’il s’adresse à un public sensibilisé. On utilisera HTTPS partout, pas de traqueurs tiers intrusifs, une politique de cookies minimale (juste ce qu’il faut pour le fonctionnement, pas de pub ni analytiques invasifs). Si des comptes utilisateurs sont introduits (pour commenter ou proposer des ajouts), on gérera les données de manière sécurisée (hachage des mots de passe, etc.). On peut aussi permettre le signalement anonyme sans compte pour protéger les contributeurs.

    Modération et fiabilité du contenu : Puisque l’outil va potentiellement pointer vers des sites pornographiques ou autres, il faut prendre garde à la présentation pour éviter tout problème légal ou de choquer le public non averti. Le site pourrait exiger une confirmation “+18” à son entrée également, étant donné qu’il va explicitement parler de sites adultes (bien que ne montrant aucun contenu pornographique, par principe on peut afficher un disclaimer “Ce site s’adresse aux adultes souhaitant s’informer sur la protection de leur vie privée en ligne”). Par ailleurs, il faudra vérifier chaque alternative proposée pour s’assurer que ce n’est pas un piège ou un site illégal. Une charte de qualité interne devra être suivie : ne recommander que des alternatives qui respectent la loi (dans leur pays d’origine au moins), qui ne contiennent pas de contenus illégaux (pédopornographie, incitation à la haine, etc. évidemment exclus), et si possible qui ont bonne réputation. Le but est de ne pas échanger un mal pour un pire (par ex éviter d’envoyer des utilisateurs vers un site non vérifié mais plein de malware).

    Légalité : Le projet en lui-même doit rester dans les clous légalement. Référencer des sites et expliquer comment accéder à du contenu adulte sans vérification est délicat. Il faudra sans doute inclure des mentions légales sur le site clarifiant que :

        L’outil ne garantit pas la légalité de l’utilisation des alternatives dans le pays de l’utilisateur (ex : « si vous résidez dans un endroit où la loi exige la vérification d’âge, utiliser une alternative sans vérification peut être en infraction » – on informera l’utilisateur de sa responsabilité).

        Le site se dégage de toute responsabilité quant aux contenus des sites externes listés.

        On s’oppose à l’accès des mineurs aux contenus inappropriés et ce site n’est pas fait pour aider les mineurs, mais pour informer les adultes.

        Ces précautions juridiques sont essentielles car on touche à un domaine réglementé et controversé.

8. Évolution future du projet

Bien que le lancement se fasse via un site web, le cahier des charges anticipe des extensions possibles si le service rencontre son public :

    Applications mobiles dédiées : Une fois le concept stabilisé, développer une app mobile (Android/iOS) pour faciliter l’accès à la base de données sous forme d’application. Celle-ci pourrait offrir par exemple des notifications push (ex: « Nouveau site ajouté dans la catégorie Jeux vidéo », « Le site X nécessite désormais un selfie – alternative dispo… »). Cependant, la validation sur les stores d’une app listant des sites adultes pourrait être compliquée, d’où la prudence de commencer par le web.

    Extension navigateur / plugin : Une autre idée puissante serait une extension pour navigateur qui, lorsqu’un utilisateur tente de visiter un site présent dans notre base, affiche une alerte : « Attention, ce site requiert une vérification d’identité. Voulez-vous voir les alternatives ? ». L’extension pourrait alors proposer en un clic de rediriger vers une alternative sans vérif. Cela rendrait le boycott très concret au quotidien. C’est néanmoins un développement distinct plus technique, prévu éventuellement en second temps.

    Collaboration communautaire accrue : Si le site gagne en visibilité, on pourrait mettre en place un véritable forum de discussion ou un système de commentaires où la communauté échange des astuces, partage des retours d’expérience sur tel ou tel site (par ex: un utilisateur pourrait commenter « tel site alternatif fonctionne bien, mais attention beaucoup de pubs », etc.). Ceci doit être modéré avec rigueur (pour éviter les dérapages, la pub déguisée, etc.), mais peut enrichir la valeur du service.

    Données ouvertes (Open Data) : Le projet pourrait publier sa base de données (ou une partie) en open data ou via une API publique, pour que d’autres développeurs ou chercheurs puissent réutiliser la liste de sites. Par exemple, une API REST permettant de requêter « ce site nécessite-t-il une vérif d’identité ? » pourrait servir à d’autres applications ou à intégrer l’info dans des filtres de navigateur. C’est à considérer selon le financement et l’esprit du projet (s’il est communautaire et open-source).

    Monétisation éventuelle : Ce projet est avant tout militant, mais s’il fallait envisager des coûts (serveur, maintenance), on pourrait imaginer des modèles type donation, ou des subventions via des organisations de défense des droits numériques. Il est exclu a priori de monétiser via de la publicité classique (car cela nuirait à la neutralité et l’expérience utilisateur). Ces aspects ne sont pas prioritaires dans le cahier des charges initial, mais devront être abordés en temps voulu pour pérenniser l’outil.

Conclusion

En rassemblant toutes ces exigences, ce cahier des charges définit un outil complet, centré utilisateur, visant à maximiser l’information et les choix offerts face aux récents contrôles d’identité en ligne. Grâce à un site web clair et détaillé, alimenté par une base de données riche et mise à jour de façon automatique autant que possible, l’utilisateur pourra :

    Identifier rapidement quels sites (tous secteurs confondus) cherchent à contrôler son identité pour l’accès à du contenu adulte/sensible.

    Comprendre les modalités de ces contrôles et le contexte (lois, portée).

    Trouver immédiatement des alternatives similaires sans avoir à fournir de pièce d’identité ni subir de scan facial, lui permettant de continuer à naviguer librement tout en boycottant les sites intrusifs.

    Se tenir informé des évolutions législatives et techniques autour de la vérification d’âge en ligne, pour appréhender les enjeux sur sa vie numérique.

En fournissant “le maximum de détails possible” de manière lisible et organisée, l’outil cherchera à redonner du pouvoir aux internautes dans un environnement web de plus en plus contraint. Il s’agit d’un projet ambitieux mêlant aspects techniques (collecte de données automatisée, site à fort contenu dynamique) et enjeux éthiques. Si toutes les fonctionnalités décrites sont mises en œuvre avec succès, ce site deviendra une référence précieuse pour tous ceux qui défendent un Internet ouvert et respectueux de la vie privée des adultes responsables, tout en s’inscrivant dans une démarche citoyenne de discussion sur la proportionnalité de ces nouvelles régulations
tomsguide.com
tomsguide.com
.

En somme, ce cahier des charges pose les bases d’un outil au service des droits numériques des utilisateurs, en réaction constructive aux mesures de contrôle de l’âge : non pas pour nier la protection des mineurs, mais pour proposer un équilibre où la protection de la jeunesse ne se fait pas au détriment de la liberté et de la vie privée de toute une population en ligne. La prochaine étape consistera à valider ces spécifications avec les parties prenantes, puis à entamer le développement itératif du site web et de sa base de données, afin de livrer une première version opérationnelle et fiable aux usagers concernés.

Sources : Les informations utilisées pour élaborer ce cahier des charges proviennent notamment de comptes rendus médiatiques et officiels sur les lois et initiatives de vérification d’âge en 2023-2025. On citera par exemple l’article de Politico.eu (2025) détaillant l’obligation en France d’utiliser un selfie vidéo ou une pièce d’identité pour les sites adultes
politico.eu
, l’article de Tom’s Guide (2024) recensant les plateformes variées (réseaux sociaux, services de streaming, apps de rencontre, etc.) qui ont introduit de tels contrôles suite aux lois britanniques
tomsguide.com
tomsguide.com
, ou encore les déclarations de Pornhub soulignant le report du trafic vers des sites non conformes quand des contrôles trop stricts sont imposés
apnews.com
. Ces éléments de contexte confirment la pertinence et l’urgence du développement de l’outil proposé. Toutes les citations et données intégrées ont pour but d’assurer que l’outil repose sur une compréhension précise de l’état de l’art et des besoins utilisateurs réels.
