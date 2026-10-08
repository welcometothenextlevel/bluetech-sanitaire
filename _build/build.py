#!/usr/bin/env python3
"""Generates the Bluetech Sanitaire static site into ../docs. Edit this file, not the HTML.
CSS and JS are hand-written in docs/assets; bump V after editing them (cache-buster)."""
import os, json, html, math
from urllib.parse import quote
from svg import LOGO, LOGO_SYMBOL, ARROW, ARROW_UR, PHONE, MAIL, PIN, PLUS, CLOSE, CHECK, CHEV, LEFT, RIGHT, WA, GOOGLE, STARS, SICON, ART

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
BASE = "https://welcometothenextlevel.github.io/bluetech-sanitaire/"
V = "1"
NOINDEX = True  # keep the site out of Google while the phone number and reviews are placeholders

# ------------------------------------------------------------------ contact (PLACEHOLDERS — to confirm with the owner)
PHONE_DISPLAY = "+41 XX XXX XX XX"
PHONE_TEL = "+41000000000"
WA_NUMBER = "41000000000"
EMAIL = ""                 # e.g. "info@bluetech-sanitaire.ch" — the forms' e-mail option appears once set
GOOGLE_REVIEWS_URL = ""    # Google Business "write a review" link, once the profile exists

TEL = "tel:" + PHONE_TEL
WA_URL = "https://wa.me/" + WA_NUMBER
def wa(text):
    return WA_URL + "?text=" + quote(text)
WA_HELLO = wa("Bonjour Bluetech Sanitaire, ")

# ------------------------------------------------------------------ company (Registre du commerce VD / Moneyhouse, 2026-10-08)
CO = dict(name="Bluetech Sanitaire Sàrl", brand="Bluetech Sanitaire", street="Route de Renens 2", zip="1008", city="Prilly",
          canton="VD", ide="CHE-227.168.225", rc="CH-550.1.258.051-8", manager="Ahmet Hoti", founded="2026-07-08",
          lat=46.52856, lng=6.60343)
ADDR = "%s, %s %s" % (CO["street"], CO["zip"], CO["city"])
MAPS = "https://www.google.com/maps/search/?api=1&query=" + quote(CO["name"] + " " + ADDR)
MAP_EMBED = "https://maps.google.com/maps?q=" + quote(ADDR) + "&z=16&output=embed"

# ------------------------------------------------------------------ services
SERVICES = [
    dict(slug="installations-sanitaires", icon="install", art="install", title="Installations sanitaires", short="Neuf & transformation",
         spec="EF · EC · Évacuations · Appareils",
         card="Distribution, évacuations, bâtis-supports et appareils : des réseaux complets, posés proprement et contrôlés avant fermeture.",
         h1="Installations sanitaires, du réseau à la robinetterie.",
         lead="Construction neuve ou transformation : nous posons l’installation complète — distribution d’eau froide et d’eau chaude, évacuations, bâtis-supports et appareils — avec des axes tracés au mur et des raccords contrôlés un à un.",
         mt="Installations sanitaires à Prilly et Lausanne",
         md="Installations sanitaires neuves et transformations à Prilly, Lausanne et environs : distribution EF/EC, évacuations, bâtis-supports, appareils. Devis sans engagement.",
         items=[("Distribution EF / EC", "Réseaux d’eau froide et d’eau chaude par collecteurs, conduites gainées et repérées."),
                ("Évacuations & colonnes", "Colonnes de chute, conduites d’évacuation et ventilations, posées avec les pentes adéquates."),
                ("Bâtis-supports", "Systèmes encastrés pour WC suspendus, lavabos, douches et baignoires, implantés au trait."),
                ("Appareils sanitaires", "Pose et raccordement des WC, lavabos, vasques, douches, baignoires et robinetteries."),
                ("Cuisine & buanderie", "Raccordement d’éviers, de lave-vaisselle, de lave-linge et de sèche-linge."),
                ("Coordination de chantier", "Suivi avec l’architecte, le maître d’ouvrage et les autres corps de métier.")],
         steps=[("Relevé & implantation", "Lecture des plans, relevé sur place, axes des appareils tracés au mur."),
                ("Pose des réseaux", "Collecteurs, alimentations et évacuations posés, fixés et repérés."),
                ("Contrôle avant fermeture", "Mise en pression, contrôle d’étanchéité, raccords vérifiés et marqués."),
                ("Appareils & mise en service", "Pose des appareils et de la robinetterie, réglages, remise des lieux propres.")],
         faq=[("Intervenez-vous en construction neuve comme en rénovation ?", "Oui. Nous réalisons des installations complètes sur des chantiers neufs et adaptons les réseaux existants lors de transformations, en appartement comme en maison."),
              ("Travaillez-vous avec les architectes et les autres entreprises ?", "Oui. Nous coordonnons nos interventions avec l’architecte ou le maître d’ouvrage, ainsi qu’avec le carreleur, l’électricien et le plâtrier, pour que chaque étape arrive au bon moment."),
              ("Quand l’installation est-elle contrôlée ?", "Avant la fermeture des parois : les réseaux sont mis en pression et chaque raccord est vérifié. C’est le moment où un défaut se corrige facilement — plus tard, il coûte un mur."),
              ("Comment obtenir un devis ?", "Décrivez votre projet via le formulaire, sur WhatsApp ou par téléphone. Nous convenons d’une visite si nécessaire, puis vous recevez un devis détaillé, sans engagement.")],
         photos=["wc-douche-collecteur", "double-bati-ventilation"]),
    dict(slug="renovation-salle-de-bains", icon="shower", art="shower", title="Rénovation de salles de bains", short="Douche · Bain · WC · Vasques",
         spec="Dépose · Adaptation · Pose",
         card="Baignoire remplacée par une douche, WC suspendu, double vasque : nous adaptons les réseaux et posons les nouveaux équipements.",
         h1="Votre salle de bains, repensée jusque dans les murs.",
         lead="Remplacer une baignoire par une douche de plain-pied, passer à un WC suspendu, installer une double vasque : nous adaptons les conduites existantes et posons vos nouveaux équipements, en coordination avec les autres artisans.",
         mt="Rénovation de salle de bains à Prilly et Lausanne",
         md="Rénovation de salles de bains à Prilly, Lausanne et environs : douche à l’italienne, WC suspendu, vasques, adaptation des conduites. Devis sans engagement.",
         items=[("Dépose & adaptation", "Démontage des anciens appareils, adaptation des alimentations et des évacuations."),
                ("Douche de plain-pied", "Douche à l’italienne avec caniveau ou siphon de sol, mitigeur thermostatique."),
                ("Baignoire", "Remplacement ou pose de baignoire, robinetterie apparente ou encastrée."),
                ("WC suspendu", "Remplacement d’un WC au sol par un WC suspendu sur bâti-support."),
                ("Vasques & meubles", "Lavabos, meubles vasques simples ou doubles, robinetterie et accessoires."),
                ("Coordination", "Planning commun avec le carreleur, l’électricien et le peintre.")],
         steps=[("Visite & conseils", "Nous regardons l’existant, les évacuations disponibles et vos envies."),
                ("Devis détaillé", "Chaque poste chiffré, avec un planning réaliste."),
                ("Travaux", "Protection des lieux, dépose, adaptation des réseaux, pose des équipements."),
                ("Remise des lieux", "Mise en service, contrôle de chaque point d’eau, nettoyage.")],
         faq=[("Combien de temps dure une rénovation de salle de bains ?", "Cela dépend de l’ampleur des travaux et des autres corps de métier impliqués. Vous recevez un planning précis avec le devis, après la visite."),
              ("Peut-on transformer une baignoire en douche ?", "Oui, c’est l’une des demandes les plus fréquentes. Nous vérifions d’abord l’évacuation disponible pour garantir un écoulement correct, puis nous proposons la solution adaptée."),
              ("Puis-je fournir mes propres appareils ?", "C’est possible. Nous vérifions ensemble leur compatibilité avec l’installation avant la pose."),
              ("Vous occupez-vous du carrelage ?", "Notre métier est le sanitaire. Pour le carrelage et les finitions, nous coordonnons nos interventions avec votre carreleur.")],
         photos=["salle-de-bains-sauge", "salle-de-bains-gros-oeuvre"]),
    dict(slug="chauffage", icon="radiator", art="radiator", title="Chauffage", short="Radiateurs · Sol · Distribution",
         spec="Pose · Remplacement · Équilibrage",
         card="Radiateurs, chauffage au sol, distribution, purge et équilibrage : une chaleur homogène, pièce par pièce.",
         h1="Un chauffage qui chauffe juste, pièce par pièce.",
         lead="Pose et remplacement de radiateurs, distribution, chauffage au sol, purge et équilibrage : nous intervenons sur les installations de chauffage à eau chaude, en neuf comme en rénovation.",
         mt="Chauffage : radiateurs, chauffage au sol, entretien",
         md="Installation et remplacement de radiateurs, chauffage au sol, purge et équilibrage à Prilly, Lausanne et environs. Bluetech Sanitaire, devis sans engagement.",
         items=[("Radiateurs", "Pose, remplacement et déplacement de radiateurs, vannes thermostatiques comprises."),
                ("Chauffage au sol", "Raccordement et équilibrage des collecteurs de chauffage au sol."),
                ("Distribution", "Conduites d’aller et de retour, isolation, raccordement aux collecteurs."),
                ("Purge & pression", "Élimination de l’air, contrôle et remise en pression du circuit."),
                ("Équilibrage", "Réglage hydraulique pour une chaleur homogène dans toutes les pièces."),
                ("Diagnostic", "Radiateur froid, bruits, pression qui chute : nous cherchons la cause.")],
         steps=[("Diagnostic", "Relevé de l’installation existante, de la pression et des circuits."),
                ("Proposition", "Solution chiffrée : réparation, remplacement ou modification."),
                ("Intervention", "Isolement du circuit, travaux, remplissage et purge."),
                ("Réglage", "Équilibrage, contrôle de la pression, essai de chaque radiateur.")],
         faq=[("Mon radiateur est froid en haut, que faire ?", "C’est souvent de l’air dans le circuit. Une purge règle généralement le problème ; si la pression chute ensuite, il faut la rétablir. Si le problème persiste, nous diagnostiquons l’installation."),
              ("Peut-on remplacer un radiateur sans vider toute l’installation ?", "Selon la configuration et la présence de vannes d’isolement, c’est souvent possible. Nous vous le confirmons lors de la visite."),
              ("Intervenez-vous sur le chauffage au sol ?", "Oui : raccordement, purge et équilibrage des circuits sur les collecteurs de chauffage au sol."),
              ("Travaillez-vous pour les immeubles et les PPE ?", "Oui, nous intervenons aussi bien pour des particuliers que pour des copropriétés et des régies.")],
         photos=["gaine-collecteurs"]),
    dict(slug="depannage", icon="tap", art="tap", title="Dépannage & réparations", short="Fuites · WC · Robinetterie",
         spec="Diagnostic · Réparation · Remplacement",
         card="Fuite, WC qui coule, écoulement bouché, plus d’eau chaude : diagnostic clair, réparation propre.",
         h1="Une fuite ? On s’en occupe.",
         lead="Robinet qui goutte, WC qui coule, écoulement bouché, raccord qui fuit : nous diagnostiquons, réparons ou remplaçons — et nous vous expliquons ce qui s’est passé.",
         mt="Dépannage sanitaire : fuites, WC, robinetterie",
         md="Dépannage sanitaire à Prilly, Lausanne et environs : fuites, WC qui coule, robinetterie, écoulements bouchés, eau chaude. Appelez ou écrivez sur WhatsApp.",
         items=[("Fuites", "Recherche et réparation de fuites sur robinetterie, raccords et conduites apparentes."),
                ("WC & chasses d’eau", "Mécanismes de chasse, robinets flotteurs, réservoirs encastrés : réglage ou remplacement."),
                ("Robinetterie", "Remplacement de cartouches, mitigeurs, flexibles et robinets d’arrêt."),
                ("Écoulements bouchés", "Débouchage de lavabos, éviers, douches et siphons."),
                ("Eau chaude", "Plus d’eau chaude ? Contrôle du boiler et de ses organes de sécurité."),
                ("Chauffage", "Radiateur froid ou pression en baisse : purge, remise en pression, diagnostic.")],
         steps=[("Vous nous contactez", "Par téléphone ou WhatsApp — une photo ou une vidéo nous aide beaucoup."),
                ("Diagnostic", "Nous identifions la cause, pas seulement le symptôme."),
                ("Réparation", "Nous vous expliquons la solution, puis nous réparons ou remplaçons."),
                ("Contrôle", "Essai, vérification d’étanchéité, lieux laissés propres.")],
         tips=[("Fermez l’eau", "Vanne d’arrêt sous l’appareil, sur le collecteur de l’appartement ou au compteur."),
               ("Coupez le courant", "Si l’eau approche d’une prise, d’un appareil ou d’un tableau électrique."),
               ("Protégez", "Épongez, déplacez ce qui craint l’eau, prévenez le voisin du dessous."),
               ("Photographiez", "Envoyez-nous une photo ou une vidéo sur WhatsApp : nous voyons tout de suite de quoi il s’agit.")],
         faq=[("Intervenez-vous rapidement ?", "Nous faisons le maximum pour intervenir au plus vite, selon l’urgence et nos disponibilités. Le plus efficace : nous appeler, ou nous écrire sur WhatsApp avec une photo."),
              ("Où se trouve ma vanne d’arrêt principale ?", "Le plus souvent près du compteur d’eau, à la cave ou dans une gaine technique. En appartement, il existe souvent des vannes sur le collecteur de l’étage et sous chaque appareil."),
              ("Connaîtrai-je le prix avant la réparation ?", "Nous vous expliquons le problème et la solution avant d’intervenir. Pour des travaux plus importants, vous recevez un devis."),
              ("Intervenez-vous pour les régies et les PPE ?", "Oui, pour les locataires, les propriétaires, les copropriétés et les régies.")],
         photos=["evacuations-controlees"]),
    dict(slug="entretien", icon="gauge", art="gauge", title="Entretien & maintenance", short="Préventif · Contrôles",
         spec="Détartrage · Sécurité · Robinetterie",
         card="Détartrage, organes de sécurité, robinetterie, chauffage : l’entretien qui évite les dépannages.",
         h1="L’entretien qui évite les dépannages.",
         lead="Une installation entretenue dure plus longtemps et consomme moins. Détartrage, contrôle des organes de sécurité, révision de la robinetterie : nous passons avant que le problème n’arrive.",
         mt="Entretien et maintenance sanitaire et chauffage",
         md="Entretien sanitaire et chauffage à Prilly, Lausanne et environs : détartrage de boilers, organes de sécurité, robinetterie, purge. Particuliers, PPE et régies.",
         items=[("Détartrage des boilers", "Vidange, détartrage, contrôle de l’anode et du corps de chauffe."),
                ("Organes de sécurité", "Groupes de sécurité, réducteurs de pression et vannes contrôlés."),
                ("Robinetterie", "Aérateurs nettoyés, joints et cartouches fatigués remplacés."),
                ("Chasses d’eau", "Réglage des mécanismes, contrôle d’étanchéité des réservoirs."),
                ("Chauffage", "Purge, contrôle de pression et des vannes thermostatiques."),
                ("Immeubles & PPE", "Entretien régulier pour propriétaires, copropriétés et régies, sur demande.")],
         steps=[("État des lieux", "Inventaire des appareils, de leur âge et de leur état."),
                ("Plan d’entretien", "Fréquence et contenu des visites définis ensemble."),
                ("Visites", "Contrôles, détartrage, remplacement des pièces d’usure."),
                ("Rapport", "Ce qui a été fait, ce qu’il faudra prévoir — par écrit.")],
         faq=[("À quelle fréquence détartrer un boiler ?", "Cela dépend de la dureté de l’eau et de la consommation ; dans la région lausannoise, un contrôle tous les quelques années est généralement recommandé. Nous vous conseillons selon votre installation."),
              ("Pourquoi entretenir une installation qui fonctionne ?", "Parce que le calcaire, l’usure des joints et les organes de sécurité grippés ne préviennent pas. Un contrôle régulier coûte moins cher qu’un dégât d’eau."),
              ("Proposez-vous des contrats d’entretien ?", "Oui, sur demande, pour les particuliers comme pour les immeubles. Nous définissons ensemble la fréquence et le contenu des visites.")],
         photos=["wc-bain-ventilation"]),
    dict(slug="boilers-eau-chaude", icon="boiler", art="boiler", title="Boilers & eau chaude", short="Remplacement · Détartrage",
         spec="Boiler · Pompe à chaleur · Sécurité",
         card="Remplacement, dimensionnement, boiler pompe à chaleur, détartrage : de l’eau chaude, tous les jours.",
         h1="De l’eau chaude, tous les jours, sans y penser.",
         lead="Remplacement de boilers, boilers pompe à chaleur, détartrage, groupe de sécurité : nous dimensionnons et installons votre production d’eau chaude sanitaire.",
         mt="Boilers : remplacement, détartrage, pompe à chaleur",
         md="Remplacement et détartrage de boilers, boilers pompe à chaleur, groupes de sécurité à Prilly, Lausanne et environs. Bluetech Sanitaire, devis sans engagement.",
         items=[("Remplacement de boiler", "Dépose de l’ancien boiler, pose et raccordement du nouveau, mise en service."),
                ("Dimensionnement", "Un volume adapté au nombre de personnes et à vos habitudes."),
                ("Boiler pompe à chaleur", "Conseil et installation de chauffe-eau thermodynamiques, plus économes."),
                ("Détartrage", "Vidange, détartrage, contrôle du corps de chauffe et de l’anode."),
                ("Groupe de sécurité", "Contrôle et remplacement des organes de sécurité."),
                ("Panne d’eau chaude", "Diagnostic de l’alimentation, du thermostat et du corps de chauffe.")],
         steps=[("Relevé", "Volume actuel, emplacement, raccordements, besoins du ménage."),
                ("Choix", "Boiler électrique ou pompe à chaleur : avantages et coûts comparés."),
                ("Remplacement", "Vidange, dépose, pose, raccordement hydraulique et sécurité."),
                ("Mise en service", "Remplissage, purge, contrôle, raccordement électrique par électricien agréé.")],
         faq=[("Quelle capacité de boiler choisir ?", "Cela dépend du nombre de personnes, de vos habitudes (bain ou douche) et de la place disponible. Nous dimensionnons le boiler avec vous lors du relevé."),
              ("Un boiler pompe à chaleur, c’est intéressant ?", "Il consomme nettement moins d’électricité qu’un boiler électrique classique. Il demande un local adapté (volume, température) : nous vérifions la faisabilité avec vous."),
              ("Le raccordement électrique est-il compris ?", "Le raccordement électrique est réalisé par un électricien agréé, avec qui nous coordonnons l’intervention."),
              ("Pourquoi détartrer son boiler ?", "Le calcaire isole le corps de chauffe : le boiler consomme plus et s’use plus vite. Un détartrage régulier prolonge sa durée de vie.")],
         photos=["mur-brique-geberit"]),
]
for k, s in enumerate(SERVICES):
    s["n"] = "%02d" % (k + 1)

