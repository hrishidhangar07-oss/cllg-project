"""
Comprehensive disease descriptions and treatment solutions for all 38 plant disease classes.
"""

from typing import Dict, Any

DISEASE_DATABASE: Dict[str, Dict[str, Any]] = {
    "Apple___Apple_scab": {
        "crop": "Apple",
        "condition": "Apple Scab",
        "is_healthy": False,
        "cause": "Venturia inaequalis (Ascomycete fungus)",
        "description": (
            "Apple scab is one of the most serious fungal diseases affecting apple and crabapple trees worldwide. "
            "It targets both foliage and fruit, causing severe defoliation, stunted fruit growth, and corky surface lesions. "
            "The pathogen overwinters in fallen infected leaves and releases ascospores during warm, wet spring rains."
        ),
        "symptoms": [
            "Olive-green to dull brown velvety spots on leaf surfaces.",
            "Deformed, puckered, or curling leaves that turn yellow and drop prematurely.",
            "Circular, velvety brown lesions on fruit that later turn corky, dark, and crack open.",
            "Reduced fruit yield and weakened overall tree vigor."
        ],
        "solutions": {
            "organic": (
                "Apply sulfur-based or copper-based bio-fungicides at green tip and petal fall stages. "
                "Spray Bacillus subtilis (Serenade) or potassium bicarbonate bi-weekly during humid conditions. "
                "Spread a layer of organic mulch around the tree base to cover overwintered spore sources."
            ),
            "chemical": (
                "Apply protectant fungicides such as Captan or Mancozeb before anticipated rain events in spring. "
                "For systemic curative action within 72 hours of infection, apply Myclobutanil (Rally) or Difenoconazole (Inspire Super). "
                "Rotate fungicide FRAC classes to prevent fungal resistance."
            ),
            "prevention": (
                "Rake and thoroughly compost or burn fallen leaves in autumn to eradicate overwintering pseudothecia. "
                "Prune the tree canopy annually during dormancy to enhance sunlight penetration and airflow. "
                "Plant scab-resistant apple cultivars such as Honeycrisp, Enterprise, Liberty, or Freedom. "
                "Avoid overhead sprinkler irrigation; use drip or soaker hoses to keep leaves dry."
            )
        }
    },
    "Apple___Black_rot": {
        "crop": "Apple",
        "condition": "Black Rot (Frog-Eye Leaf Spot)",
        "is_healthy": False,
        "cause": "Botryosphaeria obtusa (Fungus)",
        "description": (
            "Black rot can infect leaves, fruit, and woody limbs of apple trees. On leaves, it manifests as 'frog-eye' "
            "leaf spots, while infected fruit develops firm, concentric dark rot that eventually mummifies on the branches. "
            "Cankers on branches serve as continuous reservoirs of spores."
        ),
        "symptoms": [
            "Small purple specks on leaves expanding into circular spots with light tan centers and purple margins ('frog-eye').",
            "Fruit rot beginning near the calyx with alternating light and dark brown concentric bands.",
            "Shrunken, black mummified fruit clinging to trees over winter.",
            "Sunken, reddish-brown cankers on bark with cracked outer margins."
        ],
        "solutions": {
            "organic": (
                "Apply liquid copper or lime-sulfur sprays during late dormant stage. "
                "Remove and bury or burn all mummified fruit clinging to trees or on the ground. "
                "Spray neem oil extracts as an early protective barrier against spore attachment."
            ),
            "chemical": (
                "Spray Captan or Thiophanate-methyl (Topsin-M) from petal fall through mid-summer every 10–14 days. "
                "Strobilurin fungicides (Flint, Pristine) provide broad-spectrum control against black rot and powdery mildew."
            ),
            "prevention": (
                "Prune out dead wood, cankered limbs, and fire blight strikes at least 6–8 inches below diseased tissue. "
                "Sterilize pruning shears with 70% isopropyl alcohol or 10% bleach between each cut. "
                "Protect bark from winter injury and sunscald by painting lower trunks with white latex paint."
            )
        }
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "condition": "Cedar Apple Rust",
        "is_healthy": False,
        "cause": "Gymnosporangium juniperi-virginianae (Heteroecious fungus)",
        "description": (
            "Cedar apple rust is a two-host fungal disease requiring both apples and Eastern red cedars (or junipers) "
            "to complete its life cycle. In spring, galls on junipers swell into gelatinous orange horn-like structures, "
            "ejecting spores that drift through the wind to infect apple foliage and developing fruits."
        ),
        "symptoms": [
            "Bright, conspicuous yellow-orange spots on the upper leaf surface that develop small black specks.",
            "Clusters of cup-shaped, tube-like fungal aecia forming on the underside of infected leaves in summer.",
            "Premature defoliation in severe infestations leading to stunted fruit growth and tree stress."
        ],
        "solutions": {
            "organic": (
                "Apply wettable sulfur or copper fungicides just as apple leaf buds unfold in early spring. "
                "Hand-pick and destroy cedar galls on nearby junipers during late winter before gelatinous horns emerge."
            ),
            "chemical": (
                "Apply systemic fungicides containing Myclobutanil (Immunox) from pink bud stage through early summer. "
                "Triflumizole (Procure) or Mancozeb treatments timed during warm, rainy periods when cedar galls are active."
            ),
            "prevention": (
                "If feasible, remove Eastern red cedar and juniper trees within a 1–2 mile radius of the orchard. "
                "Select rust-resistant apple varieties like Redfree, Liberty, Freedom, or Williams Pride. "
                "Inspect windbreak junipers annually and clip off small brown woody galls."
            )
        }
    },
    "Apple___healthy": {
        "crop": "Apple",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": (
            "The apple leaf displays vibrant green pigmentation, clear vascular venation, and smooth lamina without "
            "fungal lesions, bacterial spots, or pest damage. The plant appears robust and thriving."
        ),
        "symptoms": ["Uniform green leaf surface.", "No spots, curling, wilting, or discoloration."],
        "solutions": {
            "organic": "Maintain regular balanced organic fertilization (well-rotted compost, seaweed extract).",
            "chemical": "No chemical treatment required. Avoid unnecessary pesticide applications.",
            "prevention": "Ensure deep watering at root zone during dry spells. Maintain adequate tree spacing and annual pruning."
        }
    },
    "Blueberry___healthy": {
        "crop": "Blueberry",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": (
            "Blueberry leaves are glossy, deep green, and firm, showing healthy photosynthesis and ideal soil acidity (pH 4.5–5.5)."
        ),
        "symptoms": ["Normal oval leaves, clean surface, healthy shoots."],
        "solutions": {
            "organic": "Apply pine needle or pine bark mulch to sustain optimal acidic soil moisture and nutrition.",
            "chemical": "None needed. Keep soil pH between 4.5 and 5.2 using elemental sulfur if necessary.",
            "prevention": "Water with non-alkaline water. Protect plants from bird foraging with netting during fruiting."
        }
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry",
        "condition": "Powdery Mildew",
        "is_healthy": False,
        "cause": "Podosphaera clandestina (Fungus)",
        "description": (
            "Powdery mildew on cherries attacks young leaves, shoots, and ripening fruit. A powdery white fungal mycelium "
            "carpets infected leaves, causing them to curl upward, distort, and drop prematurely."
        ),
        "symptoms": [
            "White circular powdery fungal patches on new leaf growth and green fruit.",
            "Leaves curling upward into troughs and exhibiting brittle texture.",
            "Blistering and distorted shoot tips with delayed ripening."
        ],
        "solutions": {
            "organic": (
                "Spray horticultural potassium bicarbonate (MilStop) or neem oil at first sign of powdery patches. "
                "Sulfur dust or wettable sulfur applied before high ambient temperatures (>32°C / 90°F)."
            ),
            "chemical": (
                "Apply Quinoxyfen (Quintec) or Boscalid + Pyraclostrobin (Pristine) at petal fall and shuck fall. "
                "Rotate with Myclobutanil (Rally) to forestall resistance development."
            ),
            "prevention": (
                "Prune dense branch canopies to encourage rapid drying and airflow. "
                "Avoid high-nitrogen fertilizers late in the season which encourage tender, susceptible succulent flushes."
            )
        }
    },
    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Healthy cherry foliage with crisp serrated edges, uniform dark green color, and clean petioles.",
        "symptoms": ["Vigorous green leaves, intact cuticle, no powdery patches or leaf spots."],
        "solutions": {
            "organic": "Maintain regular balanced organic mulch and compost application.",
            "chemical": "No chemical intervention needed.",
            "prevention": "Inspect leaves weekly during humid spring weather. Prune for good canopy ventilation."
        }
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn (Maize)",
        "condition": "Gray Leaf Spot",
        "is_healthy": False,
        "cause": "Cercospora zeae-maydis (Fungus)",
        "description": (
            "Gray leaf spot is a devastating foliar disease of maize favored by prolonged warm, humid weather and minimal tillage. "
            "Lesions expand parallel to leaf veins, restricting photosynthesis and accelerating premature senescence."
        ),
        "symptoms": [
            "Small tan spots with yellow halos expanding into long, narrow, rectangular gray-to-tan lesions.",
            "Lesions strictly delimited by leaf veins giving them crisp blocky borders.",
            "Widespread blighting of upper canopy and premature stalk lodging."
        ],
        "solutions": {
            "organic": (
                "Implement strict multi-year crop rotation with non-host crops (soybeans, alfalfa, small grains). "
                "Apply bio-fungicides with Trichoderma harzianum or Bacillus amyloliquefaciens."
            ),
            "chemical": (
                "Apply strobilurin and triazole fungicide mixtures (e.g. Azoxystrobin + Propiconazole / Quilt Xcel). "
                "Spray between VT (tasseling) and R2 (blister stage) when conditions favor disease progression."
            ),
            "prevention": (
                "Till crop residue under to accelerate degradation of overwintering fungal mycelium. "
                "Plant high-yielding maize hybrids bred with genetic resistance to Gray Leaf Spot."
            )
        }
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (Maize)",
        "condition": "Common Rust",
        "is_healthy": False,
        "cause": "Puccinia sorghi (Fungus)",
        "description": (
            "Common rust produces powdery brick-red pustules on both upper and lower corn leaves. "
            "Spores are blown northward on wind currents from subtropical regions every growing season."
        ),
        "symptoms": [
            "Cinnamon-brown to brick-red oval pustules scattered across both leaf surfaces.",
            "Pustules rupture the leaf epidermis, releasing powdery reddish-brown urediniospores.",
            "Leaf chlorosis and drying when pustule density is high."
        ],
        "solutions": {
            "organic": (
                "Utilize certified rust-resistant corn varieties. "
                "Spray sulfur-based formulations early in infection cycles."
            ),
            "chemical": (
                "Apply Pyraclostrobin (Headline) or Tebuconazole if rust appears on upper leaves before tasseling and 6+ pustules per leaf are observed."
            ),
            "prevention": (
                "Plant early in the season to evade peak mid-summer airborne spore influx. "
                "Select maize hybrids with Rp1D resistance genes."
            )
        }
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)",
        "condition": "Northern Corn Leaf Blight",
        "is_healthy": False,
        "cause": "Exserohilum turcicum (Fungus)",
        "description": (
            "Northern corn leaf blight (NCLB) is recognized by large cigar-shaped grayish-green or tan lesions on leaves. "
            "It thrives under moderate temperatures (18–27°C) accompanied by heavy dew or frequent rain."
        ),
        "symptoms": [
            "Long, elliptical, cigar-shaped grayish-green or tan lesions (2.5 to 15 cm long).",
            "Dark dirty olive fungal sporulation in center of lesions during damp mornings.",
            "Extensive leaf death and premature field dry-down."
        ],
        "solutions": {
            "organic": (
                "Incorporate deep tillage to bury infected corn residue. "
                "Rotate field with legumes or sunflowers for at least 2 consecutive seasons."
            ),
            "chemical": (
                "Apply Pyraclostrobin + Fluxapyroxad (Priaxor) or Prothioconazole + Trifloxystrobin (Delaro) near silking stage."
            ),
            "prevention": (
                "Plant corn hybrids containing specific Ht resistance genes (Ht1, Ht2, Ht3, HtN). "
                "Maintain balanced soil fertility, avoiding excessive nitrogen with deficient potassium."
            )
        }
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (Maize)",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Healthy maize foliage with broad, deep-green, waxy leaves and robust photosynthetic activity.",
        "symptoms": ["Deep green color, clean leaf margins, strong central midrib."],
        "solutions": {
            "organic": "Maintain regular nitrogen sidedressing and organic cover crop integration.",
            "chemical": "No treatments needed.",
            "prevention": "Ensure proper plant spacing and consistent moisture during tasseling and silking."
        }
    },
    "Grape___Black_rot": {
        "crop": "Grape",
        "condition": "Black Rot",
        "is_healthy": False,
        "cause": "Guignardia bidwellii (Fungus)",
        "description": (
            "Black rot is one of the most destructive grape diseases in warm, humid regions. "
            "It attacks all green parts of the vine, turning plump berries into hard, shriveled black mummies."
        ),
        "symptoms": [
            "Small reddish-brown circular spots on leaves with dark borders and tiny black fruiting bodies (pycnidia).",
            "Infected fruit softens, turns brown, then shrivels into wrinkled, hard, blue-black mummies.",
            "Elongated black lesions on young green shoots and tendrils."
        ],
        "solutions": {
            "organic": (
                "Apply copper hydroxide or lime sulfur before bloom and every 10–14 days in damp conditions. "
                "Rake and remove all fallen mummies from beneath grapevines before bud break."
            ),
            "chemical": (
                "Apply Mancozeb, Captan, or Myclobutanil (Rally) from early shoot development (1–3 inch shoots) through 4 weeks post-bloom."
            ),
            "prevention": (
                "Prune vines in winter to a high-wire trellis system to maximize sun exposure and airflow. "
                "Maintain weed-free ground below the canopy to reduce humidity."
            )
        }
    },
    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape",
        "condition": "Esca (Black Measles)",
        "is_healthy": False,
        "cause": "Complex of wood-rotting fungi (Phaeomoniella chlamydospora, Fomitiporia mediterranea)",
        "description": (
            "Esca is a complex fungal vascular decline disease of mature grapevines. It causes distinctive 'tiger-stripe' "
            "foliar patterns and spotty 'measles' on berries, ultimately leading to vine apoplexy (sudden wilting)."
        ),
        "symptoms": [
            "Interveinal chlorosis and necrosis creating a distinctive 'tiger-stripe' leaf pattern.",
            "Small dark purple or brown spots ('measles') on the skin of white or red grape clusters.",
            "Internal dark wood streaking and soft yellow spongy wood rot inside cordons and trunk."
        ],
        "solutions": {
            "organic": (
                "Apply Trichoderma-based bio-protectants directly onto fresh pruning wounds immediately after cutting. "
                "Paint pruning wounds with wound sealants to prevent fungal spore germination."
            ),
            "chemical": (
                "There are no curative chemical sprays once systemic wood infection occurs. "
                "Apply Thiophanate-methyl or boron pastes directly to large pruning cuts."
            ),
            "prevention": (
                "Delay winter pruning until late in the dormant season when wounds heal more rapidly. "
                "Disinfect pruning shears between individual vines. "
                "Retrain a new healthy shoot from below trunk cankers to regenerate the vine framework."
            )
        }
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape",
        "condition": "Leaf Blight (Isariopsis Spot)",
        "is_healthy": False,
        "cause": "Pseudocercospora vitis / Phaeoisariopsis vitis (Fungus)",
        "description": (
            "Late-season foliar disease causing irregular dark brown spots with darker margins on grape leaves, "
            "leading to early defoliation and compromised berry sugar accumulation."
        ),
        "symptoms": [
            "Irregular, angular reddish-brown to dark brown necrotic spots on leaves.",
            "Grayish or olive fungal sporulation on the underside of spots during humid spells.",
            "Premature defoliation in late summer."
        ],
        "solutions": {
            "organic": "Apply copper-based bordeaux mixture or sulfur sprays in early summer.",
            "chemical": "Use Mancozeb, Azoxystrobin, or Difenoconazole according to local vineyard spray calendars.",
            "prevention": "Prune foliage to open vine canopy; destroy fallen leaves post-harvest."
        }
    },
    "Grape___healthy": {
        "crop": "Grape",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Lush, well-expanded palmately lobed green grape leaves with clean cuticles and vigorous tendrils.",
        "symptoms": ["Uniform green foliage, no leaf spots, no chlorosis or necrosis."],
        "solutions": {
            "organic": "Maintain regular canopy management, mulching, and balanced organic vine nutrition.",
            "chemical": "No treatments needed.",
            "prevention": "Continue canopy hedging, cluster thinning, and proper soil moisture monitoring."
        }
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange / Citrus",
        "condition": "Huanglongbing (Citrus Greening)",
        "is_healthy": False,
        "cause": "Candidatus Liberibacter asiaticus (Bacteria transmitted by Asian citrus psyllid)",
        "description": (
            "Huanglongbing (HLB) is one of the most fatal diseases affecting citrus orchards worldwide. "
            "The phloem-limited bacterium is transmitted by the Asian citrus psyllid (Diaphorina citri). "
            "It causes asymmetric blotchy leaf mottle, bitter misshapen fruit with green ends, and tree death."
        ),
        "symptoms": [
            "Asymmetrical blotchy yellow mottling crossing leaf veins (different pattern on either side of midrib).",
            "Yellowing of individual shoots followed by progressive branch dieback.",
            "Small, lopsided, bitter fruit that stays green at the blossom end ('greening').",
            "Twig dieback and premature fruit drop."
        ],
        "solutions": {
            "organic": (
                "Release biological control parasitoids (Tamarixia radiata wasps) to suppress psyllid populations. "
                "Spray horticultural mineral oils or citrus-friendly insecticidal soaps to suffocate psyllid nymphs. "
                "Provide foliar micro-nutrient therapies (zinc, manganese, iron) to support tree longevity."
            ),
            "chemical": (
                "Apply targeted systemic insecticides (Imidacloprid, Thiamethoxam) to manage vector psyllid insect populations. "
                "Oxytetracycline trunk injections may be legally administered under agricultural permits."
            ),
            "prevention": (
                "Always plant certified pathogen-free citrus nursery trees from screened greenhouses. "
                "Immediately remove and eradicate confirmed infected trees to protect surrounding orchards. "
                "Scout groves weekly for Asian citrus psyllid eggs and waxy feeding honeydew."
            )
        }
    },
    "Peach___Bacterial_spot": {
        "crop": "Peach",
        "condition": "Bacterial Spot",
        "is_healthy": False,
        "cause": "Xanthomonas arboricola pv. pruni (Bacterium)",
        "description": (
            "Bacterial spot attacks peach leaves, twigs, and fruit in sandy soils during warm, windy, wet seasons. "
            "Leaf spots drop out leaving a 'shot-hole' appearance, and fruit exhibits deep pitted craters."
        ),
        "symptoms": [
            "Small, angular, water-soaked purple-brown lesions on leaves.",
            "Dead centers of spots drop out, producing a characteristic 'shot-hole' perforated appearance.",
            "Small water-soaked blisters on fruit that enlarge, turn dark, and crack deeply.",
            "Spring and summer cankers on succulent twigs."
        ],
        "solutions": {
            "organic": "Apply copper octanoate or fixed copper sprays at dormant bud swell and fall leaf drop.",
            "chemical": (
                "Spray Oxytetracycline (Mycoshield) from shuck split through harvest at 7-day intervals. "
                "Use low-rate copper formulations during early cover sprays to prevent phytotoxicity."
            ),
            "prevention": (
                "Plant peach cultivars with high bacterial spot resistance (e.g. Candor, Biscoe, Harrow Diamond). "
                "Avoid planting in wind-swept, highly sandy sites without established windbreaks."
            )
        }
    },
    "Peach___healthy": {
        "crop": "Peach",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Graceful lanceolate, glossy green peach leaves with clean margins and sturdy branch attachments.",
        "symptoms": ["Uniform green coloration, no perforations, no gumming or leaf spots."],
        "solutions": {
            "organic": "Annual compost application and soil moisture monitoring.",
            "chemical": "No treatments needed.",
            "prevention": "Prune open-center vase shapes annually in late winter for maximum air passage."
        }
    },
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Bell Pepper",
        "condition": "Bacterial Spot",
        "is_healthy": False,
        "cause": "Xanthomonas campestris pv. vesicatoria (Bacterium)",
        "description": (
            "A major threat to pepper production in warm, rainy climates. The bacteria enter through stomata and wounds, "
            "causing defoliation and sunscald on exposed bell peppers."
        ),
        "symptoms": [
            "Water-soaked small spots turning dark brown or black with yellowish halos.",
            "Severe yellowing and dropping of infected leaves.",
            "Raised, blister-like rough scabby warts on the surface of green bell peppers."
        ],
        "solutions": {
            "organic": "Apply copper hydroxide mixed with Bacillus amyloliquefaciens bi-weekly.",
            "chemical": "Apply preventive copper bactericides tank-mixed with Mancozeb to overcome copper-tolerant strains.",
            "prevention": (
                "Use certified disease-free, hot-water treated seeds. "
                "Rotate with non-solanaceous crops for at least 2–3 years. "
                "Use drip irrigation instead of overhead sprinklers to prevent bacterial splashing."
            )
        }
    },
    "Pepper,_bell___healthy": {
        "crop": "Bell Pepper",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Smooth, dark green, ovate pepper leaves showing strong vegetative vigor and flowering capacity.",
        "symptoms": ["Glossy foliage, no lesions, clean leaf undersides."],
        "solutions": {
            "organic": "Feed with balanced organic tomato/vegetable fertilizer rich in potassium and calcium.",
            "chemical": "None needed.",
            "prevention": "Maintain consistent moisture and stake plants to prevent fruit from touching soil."
        }
    },
    "Potato___Early_blight": {
        "crop": "Potato",
        "condition": "Early Blight",
        "is_healthy": False,
        "cause": "Alternaria solani (Fungus)",
        "description": (
            "Early blight is a common fungal disease of potato and tomato foliage. It typically starts on older, "
            "lower leaves and forms characteristic 'target-board' concentric rings surrounded by yellow chlorotic tissue."
        ),
        "symptoms": [
            "Circular to angular brown spots with distinctive concentric rings ('target-board' pattern).",
            "Yellow halo encircling the dark lesions.",
            "Lower leaves turn yellow, dry up, and drop, exposing potato tubers to sunburn and reduced yields."
        ],
        "solutions": {
            "organic": (
                "Spray copper soap or bio-fungicide containing Bacillus subtilis as early preventive measures. "
                "Apply organic mulch to stop fungal spores splashing up from the soil."
            ),
            "chemical": (
                "Apply Chlorothalonil (Daconil), Mancozeb, or Azoxystrobin (Quadris) at 7–10 day intervals after canopy closure."
            ),
            "prevention": (
                "Avoid nitrogen deficiency or excessive vine stress which predisposes plants to Alternaria. "
                "Rotate crops away from potatoes and tomatoes for at least 3 years."
            )
        }
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "condition": "Late Blight",
        "is_healthy": False,
        "cause": "Phytophthora infestans (Oomycete water mold)",
        "description": (
            "Late blight is the infamous pathogen responsible for the Irish Potato Famine. It can destroy an entire field "
            "in days under cool, foggy, or wet conditions (10–20°C and >90% humidity)."
        ),
        "symptoms": [
            "Large, irregular, water-soaked dark brown or black lesions starting at leaf tips and edges.",
            "Delicate white downy fungal-like growth visible on the underside of leaves around lesion borders in humid mornings.",
            "Rapid stem rot turning black and collapsing, followed by brown rot inside tubers."
        ],
        "solutions": {
            "organic": (
                "Immediately destroy and dispose of infected plants in sealed bags. Do not compost. "
                "Apply fixed copper fungicides before rainy spells as a protective shield on healthy vines."
            ),
            "chemical": (
                "Apply targeted oomycete fungicides: Mandipropamid (Revus), Cymoxanil (Curzate), or Fluopicolide (Presidio). "
                "Act quickly upon receiving regional Late Blight forecasts or alerts."
            ),
            "prevention": (
                "Plant certified disease-free seed tubers; never plant grocery store sprouting potatoes. "
                "Eliminate cull piles and volunteer potato plants where the pathogen overwinters. "
                "Hill soil deeply over tubers to prevent spores washing into the soil and rotting tubers."
            )
        }
    },
    "Potato___healthy": {
        "crop": "Potato",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Deep green compound potato leaves with lush spreading growth and strong tuberization potential.",
        "symptoms": ["Intact leaflets, crisp green stems, no blighted margins."],
        "solutions": {
            "organic": "Hill soil regularly and supply balanced organic fertilizers.",
            "chemical": "None needed.",
            "prevention": "Ensure well-drained soil and scout weekly for Colorado potato beetles and blight signs."
        }
    },
    "Raspberry___healthy": {
        "crop": "Raspberry",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Healthy serrated composite raspberry foliage with pale green undersides and strong canes.",
        "symptoms": ["Clean green leaf blades, no rust or anthracnose spots."],
        "solutions": {
            "organic": "Annual cane thinning and organic straw mulching.",
            "chemical": "None needed.",
            "prevention": "Prune out spent floricanes after fruiting to improve sunlight penetration and cane health."
        }
    },
    "Soybean___healthy": {
        "crop": "Soybean",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Trifoliate green leaves with clean surface and strong nitrogen fixation nodules in the root zone.",
        "symptoms": ["Uniform green trifoliate foliage, no rust or mosaic symptoms."],
        "solutions": {
            "organic": "Inoculate seeds with Bradyrhizobium japonicum before planting for biological nitrogen fixation.",
            "chemical": "None needed.",
            "prevention": "Practice good crop rotation and weed control."
        }
    },
    "Squash___Powdery_mildew": {
        "crop": "Squash / Cucurbits",
        "condition": "Powdery Mildew",
        "is_healthy": False,
        "cause": "Podosphaera xanthii (Fungus)",
        "description": (
            "Powdery mildew affects squash, pumpkins, cucumbers, and melons. A white talcum-powder-like coating covers "
            "leaves, leading to early leaf death and sunburned, tasteless fruit."
        ),
        "symptoms": [
            "White circular powdery spots on both upper and lower leaf surfaces and petioles.",
            "Infected leaves turn yellow, then brown and papery, and wither completely.",
            "Exposed squash fruit suffers sunburn and poor sugar development."
        ],
        "solutions": {
            "organic": (
                "Spray potassium bicarbonate (Kaligreen) or baking soda solution (1 tbsp baking soda + 1 tsp liquid soap per gallon of water). "
                "Spray 1:9 milk-to-water dilution under bright sunlight; milk proteins produce antiseptic free radicals in UV light."
            ),
            "chemical": (
                "Apply systemic fungicides: Trifloxystrobin (Flint), Myclobutanil, or Metrafenone (Vivando) early in disease onset."
            ),
            "prevention": (
                "Plant resistant squash cultivars (e.g., 'Dunja', 'Success PM', 'Honeyboat'). "
                "Space squash hills 4–6 feet apart to promote airflow and quick drying."
            )
        }
    },
    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry",
        "condition": "Leaf Scorch",
        "is_healthy": False,
        "cause": "Diplocarpon earlianum (Fungus)",
        "description": (
            "Leaf scorch produces numerous small purple to dark brown irregular spots on strawberry foliage. "
            "As spots coalesce, the entire leaf looks scorched or burned by fire."
        ),
        "symptoms": [
            "Small irregular purple or dark brown spots on upper leaf surfaces without light white centers.",
            "Spots merge, causing the leaf margins to curl upward and turn brown and burnt.",
            "Weakened crowns and diminished runner production."
        ],
        "solutions": {
            "organic": "Remove and destroy severely affected leaves after harvest; apply copper soap in early spring.",
            "chemical": "Apply Captan or Pyraclostrobin + Boscalid (Pristine) during early bloom periods.",
            "prevention": (
                "Renovate strawberry beds after harvest by mowing old foliage without damaging crowns. "
                "Use drip irrigation rather than overhead sprinklers."
            )
        }
    },
    "Strawberry___healthy": {
        "crop": "Strawberry",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Vibrant trifoliate strawberry leaves with healthy serrations and strong stolon/runner growth.",
        "symptoms": ["Bright green glossy leaves, clear veins, clean petioles."],
        "solutions": {
            "organic": "Keep crowns mulched with clean straw to keep leaves and berries off bare wet soil.",
            "chemical": "None needed.",
            "prevention": "Ensure full sun exposure (6+ hours daily) and well-draining sandy loam soil."
        }
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "condition": "Bacterial Spot",
        "is_healthy": False,
        "cause": "Xanthomonas perforans / Xanthomonas vesicatoria (Bacteria)",
        "description": (
            "A bacterial disease causing dark, water-soaked, greasy spots on leaves, stems, and tomatoes. "
            "It spreads quickly through splashing rain, overhead irrigation, and handling wet plants."
        ),
        "symptoms": [
            "Small (less than 3 mm), dark, water-soaked greasy spots on leaves.",
            "Yellowing around spots with leaves taking on a scorched appearance.",
            "Small, raised, scab-like blister spots on green fruit."
        ],
        "solutions": {
            "organic": "Apply Bacillus subtilis or copper octanoate bio-pesticides every 7 days during wet weather.",
            "chemical": "Apply a combination of copper hydroxide and Mancozeb to tackle copper-resistant bacterial strains.",
            "prevention": (
                "Never work in tomato patches when foliage is wet. "
                "Use drip irrigation and maintain a 3-year crop rotation away from peppers and tomatoes. "
                "Sterilize trellises, stakes, and tomato cages at the end of each season."
            )
        }
    },
    "Tomato___Early_blight": {
        "crop": "Tomato",
        "condition": "Early Blight",
        "is_healthy": False,
        "cause": "Alternaria linariae (Alternaria solani) (Fungus)",
        "description": (
            "One of the most frequent tomato diseases worldwide. It typically begins on the lowest, oldest leaves "
            "and works upward, causing yellowing, defoliation, and fruit stem rot."
        ),
        "symptoms": [
            "Brown-to-black circular spots with concentric target-ring rings.",
            "Yellow halo around lesions, followed by entire leaf yellowing and dropping.",
            "Dark, sunken, velvety cankers at the soil line on stems and on fruit shoulder."
        ],
        "solutions": {
            "organic": (
                "Prune off the lowest 12–18 inches of tomato branches once the plant reaches 3 feet to prevent soil contact. "
                "Apply thick organic mulch (straw or wood chips) to prevent rain splash. "
                "Spray copper bio-fungicide or neem oil preventively."
            ),
            "chemical": "Spray Chlorothalonil (Daconil), Mancozeb, or Azoxystrobin every 7–10 days during warm, humid conditions.",
            "prevention": (
                "Stake or cage indeterminate tomatoes to keep foliage elevated and dry. "
                "Rotate solanaceous crops on a 3-year cycle."
            )
        }
    },
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "condition": "Late Blight",
        "is_healthy": False,
        "cause": "Phytophthora infestans (Oomycete)",
        "description": (
            "A rapidly destructive water mold capable of killing healthy tomato plants in less than a week. "
            "It turns leaves, stems, and green fruit into greasy, rotting brown tissue."
        ),
        "symptoms": [
            "Large, dark, water-soaked pale-green to brown greasy lesions on leaves.",
            "White fuzzy growth on leaf undersides in high humidity.",
            "Brown to purplish-black lesions on stems, causing stems to snap.",
            "Firm, greasy, golden-brown rot on green and ripe tomato fruit."
        ],
        "solutions": {
            "organic": "Immediately remove and bag all infected plants; do not compost. Apply preventative copper fungicides.",
            "chemical": "Apply Mandipropamid (Revus), Chlorothalonil, or Cymoxanil immediately upon regional blight warnings.",
            "prevention": (
                "Choose blight-resistant tomato varieties (e.g. 'Mountain Magic', 'Defiant', 'Iron Lady'). "
                "Provide maximum spacing between plants and avoid overhead watering."
            )
        }
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "condition": "Leaf Mold",
        "is_healthy": False,
        "cause": "Passalora fulva (Cladosporium fulvum) (Fungus)",
        "description": (
            "Common in high tunnels and greenhouses with high humidity (>85%) and poor air movement. "
            "It affects primarily leaves, severely diminishing photosynthetic capacity."
        ),
        "symptoms": [
            "Pale green to yellow spots on the upper leaf surface with indefinite margins.",
            "Dense olive-green to gray velvety mold growth on the corresponding lower leaf surface.",
            "Leaves curl, turn brown, wither, and drop prematurely."
        ],
        "solutions": {
            "organic": "Increase greenhouse ventilation and run circulation fans. Apply copper-based or Serenade bio-fungicides.",
            "chemical": "Apply Chlorothalonil, Difenoconazole (Inspire Super), or Pyraclostrobin.",
            "prevention": (
                "Maintain greenhouse relative humidity below 80% via heat venting and fan air exchanges. "
                "Drip irrigate and avoid wetting tomato foliage."
            )
        }
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato",
        "condition": "Septoria Leaf Spot",
        "is_healthy": False,
        "cause": "Septoria lycopersici (Fungus)",
        "description": (
            "A very prevalent destructive fungal disease that starts on lower leaves after fruit set. "
            "Leaves become speckled with hundreds of tiny circular spots, leading to rapid defoliation and sunscalded fruit."
        ),
        "symptoms": [
            "Numerous small, circular spots (1.5 to 3 mm) with dark brown margins and white/gray centers.",
            "Tiny black specks (pycnidia) visible inside the center of mature spots under magnification.",
            "Leaves turn completely yellow, wither, and drop off in large numbers from the bottom up."
        ],
        "solutions": {
            "organic": "Prune lower leaves to maintain a 12-inch gap above ground. Mulch deeply. Apply copper or bio-fungicide sprays.",
            "chemical": "Apply Chlorothalonil (Daconil), Mancozeb, or Boscalid early in the season before spots proliferate.",
            "prevention": (
                "Space tomato plants at least 2.5–3 feet apart to permit maximum airflow. "
                "Clean up and burn all dead tomato debris in autumn."
            )
        }
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato",
        "condition": "Two-Spotted Spider Mite Infestation",
        "is_healthy": False,
        "cause": "Tetranychus urticae (Arachnid mite pest)",
        "description": (
            "Tiny arachnids that feed by piercing plant cells and sucking out chlorophyll. "
            "They multiply explosively during hot, dry, dusty weather, spinning dense silky webs over leaves and fruit."
        ),
        "symptoms": [
            "Fine yellow stippling or white speckling on upper leaf surfaces.",
            "Silky, fine webbing covering the underside of leaves, growing tips, and flower clusters.",
            "Leaves turn bronze or yellow, dry up, and plants become severely stunted."
        ],
        "solutions": {
            "organic": (
                "Spray insecticidal soap or horticultural oil (neem oil) thoroughly on leaf undersides every 4–5 days. "
                "Release predatory mites (Phytoseiulus persimilis or Neoseiulus californicus) in greenhouses and gardens. "
                "Wash plants with a strong stream of cold water to disrupt webs and knock mites off."
            ),
            "chemical": "Apply selective miticides such as Bifenazate (Acramite) or Spiromesifen (Oberon). Avoid synthetic pyrethroids which kill beneficial predatory insects.",
            "prevention": "Avoid dusty conditions by keeping paths mulched or damp. Keep plants adequately irrigated to avoid water stress."
        }
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato",
        "condition": "Target Spot",
        "is_healthy": False,
        "cause": "Corynespora cassiicola (Fungus)",
        "description": (
            "Target spot causes brown lesions with concentric rings on leaves, stems, and tomato fruit in humid conditions. "
            "Fruit lesions develop into deep, sunken circular craters."
        ),
        "symptoms": [
            "Brown circular lesions with distinct concentric target-like rings.",
            "Leaf spots turn necrotic and centers may drop out.",
            "Circular, sunken, firm lesions on ripe and green fruit."
        ],
        "solutions": {
            "organic": "Apply copper fungicides or bio-fungicides; improve plant spacing and remove infected leaves.",
            "chemical": "Spray Azoxystrobin, Chlorothalonil, or Famoxadone + Cymoxanil.",
            "prevention": "Avoid overhead watering; remove old crop debris promptly."
        }
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "condition": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "is_healthy": False,
        "cause": "Geminiviridae transmitted exclusively by Silverleaf Whiteflies (Bemisia tabaci)",
        "description": (
            "A devastating viral disease transmitted by tiny whiteflies. It causes severe plant stunting, "
            "upward cupping of leaves with bright yellow margins, and near-total cessation of fruit production."
        ),
        "symptoms": [
            "Severe upward curling and cupping of leaflets into a boat-like shape.",
            "Interveinal yellowing (chlorosis) and distinct yellow margins on young leaves.",
            "Extreme plant stunting and bushy growth habit.",
            "Flower abortion resulting in minimal or zero fruit set."
        ],
        "solutions": {
            "organic": (
                "Install fine 50-mesh insect netting over nursery plants to exclude whiteflies. "
                "Use yellow sticky traps to monitor and trap whitefly adults. "
                "Spray insecticidal soaps, neem oil, or pyrethrins to control whitefly nymphs on leaf undersides."
            ),
            "chemical": (
                "There is no cure for the virus once contracted; infected plants must be removed immediately. "
                "Apply systemic insecticides (Dinotefuran, Spiromesifen) to control whitefly vector populations."
            ),
            "prevention": (
                "Plant TYLCV-resistant tomato hybrids (e.g., 'Tycoon', 'Charger', 'Tribute'). "
                "Immediately pull out and seal infected plants in plastic bags to stop whiteflies spreading virus."
            )
        }
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato",
        "condition": "Tomato Mosaic Virus (ToMV)",
        "is_healthy": False,
        "cause": "Tobamovirus (Extremely stable mechanical virus)",
        "description": (
            "Tomato mosaic virus is an exceptionally durable virus transmitted mechanically through hands, tools, "
            "clothing, contaminated seeds, and tobacco products. It causes mottled foliage and internal fruit browning."
        ),
        "symptoms": [
            "Mottling of leaves with alternating light green and dark green mosaic patches.",
            "Leaves may become distorted, curled, or strap-like ('fern-leaf' or shoestring effect).",
            "Internal browning of the fruit wall (brown wall) and uneven fruit ripening."
        ],
        "solutions": {
            "organic": (
                "Immediately remove and burn infected plants. Do not compost. "
                "Dip gardening tools in a 20% non-fat dry milk solution or 10% bleach between plants; milk proteins inactivate Tobamoviruses."
            ),
            "chemical": "No chemical virucides exist. Management relies entirely on strict sanitation and vector hygiene.",
            "prevention": (
                "Plant certified disease-free seeds and virus-resistant varieties (marked with 'T' or 'ToMV'). "
                "Smokers and tobacco users must thoroughly wash hands with soap before touching plants. "
                "Eliminate solanaceous weeds (nightshade, horsenettle) around the garden."
            )
        }
    },
    "Tomato___healthy": {
        "crop": "Tomato",
        "condition": "Healthy Foliage",
        "is_healthy": True,
        "cause": "Optimal plant health - No pathogen detected",
        "description": "Vibrant, sturdy, deep green tomato foliage with robust stems, active flowering clusters, and no signs of disease.",
        "symptoms": ["Evenly colored pinnate green leaves, strong erect stems, healthy blossom clusters."],
        "solutions": {
            "organic": "Support steady growth with calcium-rich organic fertilizer (bone meal, crushed eggshells) to prevent blossom end rot.",
            "chemical": "No chemical treatment required.",
            "prevention": "Maintain 2–3 inches of straw mulch, prune suckers for optimal air passage, and deep water once or twice a week at the base."
        }
    }
}

