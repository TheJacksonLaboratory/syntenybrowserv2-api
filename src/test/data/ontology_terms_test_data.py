ONTOLOGY_TERMS_DATA = [
    (
        'GO:0000001',
        'mitochondrion inheritance',
        'biological_process',
        '"The distribution of mitochondria, including the mitochondrial genome, '
        'into daughter cells after mitosis or meiosis, mediated by interactions ' 
        'between mitochondria and the cytoskeleton." [GOC:mcc, PMID:10873824, PMID:11389764]',
        0,
        []
    ),
    (
        'GO:0033862',
        'UMP kinase activity',
        'molecular_function',
        '"Catalysis of the reaction: ATP + UMP = ADP + UDP." [EC:2.7.4.22]',
        0,
        []
    ),
    (
        'GO:0006435',
        'threonyl-tRNA aminoacylation',
        'biological_process',
        '"The process of coupling threonine to threonyl-tRNA, catalyzed by threonyl-tRNA synthetase. '
        'In tRNA aminoacylation, the amino acid is first activated by linkage to AMP and then transferred '
        'to either the 2\'- or the 3\'-hydroxyl group of the 3\'-adenosine residue of the tRNA." '
        '[GOC:mcc, ISBN:0716730510]',
        1,
        [
            (
                'GO:0070159',
                'mitochondrial threonyl-tRNA aminoacylation',
                'biological_process',
                '"The process of coupling threonine to threonyl-tRNA in a mitochondrion, '
                'catalyzed by threonyl-tRNA synthetase. In tRNA aminoacylation, the amino acid '
                'is first activated by linkage to AMP and then transferred to either the '
                '2\'- or the 3\'-hydroxyl group of the 3\'-adenosine residue of the tRNA." [GOC:mah, GOC:mcc]',
                0,
                []
            )
        ]
    ),
    (
        'GO:0046983',
        'protein dimerization activity',
        'molecular_function',
        '"The formation of a protein dimer, a macromolecular structure consists of two noncovalently '
        'associated identical or nonidentical subunits." [ISBN:0198506732]',
        2,
        [
            (
                'GO:0042803',
                'protein homodimerization activity',
                'molecular_function',
                '"Interacting selectively and non-covalently with an identical '
                'protein to form a homodimer." [GOC:jl]',
                0,
                []
            ),
            (
                'GO:0046982',
                'protein heterodimerization activity',
                'molecular_function',
                '"Interacting selectively and non-covalently with a nonidentical '
                'protein to form a heterodimer." [GOC:ai]',
                0,
                []
            )
        ]
    ),
    (
        'GO:2001063',
        'glucomannan binding',
        'molecular_function',
        '"Interacting selectively and non-covalently with glucomannan." [GOC:mengo_curators]',
        0,
        []
    ),
    (
        'MP:0002083',
        'premature death',
        '',
        '"death after weaning age, but before the normal life span (Mus: after 3 weeks of age)" [MGI:csmith]',
        1,
        [
            (
                'MP:0008028',
                'pregnancy-related premature death',
                '',
                '"death occurring before the normal life span of an organism, occurring during '
                'pregnancy, parturition or lactation" [MGI:csmith, MGI:hdene]',
                0,
                []
            )
        ]
    ),
    (
        'MP:0001265',
        'decreased body size',
        '',
        '"smaller than average body weight, height and/or length of an organism compared '
        'to controls" [ISBN:0-683-40008-8, PMID:7854452]',
        9,
        [
            (
                'MP:0001255',
                'decreased body height',
                '',
                '"decreased shoulder to floor distance compared to controls" [MGI:dlb]',
                0,
                []
            ),
            (
                'MP:0001258',
                'decreased body length',
                '',
                '"decreased measure of the head and trunk (head, thorax and abdomen) '
                'in the rostral-caudal direction" [MGI:csmith]',
                0,
                []
            ),
            (
                'MP:0001262',
                'decreased body weight',
                '',
                '"lower than normal average weight" [PMID:10709991]',
                3,
                [
                    (
                        'MP:0001263',
                        'weight loss',
                        '',
                        '"progressive reduction of body weight below normal average for age" [PMID:9420327]',
                        0,
                        [
                            'MP:0005150',
                            'cachexia',
                            '',
                            '"general weight loss and wasting occurring in the course of chronic disease" '
                            '[ISBN:0-683-40008-8]',
                            0,
                            []
                        ]
                    ),
                    (
                        'MP:0005150',
                        'cachexia',
                        '',
                        '"general weight loss and wasting occurring in the course of chronic disease" '
                        '[ISBN:0-683-40008-8]',
                        0,
                        []
                    ),
                    (
                        'MP:0008489',
                        'slow postnatal weight gain',
                        '',
                        '"the weight gain over a span of postnatal developmental time is slower than controls, '
                        'with or without ever attaining a similar weight to controls as adults" [MGI:csmith]',
                        0,
                        []
                    )
                ]
            ),
            (
                'MP:0001263',
                'weight loss',
                '',
                '"progressive reduction of body weight below normal average for age" [PMID:9420327]',
                1,
                [
                    'MP:0005150',
                    'cachexia',
                    '',
                    '"general weight loss and wasting occurring in the course of chronic disease" [ISBN:0-683-40008-8]',
                    0,
                    []
                ]
            ),
            (
                'MP:0002427',
                'disproportionate dwarf',
                '',
                '"abnormally undersized with disproportionate body parts; usually with '
                'more significant shortening of the limbs in proportion to the trunk size" '
                '[ISBN:0-683-40008-8, MGI:csmith]',
                0,
                []
            ),
            (
                'MP:0005150',
                'cachexia',
                '',
                '"general weight loss and wasting occurring in the course of chronic disease" [ISBN:0-683-40008-8]',
                0,
                []
            ),
            (
                'MP:0008489',
                'slow postnatal weight gain',
                '',
                '"the weight gain over a span of postnatal developmental time is slower than controls, '
                'with or without ever attaining a similar weight to controls as adults" [MGI:csmith]',
                0,
                []
            ),
            (
                'MP:0008974',
                'proportional dwarf',
                '',
                '"abnormally undersized with both limbs and trunk symmetrically shorter; '
                'usually due to chemical, endocrine, nutritional or nonosseous influences" '
                '[ISBN:0-683-40008-8, MGI:csmith]',
                0,
                []
            ),
            (
                'MP:0013138',
                'thin body',
                '',
                '"lean or slender in form" [MGI:Ahmad_Retha]',
                0,
                []
            )
        ]
    ),
    (
        'MP:0020001',
        'decreased response to antigen',
        '',
        '"decreased or weak immune response after exposure to an antigen" [GOC:NV]',
        0,
        []
    ),
    (
        'DOID:9119',
        'acute myeloid leukemia',
        '',
        '',
        1,
        [
            (
                'DOID:0060318',
                'acute promyelocytic leukemia',
                '',
                '"An acute myeloid leukemia characterized by accumulation of promyelocytes '
                'in the bone marrow and by a translocation between chromosomes 15 and 17." '
                '[url:http\\://en.wikipedia.org/wiki/Acute_promyelocytic_leukemia, '
                'url:http\\://ghr.nlm.nih.gov/condition/acute-promyelocytic-leukemia]',
                0,
                []
            )
        ]
    ),
    (
        'DOID:3523',
        'brain stem infarction',
        '',
        '"A brain infarction that is characterized by stroke of the brain stem '
        'that develops from blockage or narrowing in the arteries located_in the '
        'brainstem, has_material_basis_in damage to the cranial nerve nuclei '
        'and long tracts, has_symptom vertigo, has_symptom imbalance, has_symptom '
        'decreased level of arousal." [url:https\\://en.wikipedia.org/wiki/Brainstem, '
        'url:https\\://en.wikipedia.org/wiki/Brainstem_stroke_syndrome]',
        1,
        [
            (
                'DOID:3522',
                'lateral medullary syndrome',
                '',
                '"A brain stem infarction that is characterized by hoarseness, dizziness, '
                'nausea, located_in the lateral part of the medulla oblongata that develops '
                'from a blockage in the posterior inferior cerebellar artery or one of its '
                'branches or of the vertebral artery, has_symptom vertigo, has_symptom '
                'ipsilateral cerebellar signs, has_symptom contralateral sensory deficits '
                'of limbs and torso, has_symptom ipsilateral sensory deficits of face, '
                'has_symptom laryngeal, pharyngeal, and palatal hemiparalysis, has_symptom '
                'ipsilateral Horner\'s syndrome." [url:https\\://en.wikipedia.org/wiki/Lateral_medullary_syndrome]',
                0
            )
        ]
    )
]