# ------------------------------------------------------------------ work (the client's own photos, captions describe what is visible)
WORK = [
    ("wc-douche-collecteur", "Implantation tracée", "WC et douche implantés au trait sur le mur brut, collecteur de distribution en attente.", "encastre", 1200, 1600),
    ("evacuations-controlees", "Raccords contrôlés", "Évacuations posées et contrôlées raccord par raccord — chaque assemblage marqué « OK ».", "evac", 1440, 2048),
    ("salle-de-bains-sauge", "Salle de bains terminée", "Mosaïque vert sauge, lavabo suspendu, miroir lumineux et étagères en verre.", "sdb", 1500, 2000),
    ("double-bati-ventilation", "Gaine technique double", "Deux bâtis-supports, colonne de chute et ventilation réunis dans une même gaine.", "encastre", 1500, 2000),
    ("gaine-collecteurs", "Distribution par collecteurs", "Collecteurs eau froide / eau chaude et alimentations gainées vers chaque appareil.", "encastre", 1500, 2000),
    ("mur-brique-geberit", "Mur d’installation", "WC suspendu et attentes lavabo sur mur en brique, évacuations raccordées.", "encastre", 1500, 2000),
    ("salle-de-bains-gros-oeuvre", "Salle de bains au gros œuvre", "WC, lavabos et douche implantés avant la pose des plaques.", "sdb", 1500, 2000),
    ("colonne-chute", "Colonne de chute", "Colonne fixée, raccordée et prête pour l’habillage.", "evac", 1500, 2000),
    ("wc-bain-ventilation", "WC & attentes bain", "Bâti-support WC, attentes baignoire et colonne de chute, avant fermeture.", "encastre", 1200, 1600),
    ("bati-lavabo", "Bâti-support lavabo", "Lavabo implanté dans un local étroit, le long de la gaine de ventilation.", "encastre", 1200, 1600),
]
WORK_TAGS = [("all", "Tout"), ("encastre", "Installations encastrées"), ("evac", "Évacuations"), ("sdb", "Salles de bains")]

