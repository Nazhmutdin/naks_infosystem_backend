from uuid import uuid4
from datetime import date, timedelta
from string import digits, ascii_uppercase

from faker import Faker

from dateutils import relativedelta
from naks_library.utils.funcs import seq

from app.application.dto import PersonalDTO, PersonalNaksCertificationDTO, NdtDTO, AcstDTO
from app.infrastructure.database.setup import create_engine


engine = create_engine()



GTDS = [
    "ПТО (1)",
    "ПТО (2)",
    "ПТО (3)",
    "ПТО (4)",
    "ПТО (5)",
    "ПТО (6)",
    "ПТО (7)",
    "ПТО (8)",
    "ПТО (9)",
    "ПТО (10)",
    "ПТО (11)",
    "ПТО (12)",
    "ПТО (13)",
    "ПТО (14)",
    "КО (1)",
    "КО (2)",
    "КО (3)",
    "КО (4)",
    "КО (5)",
    "ГО (1)",
    "ГО (2)",
    "ГО (3)",
    "ГО (4)",
    "ГО (5)",
    "ГО (6)",
    "ГО (7)",
    "НГДО (1)",
    "НГДО (2)",
    "НГДО (3)",
    "НГДО (4)",
    "НГДО (5)",
    "НГДО (6)",
    "НГДО (7)",
    "НГДО (8)",
    "НГДО (9)",
    "НГДО (10)",
    "НГДО (11)",
    "НГДО (12)",
    "НГДО (13)",
    "МО (1)",
    "МО (2)",
    "МО (3)",
    "МО (4)",
    "МО (5)",
    "МО (6)",
    "ОХНВП (1)",
    "ОХНВП (2)",
    "ОХНВП (3)",
    "ОХНВП (4)",
    "ОХНВП (5)",
    "ОХНВП (6)",
    "ОХНВП (7)",
    "ОХНВП (8)",
    "ОХНВП (9)",
    "ОХНВП (10)",
    "ОХНВП (11)",
    "ОХНВП (12)",
    "ОХНВП (13)",
    "ОХНВП (14)",
    "ОХНВП (15)",
    "ОХНВП (16)",
    "ГДО (1)",
    "ОТОГ (1)",
    "ОТОГ (2)",
    "ОТОГ (3)",
    "СК (1)",
    "СК (2)",
    "СК (3)",
    "СК (4)",
    "КСМ (1)",
    "КСМ (2)"
]


class FakePersonalDataGenerator:
    faker = Faker()

    def generate(self, k: int = 20) -> list[dict]:
        data = []

        for _ in range(k):
            sub_data = {}

            sub_data["ident"] = uuid4()
            sub_data["name"] = self.faker.name()
            sub_data["kleymo"] = "".join(self.faker.random_choices(ascii_uppercase + digits, 4))
            sub_data["birthday"] = self.faker.date_of_birth()
            sub_data["passport_number"] = "".join([self.faker.random_element(ascii_uppercase)] + list(self.faker.random_choices(digits, 10)))
            sub_data["exp_age"] = self.faker.random_number(fix_len=True, digits=2)
            sub_data["nation"] = self.faker.country_code("alpha-3")

            data.append(sub_data)
        
        return data


class FakePersonalCertificationDataGenerator:
    faker = Faker()

    def __init__(self, personals: list[PersonalDTO]) -> None:
        self.personals = personals

    def generate(self, k: int = 100) -> list[dict]:
        data = []

        for _ in range(k):
            sub_data = {}

            sub_data["ident"] = uuid4()
            sub_data["personal_ident"] = self.faker.random_element(self.personals).ident
            sub_data["certification_number"] = "ТОР-6АЦ" + "-" + self.faker.random_element(["I", "II", "III", "IV", "V"]) + "-" + str(self.faker.random_number(digits=5, fix_len=True))
            sub_data["certification_date"] = self.faker.date_between(
                date.today() - timedelta(weeks=200),
                date.today()
            )
            sub_data["expiration_date"] = sub_data["certification_date"] + relativedelta(years=2)
            sub_data["expiration_date_fact"] = sub_data["certification_date"] + self.faker.random_element([relativedelta(years=2), relativedelta(years=3), relativedelta(years=4)])
            sub_data["insert"] = self.faker.random_element([None, "В1", "В2"])
            sub_data["company"] = self.faker.company()
            sub_data["gtd"] = self.faker.random_choices(GTDS, 15)
            sub_data["method"] = self.faker.random_element(["РД", "РАД", "МПГ", "МП", "АФ", "П"])
            sub_data["detail_types"] = self.faker.random_elements(["Л+Т", "Т", "Л"])
            sub_data["joint_types"] = ["УШ", "СШ"]
            sub_data["materials"] = self.faker.random_elements(["M01", "M03", "M07", "M11"])
            sub_data["detail_thikness_from"] = self.faker.random_element(seq(0, 150, 0.1))
            sub_data["detail_thikness_before"] = sub_data["detail_thikness_from"] + self.faker.random_element(seq(0, 2000, 0.1))
            sub_data["outer_diameter_from"] = None
            sub_data["outer_diameter_before"] = None
            sub_data["rod_diameter_from"] = None
            sub_data["rod_diameter_before"] = None
            sub_data["detail_diameter_from"] = None
            sub_data["detail_diameter_before"] = None
            sub_data["html"] = ""

            self._dump_diameters(sub_data)

            data.append(sub_data)
        
        return data
    

    def _dump_diameters(self, data: dict):
        mode = self.faker.random_element(["details", "details", "details", "details", "outer", "rod"])

        if mode == "details":
            data["detail_diameter_from"] = self.faker.random_element(seq(0, 150, 0.1))
            data["detail_diameter_before"] = data["detail_diameter_from"] + self.faker.random_element(seq(0, 2000, 0.1))

        elif mode == "outer":
            data["outer_diameter_from"] = self.faker.random_element(seq(0, 150, 0.1))
            data["outer_diameter_before"] = data["outer_diameter_from"] + self.faker.random_element(seq(0, 2000, 0.1))

        else:
            data["rod_diameter_from"] = self.faker.random_element(seq(0, 150, 0.1))
            data["rod_diameter_before"] = data["rod_diameter_from"] + self.faker.random_element(seq(0, 2000, 0.1))

            