def get_disease_details(disease_key: str) -> Dict[str, Any]:
    """Retrieve full description, cause, symptoms, and solutions for a predicted class."""
    if disease_key in DISEASE_DATABASE:
        data = dict(DISEASE_DATABASE[disease_key])
        data["key"] = disease_key
        data["display_name"] = disease_key.replace("___", " — ").replace("_", " ")
        return data

    # Fallback for unexpected or generic classes
    parts = disease_key.split("___")
    crop = parts[0].replace("_", " ") if parts else "Plant"
    condition = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"
    is_healthy = "healthy" in condition.lower()

    return {
        "key": disease_key,
        "display_name": f"{crop} — {condition}",
        "crop": crop,
        "condition": condition,
        "is_healthy": is_healthy,
        "cause": "No pathogen detected" if is_healthy else "Pathogenic agent under diagnostic evaluation",
        "description": f"The leaf shows characteristics consistent with {condition} on {crop}.",
        "symptoms": ["Normal appearance" if is_healthy else f"Visual signs of {condition}."],
        "solutions": {
            "organic": "Maintain regular organic soil nutrition and water management.",
            "chemical": "Consult local agricultural extension if disease symptoms expand.",
            "prevention": "Ensure good spacing, weed removal, and crop rotation."
        }
    }