# ------------------------------------------------------------------ reviews — PLACEHOLDERS, swap for real Google reviews
REVIEWS_ARE_EXAMPLES = True
REVIEWS = [
    ("Prénom N.", "Rénovation de salle de bains", "Travail soigné du début à la fin. Le chantier était propre chaque soir et le planning a été respecté."),
    ("Prénom N.", "Dépannage", "Fuite sous l’évier réparée rapidement. Explications claires, prix annoncé avant l’intervention."),
    ("Prénom N.", "Boiler", "Remplacement de notre boiler en une matinée. Très professionnel, je recommande."),
    ("Prénom N.", "Installation sanitaire", "Excellente coordination avec notre architecte. Une équipe précise et à l’écoute."),
    ("Prénom N.", "Chauffage", "Radiateurs purgés et équilibrés : enfin la même chaleur dans toutes les pièces."),
    ("Prénom N.", "Entretien", "Détartrage et contrôle de l’installation sans mauvaise surprise. Ponctuel et efficace."),
    ("Prénom N.", "Rénovation de salle de bains", "Notre baignoire est devenue une douche de plain-pied magnifique. Merci pour le conseil."),
    ("Prénom N.", "Dépannage", "WC qui coulait depuis des semaines, réglé en une visite. Rapide et sympathique."),
]

# ------------------------------------------------------------------ area (inferred from the Prilly address — confirm with the owner)
TOWNS = [("Prilly", 46.5346, 6.6056, 1), ("Lausanne", 46.5197, 6.6323, 1), ("Renens", 46.5393, 6.5881, 0), ("Crissier", 46.5513, 6.5754, 0),
         ("Ecublens", 46.5279, 6.5615, 0), ("Chavannes", 46.5309, 6.5702, 0), ("Bussigny", 46.5507, 6.5528, 0),
         ("Le Mont", 46.5583, 6.6313, 0), ("Romanel", 46.5642, 6.6075, 0), ("Jouxtens", 46.5523, 6.5979, 0),
         ("Pully", 46.5101, 6.6618, 0), ("Epalinges", 46.5491, 6.6687, 0), ("Morges", 46.5113, 6.4985, 0), ("St-Sulpice", 46.5106, 6.5590, 0)]
SHORE = [(46.4995, 6.47), (46.5055, 6.497), (46.5085, 6.53), (46.5075, 6.556), (46.5113, 6.585), (46.5155, 6.598), (46.5135, 6.615), (46.5062, 6.626),
         (46.5065, 6.645), (46.5055, 6.663), (46.4985, 6.69), (46.49, 6.71)]

NAV = [("realisations", "Réalisations"), ("entreprise", "L’entreprise"), ("contact", "Contact")]

e = html.escape


def pic(name, alt, sizes="100vw", cls="", w=1500, h=2000, eager=False, attrs=""):
    """<picture> with webp + jpg, two widths."""
    R = "{R}"
    lo = "eager" if eager else "lazy"
    fp = ' fetchpriority="high"' if eager else ""
    sw = w if w <= 1500 else 1500
    return ('<picture%s><source type="image/webp" srcset="%sassets/img/work/%s-s.webp 760w, %sassets/img/work/%s.webp %dw" sizes="%s">'
            '<img src="%sassets/img/work/%s.jpg" srcset="%sassets/img/work/%s-s.jpg 760w, %sassets/img/work/%s.jpg %dw" sizes="%s" '
            'alt="%s" width="%d" height="%d" loading="%s" decoding="async"%s%s></picture>') % (
        (' class="%s"' % cls) if cls else "", R, name, R, name, sw, sizes, R, name, R, name, R, name, sw, sizes, e(alt), w, h, lo, fp, attrs)


def btn(href, label, cls="btn--blue", icon=ARROW, attrs=""):
    return '<a class="btn %s" href="%s"%s><span class="btn__fill"></span><span class="btn__t">%s</span>%s</a>' % (cls, href, attrs, label, icon)


def svc_url(s):
    return "{R}services/" + s["slug"]


# ------------------------------------------------------------------ shared chrome
def header(key):
    mega = "".join(
        '<a class="mega__i" href="%s"><span class="mega__ic">%s</span><span class="mega__t"><b>%s</b><em>%s</em></span><span class="mega__n">%s</span></a>'
        % (svc_url(s), SICON[s["icon"]], s["title"], s["short"], s["n"]) for s in SERVICES)
    nav = "".join('<a class="hd__link%s" href="{R}%s">%s</a>' % (" is-cur" if key == k else "", k, t) for k, t in NAV)
    msvc = "".join('<li><a href="%s"><span>%s</span>%s</a></li>' % (svc_url(s), s["n"], s["title"]) for s in SERVICES)
    return '''
<header class="hd" data-hd>
 <div class="hd__in">
  <a class="hd__logo" href="{HOME}" aria-label="Bluetech Sanitaire — accueil">%(logo)s</a>
  <nav class="hd__nav" aria-label="Navigation principale">
   <div class="hd__dd" data-dd>
    <button class="hd__link%(svccur)s" type="button" aria-expanded="false" aria-controls="mega" data-dd-btn>Services %(chev)s</button>
    <div class="mega" id="mega" data-mega>
     <div class="mega__in">
      <div class="mega__list">%(mega)s</div>
      <a class="mega__all" href="{R}services/"><span class="mono">06 départs</span><b>Tous les services</b>%(arrow)s</a>
     </div>
    </div>
   </div>
   %(nav)s
  </nav>
  <div class="hd__act">
   <a class="hd__tel" href="%(tel)s">%(phone)s<span>%(phd)s</span></a>
   <a class="btn btn--blue btn--sm hd__cta" href="{R}contact"><span class="btn__fill"></span><span class="btn__t">Demander un devis</span></a>
   <button class="hd__burger" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu" data-burger><span></span><span></span></button>
  </div>
 </div>
 <div class="hd__pipe" aria-hidden="true"><i data-progress></i></div>
</header>
<div class="menu" id="menu" data-menu aria-hidden="true">
 <div class="menu__in">
  <nav class="menu__nav" aria-label="Menu mobile">
   <a class="menu__big" href="{HOME}">Accueil</a>
   <a class="menu__big" href="{R}services/">Services</a>
   <ul class="menu__svc">%(msvc)s</ul>
   <a class="menu__big" href="{R}realisations">Réalisations</a>
   <a class="menu__big" href="{R}entreprise">L’entreprise</a>
   <a class="menu__big" href="{R}contact">Contact & devis</a>
  </nav>
  <div class="menu__foot">
   <a class="btn btn--blue" href="%(tel)s"><span class="btn__fill"></span><span class="btn__t">Appeler</span>%(phone)s</a>
   <a class="btn btn--wa" href="%(wa)s" target="_blank" rel="noopener"><span class="btn__fill"></span><span class="btn__t">WhatsApp</span>%(waic)s</a>
   <p class="mono">%(addr)s</p>
  </div>
 </div>
</div>''' % dict(logo=LOGO, chev=CHEV, mega=mega, arrow=ARROW, nav=nav, tel=TEL, phone=PHONE, phd=PHONE_DISPLAY, msvc=msvc,
                  wa=WA_HELLO, waic=WA, addr=e(ADDR), svccur=" is-cur" if key == "services" else "")


def footer():
    svc = "".join('<li><a href="%s">%s</a></li>' % (svc_url(s), s["title"]) for s in SERVICES)
    mail = ('<a href="mailto:%s">%s</a>' % (EMAIL, EMAIL)) if EMAIL else ""
    return '''
<footer class="ft">
 <div class="wrap">
  <div class="ft__top">
   <div class="ft__brand">
    <a class="ft__logo" href="{HOME}" aria-label="Bluetech Sanitaire — accueil">%(logo)s</a>
    <p>Installations sanitaires et de chauffage à Prilly et dans la région lausannoise.</p>
   </div>
   <nav class="ft__col" aria-label="Services"><p class="mono">Services</p><ul>%(svc)s</ul></nav>
   <nav class="ft__col" aria-label="Entreprise"><p class="mono">Entreprise</p><ul><li><a href="{R}realisations">Réalisations</a></li><li><a href="{R}entreprise">L’entreprise</a></li><li><a href="{R}contact">Contact & devis</a></li><li><a href="{R}mentions-legales">Mentions légales</a></li></ul></nav>
   <div class="ft__col"><p class="mono">Contact</p><ul><li><a href="%(tel)s">%(phd)s</a></li><li><a href="%(wa)s" target="_blank" rel="noopener">WhatsApp</a></li>%(mail)s<li><a href="%(maps)s" target="_blank" rel="noopener">%(street)s<br>%(zip)s %(city)s</a></li></ul></div>
  </div>
  <div class="cartouche" aria-label="Informations légales">
   <div class="c c--logo"><span class="mono">Entreprise</span><b>%(name)s</b></div>
   <div class="c"><span class="mono">Siège</span><b>%(street)s, %(zip)s %(city)s</b></div>
   <div class="c"><span class="mono">IDE</span><b>%(ide)s</b></div>
   <div class="c"><span class="mono">Projet</span><b>Votre installation</b></div>
   <div class="c"><span class="mono">Échelle</span><b>1 : 1</b></div>
   <div class="c"><span class="mono">Date</span><b data-today>2026</b></div>
  </div>
  <div class="ft__bot"><span>© <span data-year>2026</span> %(name)s</span><a href="{R}mentions-legales">Mentions légales & confidentialité</a></div>
 </div>
</footer>
<div class="fab" data-fab>
 <a class="fab__b fab__b--wa" href="%(wa)s" target="_blank" rel="noopener" aria-label="Écrire sur WhatsApp">%(waic)s<span class="fab__tip">WhatsApp</span></a>
 <a class="fab__b fab__b--tel" href="%(tel)s" aria-label="Appeler Bluetech Sanitaire">%(phone)s<span class="fab__tip">%(phd)s</span></a>
</div>
<nav class="dock" aria-label="Contact rapide" data-dock>
 <a href="%(tel)s">%(phone)s<span>Appeler</span></a>
 <a class="dock__wa" href="%(wa)s" target="_blank" rel="noopener">%(waic)s<span>WhatsApp</span></a>
 <a class="dock__cta" href="{R}contact">%(arrowur)s<span>Devis</span></a>
</nav>
<div class="sidepipe" aria-hidden="true"><i data-sidepipe></i><b></b></div>''' % dict(
        logo=LOGO, svc=svc, tel=TEL, phd=PHONE_DISPLAY, wa=WA_HELLO, waic=WA, phone=PHONE, mail=("<li>%s</li>" % mail) if mail else "",
        maps=MAPS, street=e(CO["street"]), zip=CO["zip"], city=CO["city"], name=e(CO["name"]), ide=CO["ide"], arrowur=ARROW_UR)


def jsonld_business():
    d = {"@context": "https://schema.org", "@type": "Plumber", "@id": BASE + "#entreprise", "name": CO["name"], "url": BASE,
         "logo": BASE + "assets/img/logo.svg", "image": BASE + "assets/img/og.jpg",
         "address": {"@type": "PostalAddress", "streetAddress": CO["street"], "postalCode": CO["zip"], "addressLocality": CO["city"],
                     "addressRegion": "VD", "addressCountry": "CH"},
         "geo": {"@type": "GeoCoordinates", "latitude": CO["lat"], "longitude": CO["lng"]},
         "areaServed": [t[0] for t in TOWNS[:12]], "foundingDate": CO["founded"], "taxID": CO["ide"],
         "founder": {"@type": "Person", "name": CO["manager"]},
         "knowsAbout": ["Installations sanitaires", "Chauffage", "Rénovation de salles de bains", "Dépannage sanitaire", "Boilers"]}
    if not PHONE_TEL.startswith("+41000"):
        d["telephone"] = PHONE_TEL
    if EMAIL:
        d["email"] = EMAIL
    return d


