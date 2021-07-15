from main import db

class Sheet(db.Model):
    __tablename__ = "Sheet"
    CharID = db.Column(db.Integer, primary_key = True)

    #Section One | Main Info
    CharacterName = db.Column(db.String)
    CharacterClass = db.Column(db.String)
    Level = db.Column(db.Integer)
    Background = db.Column(db.String)
    Race = db.Column(db.String)
    Alignment = db.Column(db.String(2))
    OwnerID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)

    owner = db.relationship("User", backref="sheets")


    #Section Two | Character Stats
    STR = db.Column(db.Integer)
    STRMod = db.Column(db.Integer)
    DEX = db.Column(db.Integer)
    DEXMod = db.Column(db.Integer)
    CON = db.Column(db.Integer)
    CONMod = db.Column(db.Integer)
    INT = db.Column(db.Integer)
    INTMod = db.Column(db.Integer)
    WIS = db.Column(db.Integer)
    WISMod = db.Column(db.Integer)
    CHA = db.Column(db.Integer)
    CHAMod = db.Column(db.Integer)


    #Section Three | Prof Bonus and Inspiration
    ProfBonus = db.Column(db.Integer)
    Inspiration = db.Column(db.Integer)


    #Section Four | Saving Throws
    STRSave = db.Column(db.Integer)
    STRSaveProf = db.Column(db.Integer)
    DEXSave = db.Column(db.Integer)
    DEXSaveProf = db.Column(db.Integer)
    CONSave = db.Column(db.Integer)
    CONSaveProf = db.Column(db.Integer)
    INTSave = db.Column(db.Integer)
    INTSaveProf = db.Column(db.Integer)
    WISSave = db.Column(db.Integer)
    WISSaveProf = db.Column(db.Integer)
    CHASave = db.Column(db.Integer)
    CHASaveProf = db.Column(db.Integer)


    #Section Five | Skills
    ##Skills
    Acrobatics = db.Column(db.Integer) #DEX
    Animal_Handling = db.Column(db.Integer) #WIS
    Arcana = db.Column(db.Integer) #INT
    Athletics = db.Column(db.Integer) #STR
    Deception = db.Column(db.Integer) #CHA
    History = db.Column(db.Integer) #INT
    Insight = db.Column(db.Integer) #WIS
    Intimidation = db.Column(db.Integer) #CHA
    Investigation = db.Column(db.Integer) #INT
    Medicine = db.Column(db.Integer) #WIS
    Nature = db.Column(db.Integer) #INT
    Perception = db.Column(db.Integer) #WIS
    Performance = db.Column(db.Integer) #CHA
    Persuasion = db.Column(db.Integer) #CHA
    Religion = db.Column(db.Integer) #INT
    Sleight_Of_Hand = db.Column(db.Integer) #DEX
    Stealth = db.Column(db.Integer) #DEX
    Survival = db.Column(db.Integer) #WIS

    ##Skill Proficiency
    AcrobaticsProf = db.Column(db.Integer)
    Animal_HandlingProf = db.Column(db.Integer)
    ArcanaProf = db.Column(db.Integer)
    AthleticsProf = db.Column(db.Integer)
    DeceptionProf = db.Column(db.Integer)
    HistoryProf = db.Column(db.Integer)
    InsightProf = db.Column(db.Integer)
    IntimidationProf = db.Column(db.Integer)
    InvestigationProf = db.Column(db.Integer)
    MedicineProf = db.Column(db.Integer)
    NatureProf = db.Column(db.Integer)
    PerceptionProf = db.Column(db.Integer)
    PerformanceProf = db.Column(db.Integer)
    PersuasionProf = db.Column(db.Integer)
    ReligionProf = db.Column(db.Integer)
    Sleight_Of_HandProf = db.Column(db.Integer)
    StealthProf = db.Column(db.Integer)
    SurvivalProf = db.Column(db.Integer) 

    PassivePerception = db.Column(db.Integer)


    #Section Six | Combat Stats
    AC = db.Column(db.Integer)
    Initiative = db.Column(db.Integer)

    ##Hit Points
    MaxHP = db.Column(db.Integer)
    CurrentHP = db.Column(db.Integer)
    TempHP = db.Column(db.Integer)

    ##Hit Dice
    HitDiceAmount = db.Column(db.Integer)
    CurrentHitDice = db.Column(db.Integer)
    HitDiceType = db.Column(db.Integer)

    ##Death Saves
    SuccessOne = db.Column(db.Integer)
    SuccessTwo = db.Column(db.Integer)
    SuccessThree = db.Column(db.Integer)
    FailureOne = db.Column(db.Integer)
    FailureTwo = db.Column(db.Integer)
    FailureThree = db.Column(db.Integer)


    #Section Seven | Attacks
    ##One
    ATKNameI = db.Column(db.String)
    ATKBonusI = db.Column(db.Integer)
    ATKDMGI = db.Column(db.Integer)
    ATKTypeI = db.Column(db.String)

    ##Two
    ATKNameII = db.Column(db.String)
    ATKBonusII = db.Column(db.Integer)
    ATKDMGII = db.Column(db.Integer)
    ATKTypeII = db.Column(db.String)

    ##Three
    ATKNameIII = db.Column(db.String)
    ATKBonusIII = db.Column(db.Integer)
    ATKDMGIII = db.Column(db.Integer)
    ATKTypeIII = db.Column(db.String)

    ##Four
    ATKNameIV = db.Column(db.String)
    ATKBonusIV = db.Column(db.Integer)
    ATKDMGIV = db.Column(db.Integer)
    ATKTypeIV = db.Column(db.String) 

    ##Five
    ATKNameV = db.Column(db.String)
    ATKBonusV = db.Column(db.Integer)
    ATKDMGV = db.Column(db.Integer)
    ATKTypeV = db.Column(db.String)

    ##Six
    ATKNameVI = db.Column(db.String)
    ATKBonusVI = db.Column(db.Integer)
    ATKDMGVI = db.Column(db.Integer)
    ATKTypeVI = db.Column(db.String)

    ##Seven
    ATKNameVII = db.Column(db.String)
    ATKBonusVII = db.Column(db.Integer)
    ATKDMGVII = db.Column(db.Integer)
    ATKTypeVII = db.Column(db.String)

    ##Eight
    ATKNameVIII = db.Column(db.String)
    ATKBonusVIII = db.Column(db.Integer)
    ATKDMGVIII = db.Column(db.Integer)
    ATKTypeVIII = db.Column(db.String)

    ##Nine
    ATKNameIX = db.Column(db.String)
    ATKBonusIX = db.Column(db.Integer)
    ATKDMGIX = db.Column(db.Integer)
    ATKTypeIX = db.Column(db.String)
    

    #Section Eight | Equipment
    ##Money
    CoinCopper = db.Column(db.Integer)
    CoinSilver = db.Column(db.Integer)
    CoinElectrum = db.Column(db.Integer)
    CoinGold = db.Column(db.Integer)
    CoinPlat = db.Column(db.Integer)

    ##Equipment
    ###Each Column is a different line
    EquipOne = db.Column(db.String)
    EquipTwo = db.Column(db.String)
    EquipThree = db.Column(db.String)
    EquipFour = db.Column(db.String)
    EquipFive = db.Column(db.String)
    EquipSix = db.Column(db.String)
    EquipSeven = db.Column(db.String)
    EquipEight = db.Column(db.String)
    EquipNine = db.Column(db.String)
    EquipTen = db.Column(db.String)
    EquipEleven = db.Column(db.String)
    EquipTwelve = db.Column(db.String)
    EquipThirteen = db.Column(db.String)
    EquipFourteen = db.Column(db.String)
    EquipFifteen = db.Column(db.String)


    #Section Nine | Other Proficiencies
    ###Each Column is a different line
    OtherProfOne = db.Column(db.String)
    OtherProfTwo = db.Column(db.String)
    OtherProfThree = db.Column(db.String)
    OtherProfFour = db.Column(db.String)
    OtherProfFive = db.Column(db.String)
    OtherProfSix = db.Column(db.String)
    OtherProfSeven = db.Column(db.String)
    OtherProfEight = db.Column(db.String)
    OtherProfNine = db.Column(db.String)
    OtherProfTen = db.Column(db.String)
    OtherProfEleven = db.Column(db.String)
    OtherProfTwelve = db.Column(db.String)
    OtherProfThirteen = db.Column(db.String)


    #Section Ten | Personality
    PersonalityTraits = db.Column(db.String)
    Ideals = db.Column(db.String)
    Bonds = db.Column(db.String)
    Flaws = db.Column(db.String)


class User(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String)

db.create_all()