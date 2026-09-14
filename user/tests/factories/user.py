import factory
from factory.django import DjangoModelFactory

from user.models import AdminProfile, MedicProfile, PatientProfile, User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = User.Role.PATIENT


class AdminProfileFactory(DjangoModelFactory):
    class Meta:
        model = AdminProfile

    user = factory.SubFactory(UserFactory, role=User.Role.ADMIN)


class MedicProfileFactory(DjangoModelFactory):
    class Meta:
        model = MedicProfile

    user = factory.SubFactory(UserFactory, role=User.Role.MEDIC)
    license_number = factory.Faker("bothify", text="MED-#####")
    specialty = factory.Faker("job")


class PatientProfileFactory(DjangoModelFactory):
    class Meta:
        model = PatientProfile

    user = factory.SubFactory(UserFactory, role=User.Role.PATIENT)
    date_of_birth = factory.Faker("date_of_birth")
    phone_number = factory.Faker("phone_number")