def render(path, title, desc, body, key="", jsonld=None, scripts="", body_cls="", og=None):
    depth = path.count("/")
    R = "../" * depth
    HOME = R or "./"
    clean = path[:-5] if path.endswith(".html") else path
    if clean.endswith("index"):
        clean = clean[:-5]
    canon = BASE + clean
    lds = [jsonld_business()] + (jsonld or [])
    head = '''<!doctype html>
<html lang="fr-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
%(robots)s<link rel="canonical" href="%(canon)s">
<meta name="theme-color" content="#F4F6F9">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_CH"><meta property="og:site_name" content="Bluetech Sanitaire">
<meta property="og:title" content="%(title)s"><meta property="og:description" content="%(desc)s"><meta property="og:url" content="%(canon)s">
<meta property="og:image" content="%(base)sassets/img/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="%(R)sassets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="%(R)sassets/img/apple-touch-icon.png">
<link rel="preload" href="%(R)sassets/fonts/cabinet-grotesk-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="%(R)sassets/fonts/general-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%(R)sassets/css/site.css?v=%(V)s">
<script>(function(d,l){var p=l.pathname;if(p.slice(-5)===".html"){history.replaceState(null,"",p.slice(-11)==="/index.html"?p.slice(0,-10):p.slice(0,-5)+l.search+l.hash)}d.documentElement.className+=" js pre-intro";window.__t0=Date.now()})(document,location)</script>
%(ld)s
</head>
<body class="%(bc)s" data-wa="%(wa)s" data-mail="%(mail)s">
<a class="skip" href="#main">Aller au contenu</a>
%(logosym)s
''' % dict(logosym=LOGO_SYMBOL, wa=WA_NUMBER, mail=EMAIL, title=e(title), desc=e(desc), canon=canon, base=BASE, R=R, V=V, bc=body_cls,
           robots='<meta name="robots" content="noindex, follow">\n' if NOINDEX else "",
           ld="\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in lds))
    tail = '''
<script src="%(R)sassets/js/vendor/gsap.min.js?v=%(V)s" defer></script>
<script src="%(R)sassets/js/vendor/ScrollTrigger.min.js?v=%(V)s" defer></script>
<script src="%(R)sassets/js/vendor/lenis.min.js?v=%(V)s" defer></script>
<script src="%(R)sassets/js/site.js?v=%(V)s" defer></script>
%(scripts)s
</body>
</html>
''' % dict(R=R, V=V, scripts=scripts.replace("{R}", R).replace("{V}", V))
    doc = head + header(key) + '\n<main id="main">\n' + body + '\n</main>\n' + footer() + tail
    doc = doc.replace("{HOME}", HOME).replace("{R}", R).replace("{RUN}", ART["run"])
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(doc)
    return clean


# ------------------------------------------------------------------ shared sections
def sec_head(num, label, title, text="", cls=""):
    return '<header class="sh-h %s"><p class="kicker"><span>[%s]</span> %s</p><h2 class="h2" data-split>%s</h2>%s</header>' % (
        cls, num, label, title, ('<p class="sh-h__p" data-r>%s</p>' % text) if text else "")


def cta_band():
    return '''
<section class="cta" data-cta>
 <canvas class="cta__gl" data-water aria-hidden="true"></canvas>
 <div class="cta__in wrap">
  <p class="kicker kicker--light" data-r><span>[—]</span> Une fuite, un projet, une question ?</p>
  <h2 class="cta__t" data-split>Parlons de votre installation.</h2>
  <p class="cta__p" data-r>Décrivez votre besoin en quelques mots — une photo suffit souvent pour un premier avis.</p>
  <div class="cta__b" data-r>
   %s
   <a class="btn btn--glass" href="%s"><span class="btn__fill"></span><span class="btn__t">Appeler</span>%s</a>
   <a class="btn btn--glass" href="%s" target="_blank" rel="noopener"><span class="btn__fill"></span><span class="btn__t">WhatsApp</span>%s</a>
  </div>
  <p class="cta__hint mono" aria-hidden="true"><i></i>Touchez l’eau</p>
 </div>
</section>''' % (btn("{R}contact", "Demander un devis", "btn--white"), TEL, PHONE, WA_HELLO, WA)


def reviews_section(num="06"):
    cards = []
    for name, svc, txt in REVIEWS:
        cards.append('''<article class="rv">
 <header class="rv__h"><span class="rv__av" aria-hidden="true">%s</span><span class="rv__n"><b>%s</b><em>%s</em></span>%s</header>
 %s
 <p>%s</p>
 %s
</article>''' % (name[0], e(name), e(svc), GOOGLE, STARS, e(txt), '<span class="rv__ex">Exemple</span>' if REVIEWS_ARE_EXAMPLES else ""))
    track = "".join(cards)
    write = ('<a class="btn btn--line btn--sm" href="%s" target="_blank" rel="noopener"><span class="btn__fill"></span><span class="btn__t">Laisser un avis</span>%s</a>' % (GOOGLE_REVIEWS_URL, ARROW_UR)) if GOOGLE_REVIEWS_URL else ""
    return '''
<section class="rev sec" data-rev>
 <div class="wrap rev__top">
  %s
  <div class="gsum" data-r>
   %s
   <div><b>Avis Google</b>%s<span>Les premiers avis de nos clients arrivent bientôt.</span></div>
   %s
  </div>
 </div>
 <div class="rev__rail" data-rail tabindex="0" aria-label="Avis clients, défilement horizontal">
  <div class="rev__track" data-track>%s</div>
 </div>
 <div class="wrap rev__ctl"><button class="rbtn" type="button" data-rail-prev aria-label="Avis précédents">%s</button><button class="rbtn" type="button" data-rail-next aria-label="Avis suivants">%s</button></div>
</section>''' % (sec_head(num, "Avis clients", "La parole est à nos clients."), GOOGLE, STARS, write, track, LEFT, RIGHT)


def zone_section(num="07"):
    # equirectangular projection around Prilly
    lat0, lng0 = 46.535, 6.595
    kx = 6500 * math.cos(math.radians(lat0)); ky = 6500
    cx, cy = 290, 236
    def P(la, ln):
        return cx + (ln - lng0) * kx, cy - (la - lat0) * ky
    shore = " ".join("%.1f,%.1f" % P(la, ln) for la, ln in SHORE)
    lake = "M%s L640,560 L-40,560 Z" % shore.replace(" ", " L")
    hq = P(CO["lat"], CO["lng"])
    towns = []
    for name, la, ln, big in TOWNS:
        x, y = P(la, ln)
        if not (-10 < x < 610 and -10 < y < 470):
            continue
        anchor = "start" if x < 520 else "end"
        dx = 9 if anchor == "start" else -9
        towns.append('<g class="tw%s"><circle cx="%.1f" cy="%.1f" r="%s"/><text x="%.1f" y="%.1f" text-anchor="%s">%s</text></g>' % (
            " tw--big" if big else "", x, y, 3.2 if big else 2.4, x + dx, y + 4, anchor, name))
    chips = "".join("<li>%s</li>" % t[0] for t in TOWNS)
    return '''
<section class="zone sec">
 <div class="wrap zone__g">
  <div class="zone__t">
   %s
   <ul class="chips" data-r>%s</ul>
   <a class="addr" href="%s" target="_blank" rel="noopener" data-r>%s<span><b>%s</b>%s</span>%s</a>
  </div>
  <figure class="zone__map" data-r>
   <svg viewBox="0 0 600 460" role="img" aria-label="Carte : Prilly et les communes voisines, au bord du Léman">
    <defs><pattern id="zg" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none"/></pattern></defs>
    <rect class="zone__grid" width="600" height="460" fill="url(#zg)"/>
    <path class="lake" d="%s"/>
    <text class="lake__t" x="420" y="420">LAC LÉMAN</text>
    <g class="rip" transform="translate(%.1f %.1f)"><circle r="40"/><circle r="40"/><circle r="40"/><circle r="40"/></g>
    %s
    <g class="hq" transform="translate(%.1f %.1f)"><circle r="7"/><circle r="15" class="hq__r"/><text x="14" y="-14">BLUETECH</text></g>
    <g class="compass" transform="translate(560 40)"><path d="M0 -16 L5 0 L0 16 L-5 0Z"/><text y="-22" text-anchor="middle">N</text></g>
   </svg>
   <figcaption class="mono">46.5286° N · 6.6034° E — Route de Renens 2, Prilly</figcaption>
  </figure>
 </div>
</section>''' % (sec_head(num, "Zone d’intervention", "Depuis Prilly, au cœur de l’Ouest lausannois.",
                      "Notre atelier est à deux pas de Malley. Nous intervenons à Prilly, à Lausanne et dans les communes voisines — n’hésitez pas à nous demander pour une adresse plus éloignée."),
                 chips, MAPS, PIN, e(CO["name"]), e(ADDR), ARROW_UR, lake, hq[0], hq[1], "".join(towns), hq[0], hq[1])


def process_section(num="05", title="Quatre étapes, aucune approximation.", steps=None, label="Méthode"):
    steps = steps or [
        ("Visite & relevé", "Nous venons voir, mesurons et écoutons. Pas de devis à l’aveugle.", "Sur place"),
        ("Devis détaillé", "Poste par poste, avec un planning réaliste. Vous savez ce que vous payez.", "Sans engagement"),
        ("Implantation & pose", "Axes tracés au mur, réseaux fixés et repérés, raccords marqués un à un.", "Comme sur nos photos"),
        ("Essai & mise en service", "Mise en pression et contrôle d’étanchéité avant fermeture, puis lieux rendus propres.", "Étanche"),
    ]
    ticks = []
    for k in range(51):
        a = math.radians(135 + k * 270 / 50)
        r1 = 150; r2 = 132 if k % 5 == 0 else 140
        ticks.append('<path class="%s" d="M%.1f %.1fL%.1f %.1f"/>' % ("tk tk--m" if k % 5 == 0 else "tk", 200 + r1 * math.cos(a), 200 + r1 * math.sin(a), 200 + r2 * math.cos(a), 200 + r2 * math.sin(a)))
    nums = []
    for k in range(11):
        a = math.radians(135 + k * 27)
        nums.append('<text x="%.1f" y="%.1f">%d</text>' % (200 + 114 * math.cos(a), 200 + 114 * math.sin(a) + 5, k))
    def arc(r, a0, a1):
        x0, y0 = 200 + r * math.cos(math.radians(a0)), 200 + r * math.sin(math.radians(a0))
        x1, y1 = 200 + r * math.cos(math.radians(a1)), 200 + r * math.sin(math.radians(a1))
        return "M%.1f %.1fA%d %d 0 %d 1 %.1f %.1f" % (x0, y0, r, r, 1 if a1 - a0 > 180 else 0, x1, y1)
    li = "".join('''<li class="step" data-step>
 <span class="step__n mono">%02d</span>
 <div><h3>%s</h3><p>%s</p><span class="step__tag mono">%s</span></div>
</li>''' % (k + 1, t, p, tag) for k, (t, p, tag) in enumerate(steps))
    return '''
<section class="proc sec" data-proc>
 <div class="wrap proc__g">
  <div class="proc__l">
   %s
   <div class="gauge" data-gauge>
    <svg viewBox="0 0 400 400" aria-hidden="true">
     <circle class="gauge__rim" cx="200" cy="200" r="186"/>
     <circle class="gauge__face" cx="200" cy="200" r="170"/>
     <path class="gauge__track" d="%s"/>
     <path class="gauge__prog" d="%s" pathLength="1" data-gauge-prog/>
     <path class="gauge__ok" d="%s"/>
     %s
     <g class="gauge__nums">%s</g>
     <text class="gauge__unit" x="200" y="158">bar</text>
     <g class="gauge__needle" data-needle><path d="M200 214 L196 200 L200 64 L204 200 Z"/><circle cx="200" cy="200" r="13"/><circle class="gauge__pin" cx="200" cy="200" r="4"/></g>
    </svg>
    <div class="gauge__read"><span class="mono" data-gauge-step>Étape 01 / 04</span><b class="gauge__ok-stamp" data-ok>OK</b></div>
   </div>
  </div>
  <ol class="proc__steps">%s</ol>
 </div>
</section>''' % (sec_head(num, label, title), arc(160, 135, 405), arc(160, 135, 405), arc(160, 351, 405), "".join(ticks), "".join(nums), li)


def faq_block(faq):
    return '<div class="faq">' + "".join('''<details class="faq__i" data-r><summary><span>%s</span><i>%s</i></summary><div class="faq__a"><p>%s</p></div></details>''' % (q, PLUS, a) for q, a in faq) + '</div>'


def quick_form(service_title="", ident="qf"):
    opts = "".join('<option%s>%s</option>' % (" selected" if s["title"] == service_title else "", s["title"]) for s in SERVICES)
    return '''
<form class="qform" data-form="quick" novalidate>
 <div class="f2">
  <label class="fld"><span>Nom</span><input name="nom" autocomplete="name" required placeholder="Votre nom"></label>
  <label class="fld"><span>Téléphone</span><input name="tel" type="tel" autocomplete="tel" required placeholder="079 123 45 67"></label>
 </div>
 <label class="fld"><span>Service</span><select name="service">%s<option>Autre demande</option></select></label>
 <label class="fld"><span>Votre demande</span><textarea name="message" rows="4" required placeholder="Décrivez votre besoin en quelques mots…"></textarea></label>
 <div class="qform__send">
  <button class="btn btn--blue" type="submit" data-via="wa"><span class="btn__fill"></span><span class="btn__t">Envoyer sur WhatsApp</span>%s</button>
  %s
 </div>
 <p class="form__note">Votre message s’ouvre dans WhatsApp%s, prêt à être envoyé. Rien n’est enregistré sur ce site.</p>
 <p class="form__ok" role="status" aria-live="polite"></p>
</form>''' % (opts, WA, ('<button class="btn btn--line" type="submit" data-via="mail"><span class="btn__fill"></span><span class="btn__t">Par e-mail</span>%s</button>' % MAIL) if EMAIL else "", " ou votre messagerie" if EMAIL else "")


# ------------------------------------------------------------------ x-ray schematic (aligned on salle-de-bains-sauge, 1500×2000)
XRAY_SVG = '''<svg class="xr" viewBox="0 0 1500 2000" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
 <defs><pattern id="xg" width="50" height="50" patternUnits="userSpaceOnUse"><path d="M50 0H0V50" fill="none"/></pattern></defs>
 <rect class="xr__grid" width="1500" height="2000" fill="url(#xg)"/>
 <g class="xr__ax"><path d="M800 1080V1990"/><path d="M770 1110l60 60M830 1110l-60 60"/><text x="820" y="1100">AXE LAVABO</text></g>
 <g class="xr__frame"><rect x="520" y="1090" width="560" height="700" rx="6"/><path d="M520 1560h560M560 1790v60M1040 1790v60"/></g>
 <text class="xr__t" x="1090" y="1600">BÂTI-SUPPORT</text>
 <g class="xr__box"><rect x="70" y="1820" width="190" height="120" rx="8"/><path d="M95 1860h140M95 1900h140"/><text x="70" y="1800">COLLECTEUR EF / EC</text></g>
 <path class="xr__p xr__p--c" d="M260 1862H700V1600"/><path class="xr__f xr__f--c" d="M260 1862H700V1600"/>
 <path class="xr__p xr__p--h" d="M260 1902H860V1600"/><path class="xr__f xr__f--h" d="M260 1902H860V1600"/>
 <g class="xr__v"><circle cx="700" cy="1590" r="16"/><circle cx="860" cy="1590" r="16"/></g>
 <path class="xr__flex xr__p--c" d="M700 1574C700 1440 735 1380 738 1272"/>
 <path class="xr__flex xr__p--h" d="M860 1574C860 1440 768 1380 764 1272"/>
 <path class="xr__p xr__p--d" d="M790 1560V1690H1010V2000"/><path class="xr__f xr__f--d" d="M790 1560V1690H1010V2000"/>
 <path class="xr__p xr__p--r" d="M1060 1940H1290V2000"/><path class="xr__p xr__p--r" d="M1060 1975H1440V2000"/>
 <g class="xr__lab">
  <text x="300" y="1846">EAU FROIDE Ø 16</text>
  <text x="300" y="1940">EAU CHAUDE Ø 16</text>
  <text x="1030" y="1676">ÉVACUATION PE Ø 50</text>
  <text x="1080" y="1930">CHAUFFAGE ALLER / RETOUR</text>
  <text x="880" y="1610">VANNES D’ARRÊT</text>
 </g>
 <text class="xr__stamp" x="70" y="140">SCHÉMA DE PRINCIPE</text>
</svg>'''


# ------------------------------------------------------------------ pages
def page_home():
    svc_rows = "".join('''
   <a class="mani__row" href="%s" data-mani-row>
    <span class="mani__br" aria-hidden="true"><i></i><span class="mani__valve"><i></i></span></span>
    <span class="mani__n mono">%s</span>
    <span class="mani__ic">%s</span>
    <span class="mani__t"><b>%s</b><em class="mono">%s</em></span>
    <span class="mani__d">%s</span>
    <span class="mani__go">%s</span>
   </a>''' % (svc_url(s), s["n"], SICON[s["icon"]], s["title"], s["spec"], s["card"], ARROW) for s in SERVICES)
    work = "".join('''
    <figure class="wc" data-wc>
     <a class="wc__ph" href="{R}realisations#%s">%s<span class="crop" aria-hidden="true"></span></a>
     <figcaption><span class="mono">R—%02d</span><b>%s</b><span>%s</span></figcaption>
    </figure>''' % (n, pic(n, t + " — " + c, "(max-width: 900px) 78vw, 30vw", w=w, h=h), k + 1, t, c) for k, (n, t, c, tag, w, h) in enumerate(WORK[:8]))
    fiche = [("Raison sociale", CO["name"]), ("Siège", ADDR), ("Direction", CO["manager"] + ", associé-gérant"),
             ("Domaines", "Installations sanitaires · Chauffage"), ("Interventions", "Neuf · Rénovation · Entretien · Dépannage"), ("IDE", CO["ide"])]
    fiche_html = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in fiche)
    body = '''
<section class="hero" data-hero>
 <div class="hero__grid" aria-hidden="true"></div>
 <div class="hero__glow" aria-hidden="true"></div>
 <canvas class="hero__gl" data-gl aria-hidden="true"></canvas>
 <svg class="hero__fallback" viewBox="0 0 480 480" aria-hidden="true"><use href="#fallback"/></svg>
 <div class="hero__co" data-callouts aria-hidden="true">
  <div class="co co--l" data-co="valve"><i></i><span class="co__l"></span><span class="co__t"><b>Vanne ¼ de tour</b><em data-valve-hint>Touchez pour fermer</em></span></div>
  <div class="co" data-co="gauge"><i></i><span class="co__l"></span><span class="co__t"><b>Manomètre</b><em data-bar>0,0 bar</em></span></div>
  <div class="co" data-co="mani"><i></i><span class="co__l"></span><span class="co__t"><b>Collecteur laiton</b><em>5 départs · PE-X Ø 16</em></span></div>
 </div>
 <div class="hero__in wrap">
  <p class="kicker" data-intro><span>[Prilly · VD]</span> Sanitaire & chauffage</p>
  <h1 class="hero__t" data-intro data-split>La précision derrière chaque mur.</h1>
  <p class="hero__p" data-intro>Bluetech Sanitaire installe, rénove et entretient vos installations sanitaires et de chauffage, à Prilly et dans toute la région lausannoise.</p>
  <div class="hero__b" data-intro>
   %(cta1)s
   <a class="btn btn--line" href="{R}realisations"><span class="btn__fill"></span><span class="btn__t">Nos réalisations</span>%(arrow)s</a>
  </div>
 </div>
 <ul class="hero__spec wrap" data-intro>
  <li><span class="mono">Siège</span>Route de Renens 2, Prilly</li>
  <li><span class="mono">Domaines</span>Sanitaire · Chauffage</li>
  <li><span class="mono">IDE</span>%(ide)s</li>
  <li><span class="mono">Devis</span>Sans engagement</li>
 </ul>
 <div class="hero__scroll" aria-hidden="true"><span class="mono">Défiler</span><i></i></div>
</section>

<section class="intro sec">
 <div class="wrap intro__g">
  <p class="kicker" data-r><span>[01]</span> L’entreprise</p>
  <h2 class="intro__big" data-split>Une installation sanitaire réussie ne se remarque pas. Elle fonctionne — chaque jour, pendant des décennies.</h2>
  <div class="intro__txt" data-r>
   <p>Bluetech Sanitaire est une entreprise de Prilly spécialisée dans les installations sanitaires et de chauffage. Nous posons, rénovons, entretenons et dépannons — avec la même rigueur sur un chantier neuf que pour une fuite sous un évier.</p>
   <p>Nos photos de chantier le montrent : axes tracés au mur, conduites repérées, raccords contrôlés et marqués. C’est ce travail invisible qui fait durer une installation.</p>
   <a class="tlink" href="{R}entreprise">Découvrir l’entreprise %(arrow)s</a>
  </div>
  <div class="fiche" data-r>
   <p class="mono fiche__h">Fiche technique <span>BTS — 2026</span></p>
   <dl>%(fiche)s</dl>
  </div>
 </div>
</section>

<section class="svc sec" id="services">
 <div class="wrap">
  %(svchead)s
  <div class="mani" data-mani>
   <div class="mani__in" aria-hidden="true"><span class="mono">Arrivée</span></div>
   <div class="mani__pipe" aria-hidden="true"><i data-mani-water></i></div>
   %(rows)s
  </div>
 </div>
</section>

<section class="xray sec sec--navy" data-xray>
 <div class="wrap xray__g">
  <div class="xray__txt">
   <p class="kicker kicker--light" data-r><span>[03]</span> Rayons X</p>
   <h2 class="h2" data-split>Le plus important ne se voit pas.</h2>
   <p data-r>Une salle de bains se juge sur ses finitions. Sa durée de vie, elle, se décide avant : dans la gaine technique, derrière le carrelage, dans chaque raccord.</p>
   <p class="xray__how mono" data-r><span class="only-fine">Passez la souris sur la photo</span><span class="only-coarse">Glissez le doigt sur la photo</span> pour voir à travers le mur.</p>
   <ul class="legend" data-r>
    <li><i class="lg lg--c"></i>Eau froide</li><li><i class="lg lg--h"></i>Eau chaude</li><li><i class="lg lg--d"></i>Évacuation</li><li><i class="lg lg--r"></i>Chauffage</li>
   </ul>
   <button class="btn btn--glass btn--sm" type="button" data-xray-toggle aria-pressed="false"><span class="btn__fill"></span><span class="btn__t">Tout révéler</span></button>
  </div>
  <figure class="xray__fig" data-xray-fig>
   <div class="xray__stage" data-xray-stage>
    %(xpic)s
    <div class="xray__lens" data-lens>
     <div class="xray__dark">%(xpic2)s</div>
     %(xsvg)s
    </div>
    <div class="xray__ring" data-ring aria-hidden="true"><span class="mono">X</span></div>
   </div>
   <figcaption class="mono">Salle de bains terminée — schéma de principe des réseaux encastrés</figcaption>
  </figure>
 </div>
</section>

<section class="work sec" data-work>
 <div class="wrap work__top">
  %(workhead)s
  <a class="tlink" href="{R}realisations" data-r>Toutes les réalisations %(arrow)s</a>
 </div>
 <div class="work__pin" data-work-pin>
  <div class="work__track" data-work-track>
   %(work)s
   <a class="wc wc--end" href="{R}realisations"><span class="mono">%(nwork)s photos</span><b>Voir toutes les réalisations</b>%(arrow)s</a>
  </div>
 </div>
 <div class="work__bar wrap" aria-hidden="true"><i data-work-bar></i></div>
</section>

%(process)s
%(reviews)s
%(zone)s
%(cta)s
''' % dict(cta1=btn("{R}contact", "Demander un devis"), arrow=ARROW, ide=CO["ide"], fiche=fiche_html,
           svchead=sec_head("02", "Services", "Six départs, une même exigence.", "Comme un collecteur distribue l’eau vers chaque appareil, nos six domaines partent du même point : un travail propre, contrôlé et expliqué."),
           rows=svc_rows, xsvg=XRAY_SVG,
           xpic=pic("salle-de-bains-sauge", "Salle de bains terminée : mosaïque vert sauge, lavabo suspendu et miroir rond lumineux", "(max-width: 900px) 92vw, 46vw", cls="xray__base"),
           xpic2=pic("salle-de-bains-sauge", "", "(max-width: 900px) 92vw, 46vw"),
           workhead=sec_head("04", "Réalisations", "Avant que les murs ne se referment.", "Nous photographions nos installations avant la fermeture des parois. C’est là que se voit la qualité d’un travail."),
           work=work, nwork=len(WORK), process=process_section(), reviews=reviews_section(), zone=zone_section(), cta=cta_band())
    body = FALLBACK_SYMBOL + body
    return render("index.html", "Bluetech Sanitaire — Installations sanitaires & chauffage à Prilly",
                  "Bluetech Sanitaire Sàrl, Prilly (VD) : installations sanitaires, rénovation de salles de bains, chauffage, dépannage, entretien et boilers à Lausanne et environs. Devis sans engagement.",
                  body, key="home", body_cls="p-home",
                  scripts='<script type="module" src="{R}assets/js/hero3d.js?v={V}"></script>')