def get_disease_details_gujarati(disease_key: str) -> Dict[str, Any]:
    """
    Retrieve Gujarati-translated disease details.
    Falls back gracefully to English if a Gujarati entry is not available.
    """
    from gujarati_data import GUJARATI_DISEASE_INFO, CROP_GUJARATI

    # Get the English base first (always needed for is_healthy, display_name fallback)
    english = get_disease_details(disease_key)

    if disease_key not in GUJARATI_DISEASE_INFO:
        # Return English data with a note that Gujarati is unavailable
        return english

    gu = GUJARATI_DISEASE_INFO[disease_key]

    # Resolve Gujarati crop name from the crop key map
    crop_key = disease_key.split("___")[0] if "___" in disease_key else ""
    gu_crop = CROP_GUJARATI.get(crop_key, gu.get("crop", english["crop"]))

    return {
        "key": disease_key,
        "display_name": f"{gu_crop} — {gu.get('condition', english['condition'])}",
        "crop": gu_crop,
        "condition": gu.get("condition", english["condition"]),
        "is_healthy": english["is_healthy"],
        "cause": gu.get("cause", english["cause"]),
        "description": gu.get("description", english["description"]),
        "symptoms": gu.get("symptoms", english["symptoms"]),
        "solutions": gu.get("solutions", english["solutions"]),
    }
