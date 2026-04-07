import random

LEGAL_CASES = {
    "CASE-E01": {
        "case_id": "CASE-E01",
        "title": "Davis v. Skyline Apartments",
        "jurisdiction": "New York, USA",
        "year": 2023,
        "facts": "The plaintiff, Mr. Davis, moved out of his apartment on January 1st after his lease ended. The landlord, Skyline Apartments, has not returned his $2,000 security deposit. It has been 45 days. The landlord claims there was damage to the walls, but provided no itemized list of deductions as required by state law.",
        "case_type": "civil_dispute",
        "urgency": "low",
        "relevant_statutes": ["NY Gen Oblig Law § 7-108", "Security Deposit Return Act"],
        "statute_text": {
            "NY Gen Oblig Law § 7-108": "A landlord who receives a security deposit must hold it in trust for the tenant and may not commingle it with personal funds. Within 14 days of the tenant vacating, the landlord must provide an itemized statement and return the full deposit less permitted deductions. Failure to comply results in forfeiture of any right to retain any portion of the deposit.",
            "Security Deposit Return Act": "This Act mandates that security deposits remain the property of the tenant during the lease term. Landlords are prohibited from making deductions for ordinary wear and tear. Any deduction must be documented by receipts or estimates provided to the tenant within the statutory window."
        },
        "prior_precedents": ["Smith v. NY Rentals (2018)"],
        "parties": {"plaintiff": "Mr. Davis", "defendant": "Skyline Apartments"},
        "relief_sought": "Return of the $2,000 security deposit plus statutory penalties.",
        "difficulty": "easy",
        "expected_classification": "civil_dispute",
        "expected_resolution_elements": ["demand letter", "small claims court", "itemized list"]
    },
    "CASE-E02": {
        "case_id": "CASE-E02",
        "title": "State v. Johnson",
        "jurisdiction": "Texas, USA",
        "year": 2023,
        "facts": "The defendant was caught on camera stealing a bicycle worth $400 from outside a grocery store. The owner reported it immediately. The defendant was apprehended two blocks away with the bicycle.",
        "case_type": "criminal",
        "urgency": "high",
        "relevant_statutes": ["Texas Penal Code § 31.03", "Theft"],
        "statute_text": {
            "Texas Penal Code § 31.03": "A person commits an offense if he unlawfully appropriates property with intent to deprive the owner of property. Appropriation of property is unlawful if it is without the owner's effective consent. Intent may be inferred from the actor's conduct and surrounding circumstances.",
            "Theft": "Theft involves the unauthorized taking of another's property with the specific intent to permanently deprive the rightful owner of its use or value. For property valued under $500, the offense is typically classified as a Class C misdemeanor, unless specific aggravating factors are present."
        },
        "prior_precedents": ["State v. Miller (2015)"],
        "parties": {"plaintiff": "State of Texas", "defendant": "Johnson"},
        "relief_sought": "Criminal conviction for misdemeanor theft.",
        "difficulty": "easy",
        "expected_classification": "criminal",
        "expected_resolution_elements": ["misdemeanor", "restitution", "plea bargain"]
    },
    "CASE-E03": {
        "case_id": "CASE-E03",
        "title": "Acme Corp v. Beta Supplies",
        "jurisdiction": "Delaware, USA",
        "year": 2022,
        "facts": "Acme Corp signed a contract with Beta Supplies to deliver 1000 widgets by June 1st for $10,000. Beta Supplies never delivered the widgets and stopped responding to emails. Acme had to buy widgets from another supplier for $15,000.",
        "case_type": "contract",
        "urgency": "medium",
        "relevant_statutes": ["UCC Article 2", "Breach of Contract"],
        "statute_text": {
            "UCC Article 2": "Under the Uniform Commercial Code, a contract for the sale of goods may be made in any manner sufficient to show agreement. If a seller fails to make delivery, the buyer may 'cover' by making in good faith and without unreasonable delay any reasonable purchase of goods in substitution. The buyer may then recover the difference between the cost of cover and the contract price.",
            "Breach of Contract": "A breach occurs when a party fails to perform any term of a contract without a legitimate legal excuse. The non-breaching party is entitled to damages that place them in the position they would have occupied had the contract been fully performed. Direct damages include the cost of obtaining substitute performance from a third party."
        },
        "prior_precedents": ["WidgetCo v. Suppliers Inc (2010)"],
        "parties": {"plaintiff": "Acme Corp", "defendant": "Beta Supplies"},
        "relief_sought": "$5,000 in cover damages.",
        "difficulty": "easy",
        "expected_classification": "contract",
        "expected_resolution_elements": ["breach of contract", "cover damages", "demand notice"]
    },
    "CASE-E04": {
        "case_id": "CASE-E04",
        "title": "Williams v. City Transit",
        "jurisdiction": "Illinois, USA",
        "year": 2023,
        "facts": "Mrs. Williams slipped on a clearly marked wet floor at a city transit station. She broke her wrist. The transit authority had placed a bright yellow 'Wet Floor' sign directly over the spill 10 minutes prior to her fall.",
        "case_type": "tort",
        "urgency": "low",
        "relevant_statutes": ["Illinois Premises Liability Act", "Negligence"],
        "statute_text": {
            "Illinois Premises Liability Act": "The duty of care owed by an owner or occupier of premises to entrants is that of reasonable care under the circumstances regarding the state of the premises. This duty does not require an owner to warn of or protect against conditions that are open and obvious. Liability is precluded if the entrant's own negligence is the primary cause of the injury.",
            "Negligence": "To establish negligence, a plaintiff must prove the defendant owed a duty of care, breached that duty, and the breach proximately caused actual damages. In Illinois, comparative negligence rules apply, meaning a plaintiff's recovery is reduced by their percentage of fault. If the plaintiff is more than 50% at fault, they are barred from recovery."
        },
        "prior_precedents": ["Doe v. Transit Authority (2019)"],
        "parties": {"plaintiff": "Mrs. Williams", "defendant": "City Transit"},
        "relief_sought": "Medical expenses and pain and suffering.",
        "difficulty": "easy",
        "expected_classification": "tort",
        "expected_resolution_elements": ["assumption of risk", "comparative negligence", "premises liability"]
    },
    "CASE-M01": {
        "case_id": "CASE-M01",
        "title": "Innovate LLC v. Former Employee",
        "jurisdiction": "California, USA",
        "year": 2023,
        "facts": "A former software engineer at Innovate LLC developed a new app. The employee claims they worked on it only on weekends using their personal laptop. Innovate LLC claims the app directly competes with their upcoming product and uses proprietary algorithms the employee learned on the job. The employment contract includes a standard PIIA (Proprietary Information and Inventions Agreement).",
        "case_type": "IP",
        "urgency": "high",
        "relevant_statutes": ["CA Labor Code § 2870", "Defend Trade Secrets Act"],
        "statute_text": {
            "CA Labor Code § 2870": "Any provision in an employment agreement which provides that an employee shall assign their rights in an invention to their employer shall not apply to an invention for which no equipment, supplies, facility, or trade secret information of the employer was used and which was developed entirely on the employee’s own time. This section does not apply to inventions that relate to the employer's business or actual or demonstrably anticipated research or development.",
            "Defend Trade Secrets Act": "An owner of a trade secret that is misappropriated may bring a civil action if the trade secret is related to a product or service used in, or intended for use in, interstate or foreign commerce. Misappropriation includes the acquisition of a trade secret of another by a person who knows or has reason to know that the trade secret was acquired by improper means."
        },
        "prior_precedents": ["Tech Giants v. Startup (2020)"],
        "parties": {"plaintiff": "Innovate LLC", "defendant": "Former Employee"},
        "relief_sought": "Injunction to stop the release of the app and ownership of the IP.",
        "difficulty": "medium",
        "expected_classification": "IP",
        "expected_resolution_elements": ["trade secrets", "injunction", "labor code 2870", "PIIA"]
    },
    "CASE-M02": {
        "case_id": "CASE-M02",
        "title": "Events Co v. Grand Hotel",
        "jurisdiction": "Florida, USA",
        "year": 2021,
        "facts": "Events Co booked a conference room at Grand Hotel for May 2020. Due to a government-mandated pandemic lockdown, the event could not occur. Events Co demanded a refund of their $50,000 deposit. Grand Hotel refused, citing the contract's non-refundable deposit clause, though the contract also contains a force majeure clause.",
        "case_type": "contract",
        "urgency": "medium",
        "relevant_statutes": ["Florida Contract Law", "Force Majeure Doctrine"],
        "statute_text": {
            "Florida Contract Law": "Contracts in Florida are interpreted according to the plain meaning of their terms to give effect to the parties' intent. Where a contract is unambiguous, its terms are strictly enforced regardless of subsequent changes in economic conditions. Parol evidence is generally inadmissible to vary or contradict the clear written terms of an integrated agreement.",
            "Force Majeure Doctrine": "The force majeure doctrine excuses performance when a superseding event, beyond the control of the parties and not reasonably foreseeable, makes performance impossible or commercially impracticable. To invoke this defense, the specific event (e.g., government mandate, act of God) must be identified within the contract's force majeure clause or meet the common law standard for impossibility."
        },
        "prior_precedents": ["Concert Promoters v. Arena (2021)"],
        "parties": {"plaintiff": "Events Co", "defendant": "Grand Hotel"},
        "relief_sought": "Full refund of the $50,000 deposit.",
        "difficulty": "medium",
        "expected_classification": "contract",
        "expected_resolution_elements": ["force majeure", "impossibility of performance", "frustration of purpose"]
    },
    "CASE-M03": {
        "case_id": "CASE-M03",
        "title": "Martinez v. Global Logistics",
        "jurisdiction": "New York, USA",
        "year": 2022,
        "facts": "Mr. Martinez was terminated from Global Logistics after 10 years. The company cites consistent tardiness over the last month. Martinez claims he was fired because he recently requested FMLA leave to care for his sick spouse. He had no prior disciplinary record.",
        "case_type": "employment",
        "urgency": "medium",
        "relevant_statutes": ["Family and Medical Leave Act", "NY Labor Law"],
        "statute_text": {
            "Family and Medical Leave Act": "Eligible employees are entitled to take up to 12 workweeks of unpaid, job-protected leave in a 12-month period for specified family and medical reasons, including caring for a spouse with a serious health condition. It is unlawful for any employer to interfere with, restrain, or deny the exercise of or the attempt to exercise any right provided under this Act.",
            "NY Labor Law": "New York Labor Law provides additional protections against retaliatory discharge for employees who exercise their rights under state or federal leave laws. An employer may not discharge, threaten, penalize, or in any other manner discriminate against any employee because such employee has requested leave. Violations may result in back pay, liquidated damages, and mandatory reinstatement."
        },
        "prior_precedents": ["Smith v. Logistics Corp (2018)"],
        "parties": {"plaintiff": "Mr. Martinez", "defendant": "Global Logistics"},
        "relief_sought": "Reinstatement and back pay.",
        "difficulty": "medium",
        "expected_classification": "employment",
        "expected_resolution_elements": ["FMLA interference", "retaliation", "mixed motive", "pretext"]
    },
    "CASE-M04": {
        "case_id": "CASE-M04",
        "title": "Neighbors v. Industrial Plant",
        "jurisdiction": "Ohio, USA",
        "year": 2023,
        "facts": "A local industrial plant recently changed its manufacturing process, emitting a strong, foul odor that permeates the surrounding residential neighborhood. The neighbors claim they cannot open their windows or use their yards. The plant claims they are fully compliant with all EPA emission standards.",
        "case_type": "tort",
        "urgency": "medium",
        "relevant_statutes": ["Private Nuisance Doctrine", "Ohio EPA Regulations"],
        "statute_text": {
            "Private Nuisance Doctrine": "A private nuisance is a non-trespassory invasion of another's interest in the private use and enjoyment of land. The invasion must be substantial and unreasonable, judged by the standard of a person of ordinary sensibilities. A court will balance the utility of the defendant's conduct against the gravity of the harm to the plaintiff.",
            "Ohio EPA Regulations": "Facilities must comply with all emission standards set forth by the Ohio Environmental Protection Agency to protect public health and the environment. Compliance with these regulatory standards, while relevant, is not an absolute defense to a common law nuisance claim if the resulting odor still significantly interferes with the use of neighboring property."
        },
        "prior_precedents": ["Community v. Factory (2015)"],
        "parties": {"plaintiff": "Neighborhood Association", "defendant": "Industrial Plant"},
        "relief_sought": "Injunction to stop the odor and damages for loss of use and enjoyment of property.",
        "difficulty": "medium",
        "expected_classification": "tort",
        "expected_resolution_elements": ["private nuisance", "compliance with regulations", "injunction", "loss of enjoyment"]
    },
    "CASE-H01": {
        "case_id": "CASE-H01",
        "title": "Global Data Inc. Privacy Breach",
        "jurisdiction": "International (EU & USA)",
        "year": 2023,
        "facts": "Global Data Inc., headquartered in California with servers in Germany, suffered a data breach exposing the personal data of 500,000 EU citizens and 1 million California residents. The company delayed notifying users for 45 days while investigating. They are facing simultaneous investigations by the California Attorney General and the Irish DPC.",
        "case_type": "privacy",
        "urgency": "critical",
        "relevant_statutes": ["GDPR Article 33", "CCPA", "CPRA"],
        "statute_text": {
            "GDPR Article 33": "In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55. If the notification is not made within 72 hours, it shall be accompanied by reasons for the delay, as specified in cross-references to Articles 34 and 58 regarding communication to data subjects and investigative powers.",
            "CCPA": "Consumers have the right to request that a business disclose the categories and specific pieces of personal information the business has collected about them. Businesses must provide a clear and conspicuous 'Do Not Sell My Personal Information' link on their website. In the event of a data breach, the CCPA provides a private right of action for statutory damages, subject to certain notice and cure provisions under Section 1798.150.",
            "CPRA": "The California Privacy Rights Act (CPRA) amends the CCPA to establish a new agency, the California Privacy Protection Agency (CPPA), to enforce privacy laws. It introduces a new category of 'sensitive personal information' and imposes stricter requirements for data minimization and purpose limitation. Under Section 1798.100, businesses must provide consumers with the right to correct inaccurate personal information and limit the use of sensitive data."
        },
        "prior_precedents": ["EU DPC v. MegaCorp (2021)"],
        "parties": {"plaintiff": "Regulatory Authorities & Class Action", "defendant": "Global Data Inc."},
        "relief_sought": "Massive regulatory fines and class-action damages.",
        "difficulty": "hard",
        "expected_classification": "privacy",
        "expected_resolution_elements": ["GDPR 72-hour rule", "CCPA notification", "cross-border data transfer", "class action defense"]
    },
    "CASE-H02": {
        "case_id": "CASE-H02",
        "title": "AlphaCorp M&A Dispute",
        "jurisdiction": "Delaware, USA",
        "year": 2024,
        "facts": "AlphaCorp acquired BetaTech for $500M. Post-acquisition, AlphaCorp discovered BetaTech was embroiled in an undisclosed, massive patent infringement lawsuit in another jurisdiction that threatens its core product. AlphaCorp claims fraud and breach of representations and warranties. BetaTech's former executives claim AlphaCorp rushed due diligence and accepted the company 'as-is'.",
        "case_type": "corporate",
        "urgency": "high",
        "relevant_statutes": ["Delaware General Corporation Law", "Securities Exchange Act Rule 10b-5"],
        "statute_text": {
            "Delaware General Corporation Law": "Directors of Delaware corporations owe fiduciary duties of care and loyalty to the corporation and its shareholders. Under Section 251, a merger agreement must be approved by the board and a majority of the outstanding stock. The 'business judgment rule' typically protects directors' decisions unless there is evidence of fraud, bad faith, or self-dealing, which may trigger 'entire fairness' review as detailed in Section 144.",
            "Securities Exchange Act Rule 10b-5": "It shall be unlawful for any person, directly or indirectly, by the use of any means of interstate commerce, to employ any device, scheme, or artifice to defraud. This includes making any untrue statement of a material fact or omitting to state a material fact necessary in order to make the statements made not misleading. Liability requires proof of scienter—an intent to deceive, manipulate, or defraud—and reliance by the plaintiff upon the misrepresentation."
        },
        "prior_precedents": ["Acquirer v. Target (2019)"],
        "parties": {"plaintiff": "AlphaCorp", "defendant": "BetaTech Former Shareholders"},
        "relief_sought": "Rescission of the acquisition and $100M in damages.",
        "difficulty": "hard",
        "expected_classification": "corporate",
        "expected_resolution_elements": ["representations and warranties", "material adverse effect", "fraudulent inducement", "due diligence"]
    },
    "CASE-H03": {
        "case_id": "CASE-H03",
        "title": "Multi-State Consumer Class Action",
        "jurisdiction": "Federal Court (MDL)",
        "year": 2023,
        "facts": "A defective consumer appliance caused fires in homes across 15 different states. Plaintiffs are seeking a nationwide class action. The defendant manufacturer argues that because strict liability and negligence laws vary significantly among the 15 states, a nationwide class cannot be certified. Furthermore, the statute of limitations has expired in 3 of the states.",
        "case_type": "tort",
        "urgency": "medium",
        "relevant_statutes": ["FRCP Rule 23", "Class Action Fairness Act (CAFA)"],
        "statute_text": {
            "FRCP Rule 23": "One or more members of a class may sue or be sued as representative parties on behalf of all only if the class is so numerous that joinder of all members is impracticable and there are questions of law or fact common to the class. For certification under Rule 23(b)(3), the court must find that questions of law or fact common to class members predominate over any questions affecting only individual members, as analyzed in conjunction with the 'superiority' requirement of Section (b)(3)(A-D).",
            "Class Action Fairness Act (CAFA)": "The Class Action Fairness Act expands federal jurisdiction over large-scale class actions where the amount in controversy exceeds $5 million and minimal diversity exists. Under 28 U.S.C. § 1332(d), a federal court may decline jurisdiction if more than two-thirds of the class members and the primary defendants are citizens of the state in which the action was filed. This requires a complex analysis of the 'home state' and 'local controversy' exceptions."
        },
        "prior_precedents": ["In re Appliance Fires Litigation (2018)"],
        "parties": {"plaintiff": "Nationwide Consumer Class", "defendant": "Appliance Manufacturer"},
        "relief_sought": "Class certification and punitive damages.",
        "difficulty": "hard",
        "expected_classification": "tort",
        "expected_resolution_elements": ["Rule 23 predominance", "choice of law", "statute_limitations", "CAFA jurisdiction"]
    },
    "CASE-H04": {
        "case_id": "CASE-H04",
        "title": "Heirs v. Estate Trust",
        "jurisdiction": "New York & Switzerland",
        "year": 2022,
        "facts": "A wealthy patriarch died leaving a complex web of offshore trusts and a contested will in New York. The primary heirs claim the patriarch lacked testamentary capacity when he signed a recent codicil disinheriting them in favor of a new charity. The charity is based in Switzerland and refuses to submit to US jurisdiction. The estate's primary assets are frozen.",
        "case_type": "family",
        "urgency": "high",
        "relevant_statutes": ["NY Estates, Powers and Trusts Law", "Hague Convention on Trusts"],
        "statute_text": {
            "NY Estates, Powers and Trusts Law": "A will or codicil is valid only if the testator was of sound mind and memory and followed the execution formalities of Section 3-2.1. Testamentary capacity requires the testator to understand the nature of the act, the extent of their property, and the natural objects of their bounty. Under Section 11-1.1, fiduciaries have broad powers but must act with the prudence of a person of ordinary discretion in the management of estate assets, subject to judicial review under the SCPA.",
            "Hague Convention on Trusts": "The Convention establishes common conflict-of-law rules for the recognition of trusts and their validity across international borders. Article 6 provides that a trust shall be governed by the law chosen by the settlor, while Article 15 reserves the application of mandatory rules of the forum state, such as those protecting forced heirship or the protection of creditors. Jurisdiction over a foreign trust often hinges on the 'closest connection' test defined in Article 7, complicating disputes involving offshore jurisdictions."
        },
        "prior_precedents": ["Estate of Billionaire (2017)"],
        "parties": {"plaintiff": "Disinherited Heirs", "defendant": "Swiss Charity & Estate Executor"},
        "relief_sought": "Invalidation of the codicil and distribution of the estate according to the prior will.",
        "difficulty": "hard",
        "expected_classification": "family",
        "expected_resolution_elements": ["testamentary capacity", "undue influence", "international jurisdiction", "asset freezing"]
    }
}