FALLBACK_SYMBOL = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="fallback" viewBox="0 0 480 480">
<g fill="none" stroke="#2A5598" stroke-width="2" stroke-linecap="round"><path d="M40 120h120a30 30 0 0 1 30 30v10"/><rect x="170" y="160" width="240" height="40" rx="8"/>
<path d="M210 200v60c0 40-30 60-30 120M260 200v60c0 40 0 60 0 120M310 200v60c0 40 30 60 30 120M360 200v60c0 40 60 60 60 120"/><circle cx="290" cy="120" r="34"/><path d="M290 154v6M290 120l18-14"/></g></symbol></svg>'''


def page_service(s):
    others = [o for o in SERVICES if o is not s]
    items = "".join('<li class="it" data-r><span class="it__c mono">%s.%d</span><h3>%s</h3><p>%s</p></li>' % (s["n"], k + 1, t, p) for k, (t, p) in enumerate(s["items"]))
    photos = s["photos"]
    wmap = {w[0]: w for w in WORK}
    band = "".join('<figure class="band__f" data-r>%s<figcaption><span class="mono">%s</span>%s</figcaption></figure>' % (
        pic(p, wmap[p][1] + " — " + wmap[p][2], "(max-width: 900px) 92vw, 46vw", w=wmap[p][4], h=wmap[p][5]), wmap[p][1], wmap[p][2]) for p in photos)
    tips = ""
    if s.get("tips"):
        tips = '''
