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
        'GO:1901206',
        'positive regulation of adrenergic receptor signaling pathway involved in heart process',
        'biological_process',
        '"Any process that activates or increases the frequency, rate or extent '
        'of a cardiac adrenergic receptor signaling pathway." [GOC:BHF, GOC:mtg_'
        'cardiac_conduct_nov11, GOC:rl, GOC:TermGenie]',
        1,
        [
            (
                'GO:1903247',
                'positive regulation of adrenergic receptor signaling pathway '
                'involved in positive regulation of heart rate',
                'biological_process',
                '"Any process that activates or increases the frequency, rate or extent of '
                'adrenergic receptor signaling pathway involved in positive regulation of '
                'heart rate." [GO_REF:0000058, GOC:BHF, GOC:mtg_cardiac_conduct_nov11, GOC:rl, '
                'GOC:TermGenie, PMID:17242280]',
                0
            )
        ]
    ),
    (
        'GO:1904552',
        'regulation of chemotaxis to arachidonic acid',
        'biological_process',
        '"Any process that modulates the frequency, rate or extent of chemotaxis to arachidonic acid." '
        '[GO_REF:0000058, GOC:TermGenie, PMID:16382163]',
        2,
        [
            (
                'GO:1904553',
                'negative regulation of chemotaxis to arachidonic acid',
                'biological_process',
                '"Any process that stops, prevents or reduces the frequency, rate or extent of '
                'chemotaxis to arachidonic acid." [GO_REF:0000058, GOC:TermGenie, PMID:16382163]',
                0
            ),
            (
                'GO:1904554',
                'positive regulation of chemotaxis to arachidonic acid',
                'biological_process',
                '"Any process that activates or increases the frequency, rate or extent of chemotaxis '
                'to arachidonic acid." [GO_REF:0000058, GOC:TermGenie, PMID:16382163]',
                0
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
        'MP:0001947',
        'abnormal mucociliary clearance',
        '',
        '"anomaly in the mechanism that removes mucus and other foreign particles and microorganisms '
        'from the lungs by directed ciliary movement and secretory activity of the tracheobronchial '
        'submucosal glands" [MESH:E01.370.386.520, MGI:csmith, MGI:mnk]',
        2,
        [
            (
                'MP:0010752',
                'impaired mucociliary clearance',
                '',
                '"reduced ability to remove mucus and other foreign particles and microorganisms '
                'from the lungs by directed ciliary movement and secretory activity of the '
                'tracheobronchial submucosal glands" [MESH:E01.370.386.520, MGI:csmith]',
                0
            ),
            (
                'MP:0010753',
                'improved mucociliary clearance',
                '',
                '"enhanced ability to remove mucus and other foreign particles and microorganisms '
                'from the lungs by directed ciliary movement and secretory activity of the '
                'tracheobronchial submucosal glands" [MESH:E01.370.386.520, MGI:csmith]',
                0
            )
        ]
    ),
    (
        'MP:0003656',
        'abnormal erythrocyte physiology',
        '',
        '"aberrant measurable or observable characteristic related to the function '
        'of or processes in the cells in the blood that carry oxygen, red blood cells" [MPD:Molly]',
        19,
        [
            (
                'MP:0003657',
                'abnormal erythrocyte osmotic lysis',
                '',
                '"increase or decrease in the ability of RBCs to withstand changes in osmolarity" [MGI:smb]',
                0
            ),
            (
                'MP:0010034',
                'abnormal erythrocyte clearance',
                '',
                '"any anomaly in the selective elimination of aging erythrocytes from the '
                'body by autoregulatory mechanisms, often expressed as half-life" [GO:0034102, MGI:csmith]',
                2
            ),
            (
                'MP:0010035',
                'increased erythrocyte clearance',
                '',
                '"increased elimination of aging erythrocytes from the body by autoregulatory mechanisms, '
                'often expressed as half-life" [GO:0034102, MGI:csmith]',
                0
            ),
            (
                'MP:0010036',
                'decreased erythrocyte clearance',
                '',
                '"decreased elimination of aging erythrocytes from the body by autoregulatory mechanisms, '
                'often expressed as half-life" [GO:0034102, MGI:csmith]',
                0
            ),
            (
                'MP:0010163',
                'hemolysis',
                '',
                '"destruction of erythrocytes such that hemoglobin is released from the cells; '
                'may occur by many different causal agents such as antibodies, bacteria, chemicals, '
                'temperature, and changes in tonicity" [ISBN:0-683-40008-8]',
                1
            ),
            (
                'MP:0011245',
                'abnormal fetal derived definitive erythrocyte physiology',
                '',
                '"any functional anomaly of a fetal liver derived enucleated erythrocyte, '
                'which matures in macrophage islands within the liver, enucleates, '
                'and then enters the bloodstream; these resemble adult erythrocytes in that '
                'they are small (3- to 6- times smaller than primitive erythrocytes) and produce '
                'adult hemoglobins" [CL:0002357, PMID:18282515]',
                0
            ),
            (
                'MP:0012384',
                'abnormal erythrocyte ion transport',
                '',
                '"aberrant measurable or observable characteristic related to the movement in red '
                'blood cells of atoms carrying an electric charge" [MPD:Molly]',
                12
            ),
            (
                'MP:0012385',
                'abnormal erythrocyte potassium:chloride symporter activity',
                '',
                '"aberrant catalysis in red blood cells of the transfer of a solute or solutes from '
                'one side of a membrane to the other according to the reaction: K+(out) + Cl-(out) '
                '= K+(in) + Cl-(in)" [GO:0015379, MPD:Molly]',
                2
            ),
            (
                'MP:0012386',
                'decreased erythrocyte potassium:chloride symporter activity',
                '',
                '"decreased catalysis in red blood cells of the transfer of a solute or '
                'solutes from one side of a membrane to the other according to the reaction: '
                'K+(out) + Cl-(out) = K+(in) + Cl-(in)" [MPD:Molly]',
                0
            ),
            (
                'MP:0012387',
                'increased erythrocyte potassium:chloride symporter activity',
                '',
                '"increased catalysis in red blood cells of the transfer of a solute or '
                'solutes from one side of a membrane to the other according to the reaction: '
                'K+(out) + Cl-(out) = K+(in) + Cl-(in)" [MPD:Molly]',
                0
            ),
            (
                'MP:0012388',
                'abnormal erythrocyte sodium:hydrogen antiporter activity',
                '',
                '"aberrant catalysis in red blood cells of the transfer of a solute or '
                'solutes from one side of a membrane to the other according to the reaction: '
                'Na+(out) + H+(in) = Na+(in) + H+(out)" [GO:0015385, MPD:Molly]',
                2
            ),
            (
                'MP:0012389',
                'decreased erythrocyte sodium:hydrogen antiporter activity',
                '',
                '"decreased catalysis in red blood cells of the transfer of a solute or '
                'solutes from one side of a membrane to the other according to the reaction: '
                'Na+(out) + H+(in) = Na+(in) + H+(out)" [MPD:Molly]',
                0
            ),
            (
                'MP:0012390',
                'increased erythrocyte sodium:hydrogen antiporter activity',
                '',
                '"increased catalysis in red blood cells of the transfer of a solute or '
                'solutes from one side of a membrane to the other according to the reaction: '
                'Na+(out) + H+(in) = Na+(in) + H+(out)" [MPD:Molly]',
                0
            ),
            (
                'MP:0012391',
                'abnormal erythrocyte sodium:potassium-exchanging ATPase activity',
                '',
                '"aberrant catalysis in red blood cells of the transfer of a solute or '
                'solutes from one side of a membrane to the other according to the reaction: '
                'ATP + H2O + Na+(in) + K+(out) = ADP + phosphate + Na+(out) + K+(in)" [GO:0005391, MPD:Molly]',
                2
            ),
            (
                'MP:0012392',
                'decreased erythrocyte sodium:potassium-exchanging ATPase activity',
                '',
                '"decreased catalysis in red blood cells of the transfer of a solute or '
                'solutes from one side of a membrane to the other according to the reaction: '
                'ATP + H2O + Na+(in) + K+(out) = ADP + phosphate + Na+(out) + K+(in)" [MPD:Molly]',
                0
            ),
            (
                'MP:0012393',
                'increased erythrocyte sodium:potassium-exchanging ATPase activity',
                '',
                '"increased catalysis in red blood cells of the transfer of a solute or '
                'solutes from one side of a membrane to the other according to the reaction: '
                'ATP + H2O + Na+(in) + K+(out) = ADP + phosphate + Na+(out) + K+(in)" [MPD:Molly]',
                0
            ),
            (
                'MP:0012394',
                'abnormal erythrocyte calcium-activated potassium channel activity',
                '',
                '"aberrant catalysis in red blood cells of the calcium concentration-regulatable '
                'energy-independent passage of potassium ions across a lipid bilayer down a '
                'concentration gradient" [GO:0015269, MPD:Molly]',
                2
            ),
            (
                'MP:0012395',
                'decreased erythrocyte calcium-activated potassium channel activity',
                '',
                '"decreased catalysis in red blood cells of the calcium concentration-regulatable '
                'energy-independent passage of potassium ions across a lipid bilayer down a '
                'concentration gradient" [MPD:Molly]',
                0
            ),
            (
                'MP:0012396',
                'increased erythrocyte calcium-activated potassium channel activity',
                '',
                '"increased catalysis in red blood cells of the calcium concentration-regulatable '
                'energy-independent passage of potassium ions across a lipid bilayer down a '
                'concentration gradient" [MPD:Molly]',
                0
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
        'DOID:0080100',
        'congenital myopathy',
        '',
        '',
        3,
        [
            ('DOID:0080101', 'Compton-North congenital myopathy', '', '', 0),
            ('DOID:0080102', 'congenital fiber-type disproportion', '', '', 0),
            ('DOID:0080103', 'cylindrical spirals myopathy', '', '', 0)
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