# -*- coding: utf-8 -*-
"""Interface text, travel-advice panel and footer of the Kinshasa Visitor Guide (EN + FR)."""

CHECKED_ISO = "2026-10-24"
CHECKED = ("24 October 2026", "24 octobre 2026")
TITLE = "Kinshasa Visitor Guide"
META_DESC = ("Hotels, restaurants, parks, gardens, wildlife, amusement parks and day trips in Kinshasa and DR Congo, each with a link to its source. Checked 24 October 2026.",
             "Hôtels, restaurants, parcs, jardins, faune, parcs de loisirs et excursions à Kinshasa et en RD Congo, chacun avec un lien vers sa source. Vérifié le 24 octobre 2026.")


def A(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'


# badge key -> (EN, FR, css class)
BADGES = {
    "new": ("New in 2025", "Nouveau 2025", "info"),
    "weekends": ("Weekends", "Week-ends", "info"),
    "family": ("Family", "En famille", "info"),
    "free": ("Free entry", "Entrée libre", "ok"),
    "4x4": ("4x4 advised", "4x4 conseillé", "info"),
    "overnight": ("Overnight advised", "Nuit conseillée", "info"),
    "call": ("Call first", "Appeler avant", "warn"),
    "single": ("Single source", "Source unique", "warn"),
    "advice": ("Check advisories", "Vérifier les avis", "warn"),
    "dated": ("Older reviews", "Avis anciens", "warn"),
    "rundown": ("Run-down", "Vétuste", "warn"),
    "renov": ("Being rebuilt", "En travaux", "warn"),
    "noswim": ("No swimming", "Baignade interdite", "bad"),
    "restricted": ("Not advisable now", "Déconseillé actuellement", "bad"),
}

LEGEND = [
    ("single", "Found in one non-official source only. Confirm before you go.",
     "Trouvé dans une seule source non officielle. Confirmez avant de vous déplacer."),
    ("call", "Hours or prices are unclear or informal. Phone or ask your hotel.",
     "Horaires ou tarifs flous ou informels. Appelez ou demandez à votre hôtel."),
    ("advice", "The place or its route is near an area covered by government travel advice.",
     "Le lieu ou son itinéraire est proche d’une zone visée par des avis aux voyageurs."),
    ("dated", "The latest review we found is more than a year old.",
     "Le dernier avis trouvé date de plus d’un an."),
    ("renov", "Closed or partly closed for works.",
     "Fermé ou partiellement fermé pour travaux."),
    ("restricted", "Governments currently advise against travel to this region.",
     "Les gouvernements déconseillent actuellement de voyager dans cette région."),
]

# link kind -> (EN, FR)
LINK_LABELS = {
    "official": ("Official site", "Site officiel"),
    "web": ("Website", "Site web"),
    "ta": ("TripAdvisor", "TripAdvisor"),
    "wiki": ("Wikipedia", "Wikipédia"),
    "news": ("News report", "Article de presse"),
    "guide": ("Local guide", "Guide local"),
    "unesco": ("UNESCO", "UNESCO"),
    "fb": ("Facebook", "Facebook"),
    "advice": ("Travel advice", "Avis aux voyageurs"),
}

UI = {
    "skip": ("Skip to the guide", "Aller au guide"),
    "nav": ("Sections", "Rubriques"),
    "eyebrow": ("DR Congo · Visitor guide", "RD Congo · Guide du visiteur"),
    "h1": ("Discover Kinshasa and the Congo", "Découvrez Kinshasa et le Congo"),
    "lead": ("Hotels, restaurants, parks, gardens, wildlife and day trips, with a link behind every place so you can check it, book it or find it on the map.",
             "Hôtels, restaurants, parcs, jardins, faune et excursions, avec un lien derrière chaque lieu pour le vérifier, le réserver ou le situer sur la carte."),
    "checked": ("Last checked", "Dernière vérification"),
    "places": ("places", "lieux"),
    "search_ph": ("Search a place, a dish, a district…", "Rechercher un lieu, un plat, un quartier…"),
    "search_label": ("Search the guide", "Rechercher dans le guide"),
    "area_label": ("District or region", "Quartier ou région"),
    "all_areas": ("All districts and regions", "Tous les quartiers et régions"),
    "clear": ("Clear search", "Effacer la recherche"),
    "shown": ("places shown", "lieux affichés"),
    "none": ("No place matches. Try another word or choose all districts.", "Aucun lieu ne correspond. Essayez un autre mot ou choisissez tous les quartiers."),
    "legend": ("What the labels mean", "Signification des étiquettes"),
    "facts": ("Good to know", "À savoir"),
    "map": ("Map", "Carte"),
    "top": ("Back to top", "Haut de page"),
    "changes_h": ("Recently changed or uncertain", "Changements récents ou incertitudes"),
    "plan_h": ("Plan and check", "Préparer et vérifier"),
    "plan_note": ("Operators are listed because they were used as sources for this guide. They are not endorsements.",
                  "Les opérateurs sont cités parce qu’ils ont servi de sources à ce guide. Ce ne sont pas des recommandations."),
    "foot_h": ("How this guide was made", "Comment ce guide a été réalisé"),
}

TRAVEL_H = ("Before you travel", "Avant de partir")
TRAVEL_LEAD = (
    "DR Congo is a very large country, and conditions differ a lot from one province to the next. This guide concentrates on Kinshasa and on regions that governments do not currently advise against. Check the latest advice before you book anything.",
    "La RD Congo est un très grand pays et les conditions varient fortement d’une province à l’autre. Ce guide se concentre sur Kinshasa et sur les régions que les gouvernements ne déconseillent pas actuellement. Consultez les derniers avis avant de réserver quoi que ce soit.",
)

UK = "https://www.gov.uk/foreign-travel-advice/democratic-republic-of-the-congo"
FR_ADV = "https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/republique-democratique-du-congo/"
US_ADV = "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/democratic-republic-of-the-congo-travel-advisory.html"
WHO = "https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON622"
VISA_VIRUNGA = "https://visit.virunga.org/visa/"
VISA_WIKI = "https://en.wikipedia.org/wiki/Visa_policy_of_the_Democratic_Republic_of_the_Congo"

TRAVEL_BLOCKS = [
    dict(h=("Health", "Santé"),
         en=("An Ebola outbreak (Bundibugyo virus) is active in DR Congo. WHO’s report of 23 October 2026 lists eight affected provinces (Ituri, North Kivu, Haut-Uélé, Tshopo, Bas-Uélé, South Kivu, South Ubangi and North Ubangi) and does not list Kinshasa. WHO advises against restricting travel, but some countries screen travellers arriving from DR Congo. France also reports a prolonged cholera outbreak across 21 provinces. "
             + A(WHO, "WHO report") + " · " + A(FR_ADV, "French advice")),
         fr=("Une épidémie d’Ebola (virus Bundibugyo) est active en RD Congo. Le rapport de l’OMS du 23 octobre 2026 recense huit provinces touchées (Ituri, Nord-Kivu, Haut-Uélé, Tshopo, Bas-Uélé, Sud-Kivu, Sud-Ubangi et Nord-Ubangi) et ne mentionne pas Kinshasa. L’OMS déconseille toute restriction de voyage, mais certains pays contrôlent les voyageurs en provenance de RD Congo. La France signale aussi une épidémie de choléra prolongée dans 21 provinces. "
             + A(WHO, "Rapport de l’OMS") + " · " + A(FR_ADV, "Conseils de la France"))),
    dict(h=("Security", "Sécurité"),
         en=("The UK Foreign Office (updated 8 October 2026) advises against all travel to Haut-Uélé, Ituri, North Kivu, South Kivu, Maniema, Tanganyika and Haut-Lomami, to within 50 km of the Central African Republic border and to Kwamouth territory. It advises against all but essential travel to Upemba National Park, to Kisangani airport and, in Kinshasa Province, to the N’djili and Kimbanseke districts south of the airport access road and to a section of the N1 road (Menkao to Kenge). It says M23 rebels and Rwandan forces have captured Goma and Bukavu, and that commercial flights no longer operate there. "
             + A(UK, "UK advice") + " · " + A(FR_ADV, "French advice") + " · " + A(US_ADV, "US advice")),
         fr=("Le Foreign Office britannique (mis à jour le 8 octobre 2026) déconseille tout voyage dans le Haut-Uélé, l’Ituri, le Nord-Kivu, le Sud-Kivu, le Maniema, le Tanganyika et le Haut-Lomami, à moins de 50 km de la frontière avec la République centrafricaine et dans le territoire de Kwamouth. Il déconseille les voyages non essentiels au parc national de l’Upemba, à l’aéroport de Kisangani et, dans la province de Kinshasa, aux districts de N’djili et de Kimbanseke au sud de la route d’accès à l’aéroport ainsi qu’à une section de la RN1 (de Menkao à Kenge). Il indique que le M23 et les forces rwandaises ont pris Goma et Bukavu et que plus aucun vol commercial n’y opère. "
             + A(UK, "Avis britannique") + " · " + A(FR_ADV, "Conseils de la France") + " · " + A(US_ADV, "Avis américain"))),
    dict(h=("Entry", "Entrée"),
         en=("Most visitors must apply for a visa before travelling, and a yellow-fever vaccination certificate is required to enter (have the vaccine at least 10 days before departure). Rules and fees change, so confirm with the nearest Congolese embassy and your airline. "
             + A(VISA_VIRUNGA, "Entry requirements (Virunga National Park)") + " · " + A(VISA_WIKI, "Visa policy overview")),
         fr=("La plupart des visiteurs doivent demander un visa avant de partir, et un certificat de vaccination contre la fièvre jaune est exigé à l’entrée (à faire au moins 10 jours avant le départ). Les règles et les tarifs évoluent : confirmez auprès de l’ambassade de RD Congo la plus proche et de votre compagnie aérienne. "
             + A(VISA_VIRUNGA, "Conditions d’entrée (parc des Virunga)") + " · " + A(VISA_WIKI, "Aperçu de la politique de visas"))),
    dict(h=("Getting around", "Se déplacer"),
         en=("Airport transfers to Gombe take about 45 minutes without traffic (hotel information), and traffic can be heavy, so allow extra time for every trip. Ask your hotel to arrange a trusted driver, avoid driving at night outside the city, and do not swim in the Congo River: the current is strong."),
         fr=("Le trajet entre l’aéroport et la Gombe prend environ 45 minutes sans circulation (information d’un hôtel), et la circulation peut être dense : prévoyez de la marge pour chaque déplacement. Demandez à votre hôtel de vous organiser un chauffeur de confiance, évitez de rouler de nuit hors de la ville et ne vous baignez pas dans le fleuve Congo : le courant est fort.")),
]

# Recently changed / uncertain: (en_html, fr_html)
CHANGES = [
    (f'<a href="#kinshasa-zoo">Kinshasa Zoo</a>: being rebuilt since mid-June 2026, with the animals moved to N’sele and no reopening date announced.',
     f'<a href="#kinshasa-zoo">Zoo de Kinshasa</a> : en reconstruction depuis la mi-juin 2026, animaux transférés à N’sele, sans date de réouverture annoncée.'),
    ('Nganda Yalha, on the Nsele River: reported permanently closed since May 2026 (' + A("https://kinocongo.com/blog/activites/nganda-yalha-23", "local guide") + ').',
     'Nganda Yalha, sur la rivière Nsele : signalé comme définitivement fermé depuis mai 2026 (' + A("https://kinocongo.com/blog/activites/nganda-yalha-23", "guide local") + ').'),
    ('Lac Cemka, Kimwenza: reported closed to the public (' + A("https://kinocongo.com/blog/activites/lac-cemka-ferme-30", "local guide") + ').',
     'Lac Cemka, Kimwenza : signalé comme fermé au public (' + A("https://kinocongo.com/blog/activites/lac-cemka-ferme-30", "guide local") + ').'),
    ('Serpents du Congo, reptile demonstrations in the Binza district: the latest ' + A("https://www.tripadvisor.com/Attraction_Review-g294187-d3784153-Reviews-Serpents_du_Congo-Kinshasa.html", "TripAdvisor review") + ' we saw dates from November 2020 and visits were arranged by phone. Confirm that it still operates before planning around it.',
     'Serpents du Congo, démonstrations de reptiles dans le quartier de Binza : le dernier ' + A("https://www.tripadvisor.com/Attraction_Review-g294187-d3784153-Reviews-Serpents_du_Congo-Kinshasa.html", "avis TripAdvisor") + ' consulté date de novembre 2020 et les visites se faisaient sur rendez-vous téléphonique. Vérifiez que le lieu fonctionne encore avant de le prévoir.'),
]

# Plan and links: (heading (en, fr), [(label_en, label_fr, url)])
PLAN = [
    (("Official advice and health", "Avis officiels et santé"), [
        ("UK Foreign Office: DR Congo", "Foreign Office britannique : RD Congo", UK),
        ("France Diplomatie: RDC", "France Diplomatie : RDC", FR_ADV),
        ("US State Department: DR Congo", "Département d’État américain : RD Congo", US_ADV),
        ("WHO: Ebola outbreak report", "OMS : rapport sur l’épidémie d’Ebola", WHO),
    ]),
    (("Entry requirements", "Conditions d’entrée"), [
        ("Visa and yellow fever: Virunga National Park page", "Visa et fièvre jaune : page du parc des Virunga", VISA_VIRUNGA),
        ("Visa policy of DR Congo (Wikipedia)", "Politique de visas de la RD Congo (Wikipédia)", VISA_WIKI),
    ]),
    (("Planning tools", "Outils de préparation"), [
        ("TripAdvisor: Kinshasa hotels", "TripAdvisor : hôtels de Kinshasa", "https://www.tripadvisor.com/Hotels-g294187-Kinshasa-Hotels.html"),
        ("TripAdvisor: Kinshasa restaurants", "TripAdvisor : restaurants de Kinshasa", "https://www.tripadvisor.com/Restaurants-g294187-Kinshasa.html"),
        ("TripAdvisor: Kinshasa things to do", "TripAdvisor : activités à Kinshasa", "https://www.tripadvisor.com/Attractions-g294187-Activities-Kinshasa.html"),
        ("Kino Congo: Kinshasa driver service with a local sites guide", "Kino Congo : service de chauffeurs à Kinshasa avec guide des sites", "https://kinocongo.com/blog"),
        ("Congo Travel and Tours: tour operator, Kongo Central itineraries", "Congo Travel and Tours : voyagiste, itinéraires au Kongo Central", "https://congotravelandtours.com/"),
    ]),
]

FOOTER = (
    "Compiled on 24 October 2026 from official hotel, park and museum websites; government and WHO pages; TripAdvisor listings (ratings, addresses and hours as displayed that day); Congolese news outlets (ACP, Actualité.cd, Bankable); and the local guide of a Kinshasa driver service (Kino Congo) for leisure sites that have few other sources. Entries that rest on one source are labelled “Single source”. Hours, prices and availability change, so confirm before you go. This is an independent guide and not an official publication of any tourism authority or of the businesses it lists. The French text is a first translation that a native speaker has not yet reviewed.",
    "Réalisé le 24 octobre 2026 à partir des sites officiels d’hôtels, de parcs et de musées ; de pages gouvernementales et de l’OMS ; des fiches TripAdvisor (notes, adresses et horaires tels qu’affichés ce jour-là) ; de médias congolais (ACP, Actualité.cd, Bankable) ; et du guide local d’un service de chauffeurs de Kinshasa (Kino Congo) pour les lieux de loisirs qui ont peu d’autres sources. Les fiches fondées sur une seule source portent l’étiquette « Source unique ». Horaires, prix et disponibilités changent : confirmez avant de vous déplacer. Ce guide est indépendant et n’est pas une publication officielle d’une autorité du tourisme ni des entreprises citées. Le texte français est une première traduction qui n’a pas encore été relue par un francophone natif.",
)