<section class="tips sec sec--navy">
 <div class="wrap">
  %s
  <ol class="tips__l">%s</ol>
  <div class="tips__b" data-r><a class="btn btn--white" href="%s"><span class="btn__fill"></span><span class="btn__t">Appeler maintenant</span>%s</a><a class="btn btn--wa" href="%s" target="_blank" rel="noopener"><span class="btn__fill"></span><span class="btn__t">Envoyer une photo</span>%s</a></div>
 </div>
</section>''' % (sec_head("!", "En cas de fuite", "Les bons réflexes, avant notre arrivée.", cls="sh-h--light"),
                 "".join('<li data-r><span class="mono">%02d</span><b>%s</b><p>%s</p></li>' % (k + 1, t, p) for k, (t, p) in enumerate(s["tips"])),
                 TEL, PHONE, wa("Bonjour Bluetech, j’ai une fuite : "), WA)
    rel = "".join('<a class="rel" href="%s"><span class="rel__n mono">%s</span><span class="rel__ic">%s</span><b>%s</b><em>%s</em>%s</a>' % (
        svc_url(o), o["n"], SICON[o["icon"]], o["title"], o["short"], ARROW) for o in others)
    steps = [(t, p, "Étape %02d" % (k + 1)) for k, (t, p) in enumerate(s["steps"])]
    body = '''
<section class="sv-hero">
 <div class="hero__grid" aria-hidden="true"></div>
 <div class="wrap sv-hero__g">
  <div class="sv-hero__t">
   <nav class="crumbs mono" aria-label="Fil d’Ariane" data-intro><a href="{HOME}">Accueil</a><span>/</span><a href="{R}services/">Services</a><span>/</span><span aria-current="page">%(title)s</span></nav>
   <p class="kicker" data-intro><span>[Service %(n)s / 06]</span> %(short)s</p>
   <h1 class="sv-hero__h" data-intro data-split>%(h1)s</h1>
   <p class="sv-hero__p" data-intro>%(lead)s</p>
   <div class="hero__b" data-intro>%(cta)s<a class="btn btn--line" href="%(tel)s"><span class="btn__fill"></span><span class="btn__t">Appeler</span>%(phone)s</a></div>
  </div>
  <div class="sv-hero__art" data-intro data-art>%(art)s<span class="sv-hero__spec mono">%(spec)s</span></div>
 </div>
</section>

<section class="band sec">
 <div class="wrap band__g band__g--%(nph)d">%(band)s</div>
</section>

<section class="items sec">
 <div class="wrap">
  %(ihead)s
  <ul class="items__l">%(items)s</ul>
 </div>
</section>
%(tips)s
%(process)s

<section class="faqs sec">
 <div class="wrap faqs__g">
  %(fhead)s
  %(faq)s
 </div>
</section>

<section class="ask sec sec--paper">
 <div class="wrap ask__g">
  <div>
   %(ahead)s
   <ul class="ask__c" data-r>
    <li><a href="%(tel)s">%(phone)s<span><b>Téléphone</b>%(phd)s</span></a></li>
    <li><a href="%(wa)s" target="_blank" rel="noopener">%(waic)s<span><b>WhatsApp</b>Photos et vidéos bienvenues</span></a></li>
    <li><a href="%(maps)s" target="_blank" rel="noopener">%(pin)s<span><b>Adresse</b>%(addr)s</span></a></li>
   </ul>
  </div>
  <div class="ask__f" data-r>%(form)s</div>
 </div>
</section>

<section class="rels sec">
 <div class="wrap">
  %(rhead)s
  <div class="rels__l">%(rel)s</div>
 </div>
</section>
%(ctab)s
''' % dict(title=s["title"], n=s["n"], short=s["short"], h1=s["h1"], lead=s["lead"], cta=btn("{R}contact?service=" + s["slug"], "Demander un devis"),
           tel=TEL, phone=PHONE, art=ART[s["art"]], spec=s["spec"], band=band, nph=len(photos),
           ihead=sec_head("01", "Prestations", "Ce que nous faisons."), items=items, tips=tips,
           process=process_section("02", "Comment ça se passe.", steps, "Déroulement"),
           fhead=sec_head("03", "Questions fréquentes", "Vos questions, nos réponses."), faq=faq_block(s["faq"]),
           ahead=sec_head("04", "Demande", "Un projet, une question ?", "Laissez-nous quelques mots : nous vous recontactons pour en parler."),
           phd=PHONE_DISPLAY, wa=WA_HELLO, waic=WA, maps=MAPS, pin=PIN, addr=e(ADDR), form=quick_form(s["title"]),
           rhead=sec_head("05", "Autres services", "Les autres départs du collecteur."), rel=rel, ctab=cta_band())
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]}
    svld = {"@context": "https://schema.org", "@type": "Service", "name": s["title"], "serviceType": s["title"], "description": s["md"],
            "provider": {"@id": BASE + "#entreprise"}, "areaServed": "Prilly, Lausanne et environs"}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Services", "item": BASE + "services/"},
        {"@type": "ListItem", "position": 3, "name": s["title"], "item": BASE + "services/" + s["slug"]}]}
    return render("services/%s.html" % s["slug"], s["mt"] + " | Bluetech Sanitaire", s["md"], body, key="services",
                  jsonld=[svld, faqld, bc], body_cls="p-service")


def deco(body):
    return body.replace("{RUN}", ART["run"])


def page_services():
    cards = "".join('''<a class="scard" href="%s" data-r>
 <span class="scard__top"><span class="mono">%s</span><span class="scard__ic">%s</span></span>
 <span class="scard__art" aria-hidden="true">%s</span>
 <b>%s</b><em class="mono">%s</em><span class="scard__p">%s</span><span class="scard__go">Découvrir %s</span>