class FakeNDTDataGenerator:
    faker = Faker()

    def __init__(self, personals: list[PersonalDTO]) -> None:
        self.personals = personals


    def generate(self, k: int = 100) -> list[dict]:
        data = []

        for _ in range(k):
            sub_data = {}

            sub_data["ident"] = uuid4()
            sub_data["personal_ident"] = self.faker.random_element(self.personals).ident
            sub_data["company"] = self.faker.company()
            sub_data["subcompany"] = self.faker.company()
            sub_data["project"] = "some project name"
            sub_data["welding_date"] = self.faker.date_between(
                date.today() - timedelta(weeks=100),
                date.today()
            )
            sub_data["ndt_type"] = self.faker.random_element(["type1", "typ2", "type3", "type4", "type5"])
            sub_data["total_welded"] = self.faker.random_element(seq(0, 5000, 0.1))
            sub_data["total_ndt"] = self.faker.random_element(seq(0, 150, 0.1))
            sub_data["total_accepted"] = self.faker.random_element(seq(0, sub_data["total_ndt"], 0.1))
            sub_data["total_rejected"] = sub_data["total_ndt"] - sub_data["total_accepted"]

            data.append(sub_data)
        
        return data


class FakeAcstDataGenerator:
    faker = Faker()

    def generate(self, k: int = 100) -> list[dict]:
        data = []

        for _ in range(k):
            sub_data = {}

            sub_data["ident"] = uuid4()
            sub_data["acst_number"] = "АЦСТ-11-" + str(self.faker.random_number(digits=5, fix_len=True))
            sub_data["certification_date"] = self.faker.date_between(
                date.today() - timedelta(weeks=200),
                date.today()
            )
            sub_data["expiration_date"] = sub_data["certification_date"] + relativedelta(years=5)
            sub_data["company"] = self.faker.company()
            sub_data["gtd"] = self.faker.random_choices(GTDS, 15)
            sub_data["method"] = self.faker.random_element(["РД", "РАД", "МПГ", "МП", "АФ", "П"])
            sub_data["detail_types"] = self.faker.random_elements(["Л+Т", "Т", "Л"])
            sub_data["joint_types"] = ["УШ", "СШ"]
            sub_data["materials"] = self.faker.random_elements(["M01", "M03", "M07", "M11"])
            sub_data["thikness_from"] = self.faker.random_element(seq(0, 150, 0.1))
            sub_data["thikness_before"] = sub_data["thikness_from"] + self.faker.random_element(seq(0, 2000, 0.1))
            sub_data["diameter_from"] = self.faker.random_element(seq(0, 150, 0.1))
            sub_data["diameter_before"] = sub_data["diameter_from"] + self.faker.random_element(seq(0, 2000, 0.1))
            sub_data["preheating"] = self.faker.random_elements([True, True, True, False], 2)
            sub_data["heat_treatment"] = self.faker.random_elements([True, True, True, False], 2)
            sub_data["html"] = ""

            data.append(sub_data)
        
        return data


class TestData:
    def __init__(self) -> None:
        self.faker = Faker()
        self.fake_personal_generator = FakePersonalDataGenerator()
        self.fake_personals_dicts = self.fake_personal_generator.generate(10)
        self.fake_personal_certification_generator = FakePersonalCertificationDataGenerator(self.fake_personals)
        self.fake_personal_certifications_dicts = self.fake_personal_certification_generator.generate(25)
        self.fake_ndt_generator = FakeNDTDataGenerator(self.fake_personals)
        self.fake_ndts_dicts = self.fake_ndt_generator.generate(25)
        self.fake_acst_generator = FakeAcstDataGenerator()
        self.fake_acsts_dicts = self.fake_acst_generator.generate(25)


    @property
    def fake_personals(self) -> list[PersonalDTO]:
        return [PersonalDTO(**el) for el in self.fake_personals_dicts]


    @property
    def fake_personal_certifications(self) -> list[PersonalNaksCertificationDTO]:
        return [PersonalNaksCertificationDTO(**el) for el in self.fake_personal_certifications_dicts]


    @property
    def fake_ndts(self) -> list[NdtDTO]:
        return [NdtDTO(**el) for el in self.fake_ndts_dicts]


    @property
    def fake_acsts(self) -> list[AcstDTO]:
        return [AcstDTO(**el) for el in self.fake_acsts_dicts]


test_data = TestData()