</a>''' % (svc_url(s), s["n"], SICON[s["icon"]], ART[s["art"]], s["title"], s["spec"], s["card"], ARROW) for s in SERVICES)
    body = '''
<section class="pg-hero">
 <div class="hero__grid" aria-hidden="true"></div>
 <div class="pg-hero__art" data-art data-intro aria-hidden="true">{RUN}</div>
 <div class="wrap">
  <nav class="crumbs mono" aria-label="Fil d’Ariane" data-intro><a href="{HOME}">Accueil</a><span>/</span><span aria-current="page">Services</span></nav>
  <p class="kicker" data-intro><span>[06 départs]</span> Sanitaire & chauffage</p>
  <h1 class="pg-hero__h" data-intro data-split>Six services, une même exigence.</h1>
  <p class="pg-hero__p" data-intro>Installation, rénovation, chauffage, dépannage, entretien, eau chaude : tout ce qui transporte l’eau dans votre bâtiment, posé et contrôlé avec le même soin.</p>
 </div>
</section>
<section class="sec scards">
 <div class="wrap scards__g">%s</div>
</section>
%s
%s''' % (cards, process_section("—"), cta_band())
    return render("services/index.html", "Services : sanitaire, chauffage, dépannage | Bluetech Sanitaire",
                  "Installations sanitaires, rénovation de salles de bains, chauffage, dépannage, entretien et boilers à Prilly, Lausanne et environs.",
                  body, key="services", body_cls="p-services")


def page_work():
    filt = "".join('<button type="button" class="fbtn%s" data-filter="%s" aria-pressed="%s">%s<span>%d</span></button>' % (
        " is-on" if k == "all" else "", k, "true" if k == "all" else "false", t, len(WORK) if k == "all" else sum(1 for w in WORK if w[3] == k)) for k, t in WORK_TAGS)
    grid = "".join('''<figure class="gi gi--%d" id="%s" data-tag="%s" data-r>
 <button type="button" class="gi__b" data-lb="%d" aria-label="Agrandir : %s">%s<span class="crop" aria-hidden="true"></span><span class="gi__z">%s</span></button>
 <figcaption><span class="mono">R—%02d</span><b>%s</b><span>%s</span></figcaption>
</figure>''' % (k % 5, n, tag, k, e(t), pic(n, t + " — " + c, "(max-width: 640px) 92vw, (max-width: 1100px) 46vw, 30vw", w=w, h=h), PLUS, k + 1, t, c) for k, (n, t, c, tag, w, h) in enumerate(WORK))
    data = json.dumps([{"n": n, "t": t, "c": c} for n, t, c, tag, w, h in WORK], ensure_ascii=False)
    body = '''
<section class="pg-hero">
 <div class="hero__grid" aria-hidden="true"></div>
 <div class="pg-hero__art" data-art data-intro aria-hidden="true">{RUN}</div>
 <div class="wrap">
  <nav class="crumbs mono" aria-label="Fil d’Ariane" data-intro><a href="{HOME}">Accueil</a><span>/</span><span aria-current="page">Réalisations</span></nav>
  <p class="kicker" data-intro><span>[%d photos]</span> Chantiers Bluetech</p>
  <h1 class="pg-hero__h" data-intro data-split>Le travail, avant qu’il ne disparaisse.</h1>
  <p class="pg-hero__p" data-intro>Une fois les plaques posées et le carrelage terminé, plus personne ne voit les réseaux. Nous les photographions avant : axes tracés, conduites repérées, raccords marqués « OK ».</p>
 </div>
</section>
<section class="sec gal">
 <div class="wrap">
  <div class="filters" role="group" aria-label="Filtrer les réalisations" data-r>%s</div>
  <div class="gal__g" data-gal>%s</div>
 </div>
</section>
<div class="lb" data-lb-box role="dialog" aria-modal="true" aria-label="Photo agrandie" hidden>
 <button class="lb__x" type="button" data-lb-close aria-label="Fermer">%s</button>
 <button class="lb__p" type="button" data-lb-prev aria-label="Photo précédente">%s</button>
 <figure class="lb__f"><img alt="" data-lb-img><figcaption><span class="mono" data-lb-n></span><b data-lb-t></b><span data-lb-c></span></figcaption></figure>
 <button class="lb__n" type="button" data-lb-next aria-label="Photo suivante">%s</button>
</div>
<script type="application/json" id="work-data">%s</script>
%s
%s''' % (len(WORK), filt, grid, CLOSE, LEFT, RIGHT, data, reviews_section("—"), cta_band())
    return render("realisations.html", "Réalisations : nos chantiers sanitaires | Bluetech Sanitaire",
                  "Photos de chantiers Bluetech Sanitaire : installations encastrées, collecteurs, évacuations, bâtis-supports et salles de bains, à Prilly et environs.",
                  body, key="realisations", body_cls="p-work")


def page_company():
    values = [("Précision", "Axes tracés, pentes respectées, raccords contrôlés. Le millimètre compte, même derrière un mur."),
              ("Propreté", "Protection des lieux, rangement chaque soir, lieux rendus propres. Vous vivez chez vous pendant les travaux."),
              ("Transparence", "Devis détaillé, explications claires, aucune surprise. Vous savez ce que nous faisons et pourquoi."),
              ("Durabilité", "Matériaux éprouvés et installations pensées pour durer, faciles à entretenir.")]
    vals = "".join('<li class="val" data-r><span class="mono">%02d</span><h3>%s</h3><p>%s</p></li>' % (k + 1, t, p) for k, (t, p) in enumerate(values))
    fiche = [("Raison sociale", CO["name"]), ("Forme juridique", "Société à responsabilité limitée"), ("Siège", ADDR),
             ("Associé-gérant", CO["manager"]), ("Inscription au RC", "Canton de Vaud, juillet 2026"), ("N° IDE", CO["ide"]),
             ("Domaines", "Installations sanitaires et de chauffage"),
             ("Activités", "Pose, entretien, maintenance, dépannage, rénovation et réparation d’équipements sanitaires et de systèmes de chauffage")]
    fiche_html = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in fiche)
    body = '''
<section class="pg-hero">
 <div class="hero__grid" aria-hidden="true"></div>
 <div class="pg-hero__art" data-art data-intro aria-hidden="true">{RUN}</div>
 <div class="wrap">
  <nav class="crumbs mono" aria-label="Fil d’Ariane" data-intro><a href="{HOME}">Accueil</a><span>/</span><span aria-current="page">L’entreprise</span></nav>
  <p class="kicker" data-intro><span>[Fondée en 2026]</span> Prilly · Vaud</p>
  <h1 class="pg-hero__h" data-intro data-split>Une entreprise de sanitaire, faite pour durer.</h1>
  <p class="pg-hero__p" data-intro>Bluetech Sanitaire Sàrl est née à Prilly en 2026, avec une idée simple : faire du sanitaire comme on aimerait qu’il soit fait chez soi — précis, propre, et expliqué.</p>
 </div>
</section>

<section class="sec story">
 <div class="wrap story__g">
  <figure class="story__ph" data-r>%(ph)s<span class="crop" aria-hidden="true"></span></figure>
  <div class="story__t">
   %(shead)s
   <p data-r>Nous intervenons sur l’ensemble des installations sanitaires et de chauffage : construction neuve, transformation, rénovation de salles de bains, entretien et dépannage, pour les particuliers, les copropriétés et les régies.</p>
   <p data-r>Notre conviction : la qualité d’une installation se joue là où personne ne regarde. C’est pourquoi nous traçons les axes avant de poser, repérons chaque conduite, contrôlons chaque raccord et photographions nos réseaux avant fermeture.</p>
   <p class="sign" data-r><b>%(mgr)s</b><span>Associé-gérant, Bluetech Sanitaire Sàrl</span></p>
  </div>
 </div>
</section>

<section class="sec sec--paper vals">
 <div class="wrap">
  %(vhead)s
  <ul class="vals__l">%(vals)s</ul>
 </div>
</section>

<section class="sec">
 <div class="wrap fiche-pg">
  %(fhead)s
  <div class="fiche fiche--lg" data-r><p class="mono fiche__h">Registre du commerce <span>VD</span></p><dl>%(fiche)s</dl></div>
 </div>
</section>
%(process)s
%(zone)s
%(cta)s''' % dict(ph=pic("evacuations-controlees", "Évacuations marquées « OK » après contrôle, derrière un bâti-support", "(max-width: 900px) 92vw, 40vw", w=1440, h=2048),
                  shead=sec_head("01", "Notre approche", "Le soin se voit surtout là où on ne regarde pas."), mgr=e(CO["manager"]),
                  vhead=sec_head("02", "Engagements", "Quatre principes, sur chaque chantier."), vals=vals,
                  fhead=sec_head("03", "Fiche d’identité", "Les faits, simplement."), fiche=fiche_html,
                  process=process_section("04"), zone=zone_section("05"), cta=cta_band())
    return render("entreprise.html", "L’entreprise : Bluetech Sanitaire Sàrl, Prilly | Sanitaire & chauffage",
                  "Bluetech Sanitaire Sàrl, entreprise de sanitaire et chauffage fondée en 2026 à Prilly (VD). Associé-gérant : Ahmet Hoti. Notre approche, nos engagements.",
                  body, key="entreprise", body_cls="p-company")


def page_contact():
    svc_opts = "".join('''<label class="opt"><input type="radio" name="service" value="%s"%s><span class="opt__b"><span class="opt__ic">%s</span><b>%s</b><em>%s</em><i class="opt__ck">%s</i></span></label>''' % (
        e(s["title"]), " required" if k == 0 else "", SICON[s["icon"]], s["title"], s["short"], CHECK) for k, s in enumerate(SERVICES))
    svc_opts += '<label class="opt"><input type="radio" name="service" value="Autre demande"><span class="opt__b"><span class="opt__ic">%s</span><b>Autre demande</b><em>Expliquez-nous</em><i class="opt__ck">%s</i></span></label>' % (PLUS, CHECK)
    slugs = json.dumps({s["slug"]: s["title"] for s in SERVICES}, ensure_ascii=False)
    def chips(name, vals):
        return "".join('<label class="chip"><input type="radio" name="%s" value="%s"><span>%s</span></label>' % (name, e(v), v) for v in vals)
    body = '''
<section class="pg-hero pg-hero--tight">
 <div class="hero__grid" aria-hidden="true"></div>
 <div class="wrap">
  <nav class="crumbs mono" aria-label="Fil d’Ariane" data-intro><a href="{HOME}">Accueil</a><span>/</span><span aria-current="page">Contact & devis</span></nav>
  <p class="kicker" data-intro><span>[Devis sans engagement]</span> Réponse personnalisée</p>
  <h1 class="pg-hero__h" data-intro data-split>Parlons de votre projet.</h1>
  <p class="pg-hero__p" data-intro>Trois étapes, deux minutes. Votre demande nous parvient sur WhatsApp%(ormail)s, prête à être envoyée.</p>
 </div>
</section>

<section class="sec contact">
 <div class="wrap contact__g">
  <form class="wiz" data-form="wizard" data-slugs='%(slugs)s' novalidate>
   <div class="wiz__pipe" aria-hidden="true"><i data-wiz-water></i><span class="wiz__node is-on">01</span><span class="wiz__node">02</span><span class="wiz__node">03</span></div>
   <fieldset class="wiz__s is-on" data-wstep="1">
    <legend><span class="mono">Étape 01 / 03</span>De quoi avez-vous besoin ?</legend>
    <div class="opts">%(opts)s</div>
    <p class="fld__err" data-err="service">Choisissez un type de demande.</p>
   </fieldset>
   <fieldset class="wiz__s" data-wstep="2">
    <legend><span class="mono">Étape 02 / 03</span>Quelques détails</legend>
    <div class="fgrp"><span class="fgrp__l">Type de bien</span><div class="chips-in">%(bien)s</div></div>
    <div class="fgrp"><span class="fgrp__l">Délai souhaité</span><div class="chips-in">%(delai)s</div></div>
    <label class="fld"><span>Votre demande</span><textarea name="message" rows="5" required placeholder="Ex. : remplacer la baignoire par une douche de plain-pied, appartement au 2e étage…"></textarea></label>
    <p class="fld__hint">Vous pourrez joindre des photos directement dans WhatsApp.</p>
   </fieldset>
   <fieldset class="wiz__s" data-wstep="3">
    <legend><span class="mono">Étape 03 / 03</span>Vos coordonnées</legend>
    <div class="f2">
     <label class="fld"><span>Nom et prénom</span><input name="nom" autocomplete="name" required placeholder="Votre nom"></label>
     <label class="fld"><span>Téléphone</span><input name="tel" type="tel" autocomplete="tel" required placeholder="079 123 45 67"></label>
    </div>
    <div class="f2">
     <label class="fld"><span>E-mail <i>(facultatif)</i></span><input name="email" type="email" autocomplete="email" placeholder="vous@exemple.ch"></label>
     <label class="fld"><span>Lieu de l’intervention</span><input name="lieu" autocomplete="address-level2" placeholder="NPA, localité"></label>
    </div>
    <div class="wiz__sum" data-wiz-sum></div>
   </fieldset>
   <div class="wiz__nav">
    <button class="btn btn--line" type="button" data-wiz-prev hidden><span class="btn__fill"></span><span class="btn__t">Retour</span>%(left)s</button>
    <button class="btn btn--blue" type="button" data-wiz-next><span class="btn__fill"></span><span class="btn__t">Continuer</span>%(arrow)s</button>
    <button class="btn btn--blue" type="submit" data-via="wa" hidden><span class="btn__fill"></span><span class="btn__t">Envoyer sur WhatsApp</span>%(waic)s</button>
    %(mailbtn)s
   </div>
   <p class="form__note">Rien n’est enregistré sur ce site : votre message s’ouvre dans WhatsApp%(ormail)s, vous gardez la main pour l’envoyer.</p>
   <p class="form__ok" role="status" aria-live="polite"></p>
  </form>

  <aside class="contact__side">
   <div class="ccard" data-r>
    <p class="mono">Contact direct</p>
    <a class="ccard__l" href="%(tel)s">%(phone)s<span><b>%(phd)s</b>Appel</span></a>
    <a class="ccard__l" href="%(wa)s" target="_blank" rel="noopener">%(waic)s<span><b>WhatsApp</b>Photos et vidéos bienvenues</span></a>
    %(mailcard)s
    <a class="ccard__l" href="%(maps)s" target="_blank" rel="noopener">%(pin)s<span><b>%(street)s</b>%(zip)s %(city)s</span></a>
   </div>
   <div class="mapf" data-r>
    <iframe title="Plan d’accès : %(addr)s" src="%(embed)s" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
   </div>
  </aside>
 </div>
</section>''' % dict(slugs=slugs.replace("'", "&#39;"), opts=svc_opts,
                     bien=chips("bien", ["Appartement", "Maison", "Immeuble / PPE", "Commerce"]),
                     delai=chips("delai", ["Urgent", "Dans le mois", "Dans les 3 mois", "Pas pressé"]),
                     left=LEFT, arrow=ARROW, waic=WA,
                     mailbtn=('<button class="btn btn--line" type="submit" data-via="mail" hidden><span class="btn__fill"></span><span class="btn__t">Par e-mail</span>%s</button>' % MAIL) if EMAIL else "",
                     ormail=" ou par e-mail" if EMAIL else "", tel=TEL, phone=PHONE, phd=PHONE_DISPLAY, wa=WA_HELLO, maps=MAPS, pin=PIN,
                     mailcard=('<a class="ccard__l" href="mailto:%s">%s<span><b>%s</b>E-mail</span></a>' % (EMAIL, MAIL, EMAIL)) if EMAIL else "",
                     street=e(CO["street"]), zip=CO["zip"], city=CO["city"], addr=e(ADDR), embed=MAP_EMBED)
    return render("contact.html", "Contact & devis | Bluetech Sanitaire, Prilly",
                  "Demandez un devis à Bluetech Sanitaire : installations sanitaires, salles de bains, chauffage, dépannage, entretien et boilers à Prilly, Lausanne et environs.",
                  body, key="contact", body_cls="p-contact")


def page_legal():
    body = '''
<section class="pg-hero pg-hero--tight">
 <div class="hero__grid" aria-hidden="true"></div>
 <div class="wrap">
  <nav class="crumbs mono" aria-label="Fil d’Ariane" data-intro><a href="{HOME}">Accueil</a><span>/</span><span aria-current="page">Mentions légales</span></nav>
  <h1 class="pg-hero__h" data-intro>Mentions légales & confidentialité</h1>
 </div>
</section>
<section class="sec legal">
 <div class="wrap legal__g">
  <div class="legal__b">
   <h2>Éditeur du site</h2>
   <p>%(name)s<br>%(street)s<br>%(zip)s %(city)s, Suisse</p>
   <p>Numéro IDE : %(ide)s<br>Registre du commerce du canton de Vaud : %(rc)s<br>Associé-gérant : %(mgr)s</p>
   <h2>Responsabilité</h2>
   <p>Les informations publiées sur ce site sont fournies à titre indicatif et peuvent être modifiées sans préavis. Elles ne constituent pas une offre ; seul un devis écrit engage %(name)s.</p>
   <h2>Propriété intellectuelle</h2>
   <p>Les textes, photographies et éléments graphiques de ce site appartiennent à %(name)s, sauf mention contraire. Toute reproduction nécessite une autorisation préalable.</p>
   <h2>Protection des données</h2>
   <p>Ce site ne collecte aucune donnée personnelle et n’utilise ni cookies publicitaires ni outils de suivi. Les formulaires ne transmettent rien à un serveur : ils préparent un message que vous envoyez vous-même via WhatsApp%(ormail)s. Les données que vous nous transmettez ainsi servent uniquement à traiter votre demande, conformément à la loi fédérale sur la protection des données (LPD).</p>
   <p>La page Contact affiche une carte Google Maps ; en la consultant, Google peut traiter certaines données de connexion selon sa propre politique de confidentialité.</p>
   <h2>Hébergement</h2>
   <p>Ce site est hébergé par GitHub Pages (GitHub, Inc., San Francisco, États-Unis).</p>
  </div>
 </div>
</section>''' % dict(name=e(CO["name"]), street=e(CO["street"]), zip=CO["zip"], city=CO["city"], ide=CO["ide"], rc=CO["rc"], mgr=e(CO["manager"]),
                     ormail=" ou par e-mail" if EMAIL else "")
    return render("mentions-legales.html", "Mentions légales | Bluetech Sanitaire", "Mentions légales et protection des données du site de Bluetech Sanitaire Sàrl, Prilly.",
                  body, key="legal", body_cls="p-legal")


def page_404():
    body = '''
<section class="nf">
 <div class="hero__grid" aria-hidden="true"></div>
 <div class="wrap nf__in">
  <svg class="nf__tap" viewBox="0 0 200 260" aria-hidden="true"><path d="M10 40h70a40 40 0 0 1 40 40v24"/><path d="M10 64h62a24 24 0 0 1 24 24v16"/><path d="M92 104h52"/><rect x="40" y="14" width="40" height="12" rx="6"/><path d="M60 26v14"/><path class="nf__drop" d="M118 120c0 0-10 13-10 20a10 10 0 0 0 20 0c0-7-10-20-10-20z"/></svg>
  <p class="kicker"><span>[404]</span> Page introuvable</p>
  <h1 class="pg-hero__h">Cette page a pris la fuite.</h1>
  <p class="pg-hero__p">Le lien est peut-être ancien, ou l’adresse mal saisie. Pas d’inquiétude : tout le reste est étanche.</p>
  <div class="hero__b">%s<a class="btn btn--line" href="{R}contact"><span class="btn__fill"></span><span class="btn__t">Nous contacter</span>%s</a></div>
 </div>
</section>''' % (btn(BASE, "Retour à l’accueil"), ARROW)
    # 404 is served from any depth, so links must be absolute
    path = render("404.html", "Page introuvable | Bluetech Sanitaire", "Cette page n’existe pas ou plus.", body, key="404", body_cls="p-404")
    f = os.path.join(OUT, "404.html")
    s = open(f).read()
    s = s.replace('href="./', 'href="' + BASE).replace('src="assets/', 'src="' + BASE + 'assets/').replace('href="assets/', 'href="' + BASE + 'assets/')
    for k in ["realisations", "entreprise", "contact", "services/", "mentions-legales"]:
        s = s.replace('href="%s' % k, 'href="%s%s' % (BASE, k))
    s = s.replace('srcset="assets/', 'srcset="' + BASE + 'assets/')
    open(f, "w").write(s)
    return path


def write_misc(urls):
    open(os.path.join(OUT, "robots.txt"), "w").write(
        ("User-agent: *\nDisallow:\n" if not NOINDEX else "User-agent: *\nAllow: /\n") + "\nSitemap: %ssitemap.xml\n" % BASE)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += "  <url><loc>%s%s</loc></url>\n" % (BASE, u)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm + "</urlset>\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")


if __name__ == "__main__":
    urls = [page_home(), page_services()] + [page_service(s) for s in SERVICES] + [page_work(), page_company(), page_contact(), page_legal()]
    page_404()
    write_misc(urls)
    print("built", len(urls) + 1, "pages:", ", ".join(u or "/" for u in urls))
